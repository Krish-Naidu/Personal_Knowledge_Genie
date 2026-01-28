import unittest
import os
import sys

# Add parent directory to path to import embedding_utils
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from embedding_utils import get_text_embedding
import llm_utils


class TestEmbeddingUtils(unittest.TestCase):
    """Simple unit tests for embedding_utils.py"""
    
    def test_1_simple_text_embedding(self):
        """Test 1: Generate embedding for simple text"""
        result = get_text_embedding("Hello, world!")
        # Should return a list
        self.assertIsInstance(result, list)
        # Should have 768 dimensions
        self.assertEqual(len(result), 768)
        # Should contain floats
        self.assertIsInstance(result[0], float)
    
    def test_2_longer_text_embedding(self):
        """Test 2: Generate embedding for longer text"""
        text = "This is a longer sentence with more words to test embedding generation."
        result = get_text_embedding(text)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 768)
    
    def test_3_empty_string_raises_error(self):
        """Test 3: Empty string should raise ValueError - Actual: Raised ValueError 'content cannot be empty'"""
        with self.assertRaises(ValueError):
            get_text_embedding("")
    
    def test_4_special_characters_embedding(self):
        """Test 4: Generate embedding with special characters"""
        result = get_text_embedding("Hello! @#$% 123 测试")
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 768)
    
    def test_5_very_long_text_raises_error(self):
        """Test 5: Very long text - Actual: content exceeds maximum length of 10,000 characters"""
        # Create text with 15000 characters
        long_text = "Lorem ipsum dolor sit amet. " * 600
        with self.assertRaises(Exception):  # Can be ValueError or other exception from API
            get_text_embedding(long_text)
    
    def test_6_no_api_key_raises_error(self):
        """Test 6: Missing API key should raise authentication error"""
        # Save current API key
        original_key = os.environ.get('GOOGLE_API_KEY')
        
        try:
            # Remove API key
            if 'GOOGLE_API_KEY' in os.environ:
                del os.environ['GOOGLE_API_KEY']
            
            # Should raise an error
            with self.assertRaises(Exception):
                get_text_embedding("Test text")
        finally:
            # Restore API key
            if original_key:
                os.environ['GOOGLE_API_KEY'] = original_key
    
    def test_7_none_input_raises_error(self):
        """Test 7: None input should raise ValueError"""
        with self.assertRaises(ValueError):
            get_text_embedding(None)


if __name__ == "__main__":
    unittest.main()
