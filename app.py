import os
import shutil
import streamlit as st
from dotenv import load_dotenv
from langchain.chains import ConversationalRetrievalChain
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
import gc

# Load environment variables
load_dotenv('.env')

# Streamlit page configuration
st.set_page_config(
    page_title="DocBot - Document Q&A Assistant",
    page_icon="📚",
    layout="wide"
)

st.title("📚 DocBot - Document Q&A Assistant")
st.markdown("Upload your documents and ask questions about them!")

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'pdf_qa' not in st.session_state:
    st.session_state.pdf_qa = None
if 'documents_processed' not in st.session_state:
    st.session_state.documents_processed = False

def remove_existing_data():
    """Remove existing data-old folder"""
    if os.path.exists("./data-old"):
        try:
            shutil.rmtree("./data-old")
            st.success("✅ Removed existing vector database")
        except Exception as e:
            st.error(f"❌ Error removing existing data: {str(e)}")
            return False
    return True

def process_documents(uploaded_files):
    """Process uploaded documents and create vector database"""
    
    # Remove existing data folder
    if not remove_existing_data():
        return None
    
    # Create docs directory
    if not os.path.exists("docs"):
        try:
            os.makedirs("docs")
        except Exception as e:
            st.error(f"❌ Error creating directory docs: {str(e)}")
            return None
    
    
    # Clear existing files in docs folder
    for file in os.listdir("docs"):
        try:
            os.remove(os.path.join("docs", file))
        except Exception as e:
            st.error(f"❌ Error removing file {file}: {str(e)}")
            return None
    
    # Save uploaded files
    for uploaded_file in uploaded_files:
        try:
            with open(os.path.join("docs", uploaded_file.name), "wb") as f:
                f.write(uploaded_file.getbuffer())
        except Exception as e:
            st.error(f"❌ Error saving file {uploaded_file.name}: {str(e)}")
            return None
    
    documents = []
    
    # Process documents
    with st.spinner("📄 Processing documents..."):
        for file in os.listdir("docs"):
            try:
                if file.endswith(".pdf"):
                    pdf_path = os.path.join("docs", file)
                    loader = PyPDFLoader(pdf_path)
                    documents.extend(loader.load())
                elif file.endswith(".docx"):
                    docx_path = os.path.join("docs", file)
                    loader = Docx2txtLoader(docx_path)
                    documents.extend(loader.load())
                elif file.endswith(".txt"):
                    txt_path = os.path.join("docs", file)
                    loader = TextLoader(txt_path)
                    documents.extend(loader.load())
                else:
                    st.warning(f"⚠️ Skipping unsupported file: {file}")
            except Exception as e:
                st.error(f"❌ Error processing file {file}: {str(e)}")
                return None
    
    if not documents:
        st.error("❌ No supported documents found!")
        return None
    
    # Split documents into chunks
    with st.spinner("✂️ Splitting documents into chunks..."):
        try:
            text_splitter = CharacterTextSplitter(chunk_size=700, chunk_overlap=100)
            documents = text_splitter.split_documents(documents)
        except Exception as e:
            st.error(f"❌ Error splitting documents: {str(e)}")
            return None
    
    # Create embeddings
    with st.spinner("🧠 Creating embeddings..."):
        try:
            embedding = GoogleGenerativeAIEmbeddings(
                model="models/embedding-001",
                api_key=os.getenv("GOOGLE_API_KEY")
            )
            
            # Debug: Log before creating vector store
            #st.write(f"DEBUG: Before FAISS init - ./data-old contents: {os.listdir('./data-old') if os.path.exists('./data-old') else 'Does not exist'}")
            
            # Generate vector DB from documents
            vectordb = FAISS.from_documents(documents, embedding=embedding)
            vectordb.save_local("./data-old")
            
            # Debug: Log after creating vector store
            #st.write(f"DEBUG: After FAISS init - ./data-old contents: {os.listdir('./data-old')}")
        except Exception as e:
            st.error(f"❌ Error creating vector database: {str(e)}")
            return None
    
    # Create Q&A chain
    with st.spinner("🔗 Setting up Q&A chain..."):
        try:
            pdf_qa = ConversationalRetrievalChain.from_llm(
                ChatGoogleGenerativeAI(
                    model="gemini-2.5-pro",
                    api_key=os.getenv("GOOGLE_API_KEY"),
                    temperature=0.7
                ),
                retriever=vectordb.as_retriever(search_kwargs={'k': 6}),
                return_source_documents=True,
                verbose=False
            )
        except Exception as e:
            st.error(f"❌ Error setting up Q&A chain: {str(e)}")
            return None
    
    return pdf_qa

# Sidebar for file upload and controls
with st.sidebar:
    st.header("📁 Document Upload")
    
    uploaded_files = st.file_uploader(
        "Choose files",
        accept_multiple_files=True,
        type=['pdf', 'docx', 'txt'],
        help="Upload PDF, DOCX, or TXT files"
    )
    
    if st.button("🔄 Process Documents", type="primary"):
        if uploaded_files:
            st.session_state.pdf_qa = process_documents(uploaded_files)
            if st.session_state.pdf_qa:
                st.session_state.documents_processed = True
                st.success(f"✅ Processed {len(uploaded_files)} documents successfully!")
        else:
            st.warning("⚠️ Please upload at least one document first!")
    
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        st.success("✅ Chat history cleared!")
    
    if st.button("🔄 Reset Vector Database"):
        remove_existing_data()
        st.session_state.pdf_qa = None
        st.session_state.documents_processed = False
        st.session_state.chat_history = []
        if os.path.exists("docs"):
            try:
                shutil.rmtree("docs")
                st.success("✅ Cleared docs directory")
            except Exception as e:
                st.error(f"❌ Error clearing docs directory: {str(e)}")
        gc.collect()  # Force garbage collection
        st.success("✅ Vector database, session state, and docs directory reset!")

# Main chat interface
if st.session_state.documents_processed and st.session_state.pdf_qa:
    st.header("💬 Chat with your documents")
    
    # Display chat history
    for i, (question, answer) in enumerate(st.session_state.chat_history):
        with st.container():
            st.markdown(f"**🤔 Question {i+1}:** {question}")
            st.markdown(f"**🤖 Answer:** {answer}")
            st.divider()
    
    # Chat input
    with st.form("chat_form", clear_on_submit=True):
        user_question = st.text_input(
            "Ask a question about your documents:",
            placeholder="What is this document about?",
            key="user_input"
        )
        submit_button = st.form_submit_button("Send", type="primary")
        
        if submit_button and user_question:
            with st.spinner("🤔 Thinking..."):
                try:
                    result = st.session_state.pdf_qa.invoke({
                        "question": user_question,
                        "chat_history": st.session_state.chat_history
                    })
                    
                    # Add to chat history
                    st.session_state.chat_history.append((user_question, result["answer"]))
                    
                    # Display the new answer
                    st.markdown(f"**🤔 Question:** {user_question}")
                    st.markdown(f"**🤖 Answer:** {result['answer']}")
                    
                    # Show source documents if available
                    if result.get("source_documents"):
                        with st.expander("📖 Source Documents"):
                            for i, doc in enumerate(result["source_documents"]):
                                st.markdown(f"**Source {i+1}:**")
                                st.text(doc.page_content[:300] + "..." if len(doc.page_content) > 300 else doc.page_content)
                                if hasattr(doc, 'metadata') and doc.metadata:
                                    st.json(doc.metadata)
                    
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Error processing question: {str(e)}")

else:
    st.info("👆 Please upload and process documents using the sidebar to start chatting!")
    
    # Display instructions
    st.markdown("""
    ## How to use DocBot:
    
    1. **Upload Documents**: Use the sidebar to upload PDF, DOCX, or TXT files
    2. **Process Documents**: Click "Process Documents" to create the vector database
    3. **Ask Questions**: Once processing is complete, you can ask questions about your documents
    4. **View Sources**: Expand the "Source Documents" section to see which parts of your documents were used to answer your question
    
    ## Supported File Types:
    - 📄 PDF files (.pdf)
    - 📝 Word documents (.docx)
    - 📋 Text files (.txt)
    
    ## Features:
    - 🧠 Intelligent document understanding using Google's Gemini AI
    - 💬 Conversational interface with chat history
    - 📖 Source document references
    - 🔄 Easy document reprocessing
    """)

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit, LangChain, and Google Gemini AI")
