# 🧠 Personal Knowledge Genie

A powerful AI-powered document processing and chat application that allows you to upload documents, store them in a vector database, and chat with an AI assistant that can reference your uploaded content.

## ✨ Features

- **📁 Document Upload**: Support for PDF and text file uploads
- **🔍 Vector Search**: Documents are stored in ChromaDB for efficient similarity search
- **💬 AI Chat Interface**: Chat with an AI assistant powered by Google's Gemini model
- **🧠 Context-Aware Responses**: AI responses include relevant content from your uploaded documents
- **💾 Persistent Storage**: All documents are stored persistently in a local vector database
- **🔒 Secure API Key Management**: API keys are stored securely in environment variables

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **AI/LLM**: Google Generative AI (Gemini 2.5 Flash Lite)
- **Vector Database**: ChromaDB
- **PDF Processing**: PyPDF2
- **AI Framework**: Pydantic AI
- **Environment Management**: python-dotenv

## 📋 Prerequisites

- Python 3.8+
- Google Generative AI API key

## � Documentation

For documentation around the flow of the application, please refer to: [Personal Knowledge Genie Documentation](docs/Personal_Knowledge_Genie.pdf)

## �🚀 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Krish-Naidu/Personal_Knowledge_Genie.git
   cd Personal_Knowledge_Genie
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv myenv
   # On Windows:
   myenv\Scripts\activate
   # On macOS/Linux:
   source myenv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   - Create a `.env` file in the project root
   - Add your Google API key:
     ```
     GOOGLE_API_KEY=your_google_api_key_here
     ```

## 🎯 Usage

1. **Start the application**:
   ```bash
   streamlit run chat_app.py
   ```

2. **Upload Documents**:
   - Use the left panel to upload PDF or text files
   - Click "Process" for each file to add it to your knowledge base

3. **Chat with Your Documents**:
   - Use the right panel to ask questions about your uploaded documents
   - The AI will search through your documents and provide context-aware responses

## 📁 Project Structure

```
Personal_Knowledge_Genie/
├── chat_app.py              # Main Streamlit application
├── chromadb_utils.py        # ChromaDB operations (store, search, list documents)
├── embedding_utils.py       # Text embedding utilities
├── llm_utils.py            # LLM integration and API management
├── pdf_utils.py            # PDF text extraction utilities
├── requirements.txt         # Python dependencies
├── .env                    # Environment variables (not in repo)
├── .gitignore              # Git ignore file
├── myenv/                  # Virtual environment
└── vectordb/               # ChromaDB storage (created automatically)
```

## 🔧 Core Components

### `chat_app.py`
Main Streamlit application with:
- Two-panel layout (file upload + chat interface)
- File processing and storage integration
- Interactive chat with document context

### `chromadb_utils.py`
ChromaDB operations:
- `store_text_as_document()` - Store text with metadata
- `search_document_by_text()` - Search for relevant documents
- `get_all_document_filenames()` - List all stored document names

### `llm_utils.py`
LLM integration:
- `init_LLM()` - Initialize the AI agent
- `get_agent_response()` - Get responses from the AI
- `set_api_key()` - Set API key in environment

### `pdf_utils.py`
PDF processing:
- `extract_text_from_pdf()` - Extract text from PDF files

### `embedding_utils.py`
Text embedding:
- `get_text_embedding()` - Generate embeddings for text

## 🔒 Security

- API keys are stored in `.env` file (excluded from version control)
- Environment variables are loaded securely using python-dotenv
- No hardcoded sensitive information in the codebase

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Generative AI for providing the language model
- ChromaDB for the vector database solution
- Streamlit for the web application framework
- PyPDF2 for PDF processing capabilities

## 📞 Support

If you encounter any issues or have questions, please open an issue on GitHub.

---

**Made with ❤️ by [Krish-Naidu](https://github.com/Krish-Naidu)**
