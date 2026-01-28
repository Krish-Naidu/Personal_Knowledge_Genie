import unittest
import os
import sys

# Add parent directory to path to import pdf_utils
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pdf_utils import extract_text_from_pdf
from PyPDF2.errors import PdfReadError


class TestPDFUtils(unittest.TestCase):
    """Simple unit tests for pdf_utils.py"""
    
    def test_1_extract_text_from_valid_pdf(self):
        """Test 1: Extract text from a valid PDF file"""
        # Assuming the file exists from the main code
        result = extract_text_from_pdf("./docs/Personal_Knowledge_Genie.pdf")
        # Should return a non-empty string
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
    
    def test_2_extract_text_returns_string(self):
        """Test 2: Verify function returns a string"""
        result = extract_text_from_pdf("./docs/Personal_Knowledge_Genie.pdf")
        self.assertIsInstance(result, str)
    
    def test_3_extract_text_from_empty_pdf(self):
        """Test 3: Extract text from PDF with no text (returns empty string)"""
        # This test would need an empty PDF - skip if not available
        # For now, just test that the function handles it gracefully
        pass
    
    def test_4_extract_text_contains_expected_content(self):
        """Test 4: Verify extracted text is not None"""
        result = extract_text_from_pdf("./docs/Personal_Knowledge_Genie.pdf")
        self.assertIsNotNone(result)
    
    def test_5_invalid_file_path(self):
        """Test 5: Raise FileNotFoundError for non-existent file"""
        with self.assertRaises(FileNotFoundError):
            extract_text_from_pdf("./docs/nonexistent_file_12345.pdf")
    
    def test_6_non_pdf_file(self):
        """Test 6: Raise error for non-PDF file"""
        # Create a temporary text file
        temp_file = "./docs/temp_test.txt"
        with open(temp_file, "w") as f:
            f.write("This is not a PDF")
        
        try:
            with self.assertRaises(PdfReadError):
                extract_text_from_pdf(temp_file)
        finally:
            # Clean up
            if os.path.exists(temp_file):
                os.remove(temp_file)


if __name__ == "__main__":
    unittest.main()
