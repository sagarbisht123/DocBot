# 📚 DocBot - Document Q&A Assistant

A powerful AI-powered document question-answering system built with Streamlit, LangChain, and Google's Gemini AI. Upload your documents and start having intelligent conversations with them!

![DocBot Interface](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-121212?style=for-the-badge&logo=langchain&logoColor=white)

## ✨ Features

- 🤖 **AI-Powered Q&A**: Leverage Google's Gemini AI for intelligent document understanding
- 📄 **Multi-Format Support**: Process PDF, DOCX, and TXT files seamlessly
- 💬 **Conversational Interface**: Chat with your documents using natural language
- 🔍 **Source References**: View which parts of your documents were used to generate answers
- ⚡ **Vector Database**: Fast document retrieval using Chroma vector store
- 🧠 **Smart Chunking**: Intelligent text splitting for optimal processing
- 📊 **Chat History**: Keep track of your conversation with documents
- 🎨 **User-Friendly UI**: Clean and intuitive Streamlit interface

## 🚀 Quick Start

### Prerequisites

- Python >=3.10,<3.11
- Poetry (for dependency management)
- Google API Key (for Gemini AI)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sagarbisht123/DocBot.git
   cd DocBot
   ```

2. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```bash
   cp .env.example .env  # If you have an example file
   # OR create a new .env file
   touch .env
   ```
   
   Add your Google API key to the `.env` file:
   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   ```
   
   > **Getting a Google API Key:**
   > 1. Go to [Google AI Studio](https://aistudio.google.com/)
   > 2. Sign in with your Google account
   > 3. Create a new API key
   > 4. Copy the key to your `.env` file

3. **Install dependencies**
   ```bash
   poetry install
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

The application will open in your default web browser at `http://localhost:8501`

## 📖 How to Use

1. **Upload Documents**: Use the sidebar to upload your PDF, DOCX, or TXT files
2. **Process Documents**: Click the "🔄 Process Documents" button to create the vector database
3. **Ask Questions**: Once processing is complete, start asking questions about your documents
4. **View Sources**: Expand the "📖 Source Documents" section to see document references
5. **Manage Chat**: Use the sidebar buttons to clear chat history or reset the database

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/) - Interactive web application framework
- **AI/ML**: [LangChain](https://langchain.com/) - AI application development framework
- **LLM**: [Google Gemini](https://ai.google.dev/) - Large language model for Q&A
- **Vector Store**: FAISS - Vector database for document retrieval
- **Embeddings**: Google Generative AI Embeddings
- **Document Processing**: PyPDF, Docx2txt, TextLoader

## 📁 Project Structure

```
DocBot/
├── app.py                 # Main Streamlit application
├── .env                   # Environment variables (create this)
├── .env.example          # Example environment file
├── pyproject.toml        # Poetry dependencies
├── poetry.lock           # Locked dependencies
├── README.md             # Project documentation
├── LICENSE               # MIT License
├── .gitignore           # Git ignore rules
├── docs/                # Uploaded documents (auto-created)
└── data-old/            # Vector database storage (auto-created)
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_API_KEY` | Your Google AI API key for Gemini access | Yes |

### Model Settings

You can customize the following parameters in `app.py`:

- **Chunk Size**: Default 700 characters (adjust in `CharacterTextSplitter`)
- **Chunk Overlap**: Default 10 characters
- **Temperature**: Default 0.7 (controls response creativity)
- **Retrieval Results**: Default top 6 similar chunks (`search_kwargs={'k': 6}`)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Troubleshooting

### Common Issues

1. **"No module named 'streamlit'"**
   - Make sure you've activated the poetry environment: `poetry shell`
   - Or run with: `poetry run streamlit run app.py`

2. **"Google API Key not found"**
   - Ensure your `.env` file exists and contains `GOOGLE_API_KEY=your_key_here`
   - Check that the `.env` file is in the root directory

3. **"Error processing documents"**
   - Verify your documents are in supported formats (PDF, DOCX, TXT)
   - Check that the files are not corrupted or password-protected

4. **Vector database issues**
   - Try clicking "🔄 Reset Vector Database" in the sidebar
   - Delete the `data-old/` folder manually if persistent issues occur

## 🔮 Future Enhancements

- [ ] Support for more document formats (PPTX, CSV, etc.)
- [ ] Multiple LLM provider support (OpenAI, Anthropic, etc.)
- [ ] Document preprocessing and cleaning
- [ ] Advanced search filters
- [ ] Export chat conversations
- [ ] Document summarization features
- [ ] Multi-language support



## ⭐ Show Your Support

If you found this project helpful, please give it a star! ⭐

---

**Built with ❤️ using Streamlit, LangChain, and Google Gemini AI**
