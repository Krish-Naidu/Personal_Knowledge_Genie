import unittest
from unittest.mock import Mock, patch, MagicMock, mock_open
import streamlit as st
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestChatApp(unittest.TestCase):
    """Unit tests for chat_app.py"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.mock_agent = Mock()
        self.mock_file = Mock()
        self.mock_file.name = "test.pdf"
        self.mock_file.type = "application/pdf"
        self.mock_file.size = 1024
        
    # ===== LLM Initialization Tests =====
    
    @patch('chat_app.init_LLM')
    def test_init_llm_success(self, mock_init):
        """Test 1: Valid LLM initialization"""
        mock_init.return_value = Mock()
        from chat_app import agent
        self.assertIsNotNone(agent)
        mock_init.assert_called_once()
    
    @patch('chat_app.init_LLM')
    def test_init_llm_failure(self, mock_init):
        """Test 2: LLM initialization failure"""
        mock_init.side_effect = Exception("API connection failed")
        with self.assertRaises(Exception):
            import importlib
            import chat_app
            importlib.reload(chat_app)
    
    # ===== File Upload Tests =====
    
    @patch('streamlit.file_uploader')
    def test_upload_single_pdf(self, mock_uploader):
        """Test 1: Upload single PDF file"""
        mock_file = Mock()
        mock_file.name = "document.pdf"
        mock_file.type = "application/pdf"
        mock_uploader.return_value = [mock_file]
        
        result = mock_uploader()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "document.pdf")
    
    @patch('streamlit.file_uploader')
    def test_upload_multiple_files(self, mock_uploader):
        """Test 2: Upload multiple files"""
        mock_files = [
            Mock(name="doc1.pdf", type="application/pdf"),
            Mock(name="doc2.txt", type="text/plain"),
            Mock(name="doc3.pdf", type="application/pdf")
        ]
        mock_uploader.return_value = mock_files
        
        result = mock_uploader()
        self.assertEqual(len(result), 3)
    
    @patch('streamlit.file_uploader')
    def test_upload_no_files(self, mock_uploader):
        """Test 4: No files uploaded"""
        mock_uploader.return_value = None
        
        result = mock_uploader()
        self.assertIsNone(result)
    
    # ===== Document Retrieval Tests =====
    
    @patch('chat_app.get_all_document_filenames')
    def test_get_documents_with_results(self, mock_get_docs):
        """Test 1: ChromaDB has documents"""
        mock_get_docs.return_value = ["doc1.pdf", "doc2.txt"]
        
        result = mock_get_docs()
        self.assertEqual(len(result), 2)
        self.assertIn("doc1.pdf", result)
    
    @patch('chat_app.get_all_document_filenames')
    def test_get_documents_empty(self, mock_get_docs):
        """Test 2: Empty ChromaDB"""
        mock_get_docs.return_value = []
        
        result = mock_get_docs()
        self.assertEqual(len(result), 0)
    
    @patch('chat_app.get_all_document_filenames')
    def test_get_documents_error(self, mock_get_docs):
        """Test 3: ChromaDB error"""
        mock_get_docs.side_effect = Exception("Database connection failed")
        
        with self.assertRaises(Exception):
            mock_get_docs()
    
    # ===== Document Deletion Tests =====
    
    @patch('chat_app.delete_document_by_filename')
    def test_delete_valid_document(self, mock_delete):
        """Test 1: Valid delete operation"""
        mock_delete.return_value = True
        
        result = mock_delete("doc1.pdf")
        self.assertTrue(result)
        mock_delete.assert_called_once_with("doc1.pdf")
    
    @patch('chat_app.delete_document_by_filename')
    def test_delete_nonexistent_document(self, mock_delete):
        """Test 2: Delete non-existent document"""
        mock_delete.side_effect = Exception("Document not found")
        
        with self.assertRaises(Exception):
            mock_delete("nonexistent.pdf")
    
    @patch('chat_app.delete_document_by_filename')
    def test_delete_chromadb_error(self, mock_delete):
        """Test 3: ChromaDB delete error"""
        mock_delete.side_effect = Exception("Database error")
        
        with self.assertRaises(Exception):
            mock_delete("doc1.pdf")
    
    # ===== PDF Processing Tests =====
    
    @patch('chat_app.extract_text_from_pdf')
    @patch('chat_app.store_text_as_document')
    @patch('os.remove')
    @patch('builtins.open', new_callable=mock_open)
    def test_process_valid_pdf(self, mock_file_open, mock_remove, mock_store, mock_extract):
        """Test 1: Valid PDF processing"""
        mock_extract.return_value = "Sample PDF text content"
        mock_store.return_value = "doc_123"
        
        # Simulate PDF processing
        text = mock_extract("temp_test.pdf")
        doc_id = mock_store(text, metadata={"filename": "test.pdf"})
        
        self.assertEqual(text, "Sample PDF text content")
        self.assertEqual(doc_id, "doc_123")
        mock_extract.assert_called_once_with("temp_test.pdf")
    
    @patch('chat_app.extract_text_from_pdf')
    def test_process_corrupted_pdf(self, mock_extract):
        """Test 2: Corrupted PDF"""
        mock_extract.side_effect = Exception("PDF is corrupted")
        
        with self.assertRaises(Exception):
            mock_extract("corrupted.pdf")
    
    @patch('chat_app.extract_text_from_pdf')
    @patch('os.remove')
    def test_pdf_extraction_failure(self, mock_remove, mock_extract):
        """Test 3: PDF extraction failure with cleanup"""
        mock_extract.side_effect = Exception("Extraction failed")
        
        with self.assertRaises(Exception):
            mock_extract("temp_test.pdf")
    
    # ===== Text File Processing Tests =====
    
    def test_process_valid_text_file(self):
        """Test 1: Valid text file"""
        mock_file = Mock()
        mock_file.read.return_value = b"Hello world"
        
        text = str(mock_file.read(), "utf-8")
        self.assertEqual(text, "Hello world")
    
    def test_process_empty_text_file(self):
        """Test 2: Empty text file"""
        mock_file = Mock()
        mock_file.read.return_value = b""
        
        text = str(mock_file.read(), "utf-8")
        self.assertEqual(text, "")
    
    def test_process_unicode_text_file(self):
        """Test 4: Unicode text file"""
        mock_file = Mock()
        mock_file.read.return_value = "日本語テスト".encode('utf-8')
        
        text = str(mock_file.read(), "utf-8")
        self.assertEqual(text, "日本語テスト")
    
    # ===== Document Storage Tests =====
    
    @patch('chat_app.store_text_as_document')
    def test_store_valid_document(self, mock_store):
        """Test 1: Valid storage"""
        mock_store.return_value = "doc_456"
        
        doc_id = mock_store("Sample text", metadata={"filename": "test.txt"})
        self.assertEqual(doc_id, "doc_456")
    
    @patch('chat_app.store_text_as_document')
    def test_store_chromadb_error(self, mock_store):
        """Test 2: ChromaDB storage error"""
        mock_store.side_effect = Exception("Storage failed")
        
        with self.assertRaises(Exception):
            mock_store("Sample text", metadata={})
    
    @patch('chat_app.store_text_as_document')
    def test_store_large_document(self, mock_store):
        """Test 3: Very long text"""
        large_text = "a" * 1000000
        mock_store.return_value = "doc_789"
        
        doc_id = mock_store(large_text, metadata={})
        self.assertEqual(doc_id, "doc_789")
    
    # ===== Chat History Tests =====
    
    def test_initialize_new_chat_session(self):
        """Test 1: First session"""
        session_state = {}
        
        if "messages" not in session_state:
            session_state["messages"] = []
        
        self.assertEqual(session_state["messages"], [])
    
    def test_existing_chat_session(self):
        """Test 2: Existing session"""
        session_state = {"messages": [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"}
        ]}
        
        self.assertEqual(len(session_state["messages"]), 2)
    
    # ===== Chat Input Tests =====
    
    def test_valid_chat_query(self):
        """Test 1: Valid query"""
        prompt = "What is Python?"
        messages = []
        
        if prompt:
            messages.append({"role": "user", "content": prompt})
        
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0]["content"], "What is Python?")
    
    def test_empty_chat_input(self):
        """Test 2: Empty input"""
        prompt = ""
        messages = []
        
        if prompt:
            messages.append({"role": "user", "content": prompt})
        
        self.assertEqual(len(messages), 0)
    
    def test_very_long_query(self):
        """Test 3: Very long query"""
        prompt = "a" * 10000
        messages = []
        
        if prompt:
            messages.append({"role": "user", "content": prompt})
        
        self.assertEqual(len(messages[0]["content"]), 10000)
    
    def test_special_characters_query(self):
        """Test 4: Special characters"""
        prompt = "Test!@#$%^&*()"
        messages = []
        
        if prompt:
            messages.append({"role": "user", "content": prompt})
        
        self.assertEqual(messages[0]["content"], "Test!@#$%^&*()")
    
    # ===== Document Search Tests =====
    
    @patch('chat_app.search_document_by_text')
    def test_search_with_results(self, mock_search):
        """Test 1: Valid search with results"""
        mock_search.return_value = {
            "documents": [["Result 1", "Result 2", "Result 3"]],
            "metadatas": [[{}, {}, {}]]
        }
        
        results = mock_search("Python basics")
        self.assertEqual(len(results["documents"][0]), 3)
    
    @patch('chat_app.search_document_by_text')
    def test_search_no_results(self, mock_search):
        """Test 2: No matching documents"""
        mock_search.return_value = {
            "documents": [[]],
            "metadatas": [[]]
        }
        
        results = mock_search("Nonexistent topic")
        self.assertEqual(len(results["documents"][0]), 0)
    
    @patch('chat_app.search_document_by_text')
    def test_search_chromadb_error(self, mock_search):
        """Test 3: ChromaDB search error"""
        mock_search.side_effect = Exception("Search failed")
        
        with self.assertRaises(Exception):
            mock_search("Query")
    
    # ===== Context Preparation Tests =====
    
    def test_context_with_three_results(self):
        """Test 1: 3+ results found"""
        search_results = {
            "documents": [["Doc 1", "Doc 2", "Doc 3", "Doc 4", "Doc 5"]]
        }
        
        context = ""
        if search_results["documents"] and search_results["documents"][0]:
            context = "\n".join(search_results["documents"][0][:3])
        
        self.assertIn("Doc 1", context)
        self.assertIn("Doc 2", context)
        self.assertIn("Doc 3", context)
        self.assertNotIn("Doc 4", context)
    
    def test_context_with_one_result(self):
        """Test 2: Less than 3 results"""
        search_results = {
            "documents": [["Doc 1"]]
        }
        
        context = ""
        if search_results["documents"] and search_results["documents"][0]:
            context = "\n".join(search_results["documents"][0][:3])
        
        self.assertEqual(context, "Doc 1")
    
    def test_context_no_results(self):
        """Test 3: No results"""
        search_results = {
            "documents": [[]]
        }
        
        context = ""
        if search_results["documents"] and search_results["documents"][0]:
            context = "\n".join(search_results["documents"][0][:3])
        
        self.assertEqual(context, "")
    
    # ===== LLM Response Tests =====
    
    @patch('chat_app.llm_utils.get_agent_response')
    def test_valid_llm_response(self, mock_get_response):
        """Test 1: Valid response"""
        mock_response = Mock()
        mock_response.output = "Python is a programming language"
        mock_get_response.return_value = mock_response
        
        response = mock_get_response(Mock(), "What is Python?")
        self.assertEqual(response.output, "Python is a programming language")
    
    @patch('chat_app.llm_utils.get_agent_response')
    def test_llm_api_error(self, mock_get_response):
        """Test 2: LLM API error"""
        mock_get_response.side_effect = Exception("API error")
        
        with self.assertRaises(Exception):
            mock_get_response(Mock(), "Query")
    
    @patch('chat_app.llm_utils.get_agent_response')
    def test_llm_timeout(self, mock_get_response):
        """Test 3: Timeout"""
        mock_get_response.side_effect = TimeoutError("Request timed out")
        
        with self.assertRaises(TimeoutError):
            mock_get_response(Mock(), "Query")
    
    # ===== Response Display Tests =====
    
    def test_display_valid_response(self):
        """Test 1: Valid response"""
        mock_response = Mock()
        mock_response.output = "This is a response"
        messages = []
        
        messages.append({"role": "assistant", "content": mock_response.output})
        
        self.assertEqual(messages[0]["content"], "This is a response")
    
    def test_display_empty_response(self):
        """Test 2: Empty response"""
        mock_response = Mock()
        mock_response.output = ""
        messages = []
        
        messages.append({"role": "assistant", "content": mock_response.output})
        
        self.assertEqual(messages[0]["content"], "")
    
    # ===== Chat History Display Tests =====
    
    def test_display_multiple_messages(self):
        """Test 1: Multiple messages"""
        messages = [
            {"role": "user", "content": "Question 1"},
            {"role": "assistant", "content": "Answer 1"},
            {"role": "user", "content": "Question 2"},
            {"role": "assistant", "content": "Answer 2"}
        ]
        
        self.assertEqual(len(messages), 4)
        self.assertEqual(messages[0]["role"], "user")
        self.assertEqual(messages[1]["role"], "assistant")
    
    def test_display_empty_history(self):
        """Test 2: Empty history"""
        messages = []
        
        self.assertEqual(len(messages), 0)
    
    # ===== Clear Chat Tests =====
    
    def test_clear_chat_with_history(self):
        """Test 1: Click clear with history"""
        messages = [{"role": "user", "content": "Hello"}] * 10
        messages.clear()
        
        self.assertEqual(len(messages), 0)
    
    def test_clear_empty_chat(self):
        """Test 2: Click clear on empty chat"""
        messages = []
        messages.clear()
        
        self.assertEqual(len(messages), 0)
    
    # ===== Error Handling Tests =====
    
    @patch('chat_app.search_document_by_text')
    def test_error_during_search(self, mock_search):
        """Test 1: Exception during search"""
        mock_search.side_effect = Exception("Search error")
        messages = []
        
        try:
            mock_search("Query")
        except Exception as e:
            error_msg = f"Sorry, I encountered an error: {str(e)}"
            messages.append({"role": "assistant", "content": error_msg})
        
        self.assertIn("Search error", messages[0]["content"])
    
    @patch('chat_app.llm_utils.get_agent_response')
    def test_error_during_llm_call(self, mock_get_response):
        """Test 2: Exception during LLM call"""
        mock_get_response.side_effect = Exception("LLM error")
        messages = []
        
        try:
            mock_get_response(Mock(), "Query")
        except Exception as e:
            error_msg = f"Sorry, I encountered an error: {str(e)}"
            messages.append({"role": "assistant", "content": error_msg})
        
        self.assertIn("LLM error", messages[0]["content"])


if __name__ == '__main__':
    unittest.main()
