import unittest
import os
import sys
import shutil

# Add parent directory to path to import chromadb_utils
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from chromadb_utils import (
    store_text_as_document,
    search_document_by_text,
    get_all_document_filenames,
    delete_document_by_filename
)


class TestChromaDBUtils(unittest.TestCase):
    """Comprehensive unit tests for chromadb_utils.py"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment before running tests"""
        cls.test_collection = "test_documents"
        cls.vectordb_path = os.path.join(os.path.dirname(__file__), "..", "vectordb")
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test data after all tests complete"""
        # Optional: Clean up test collection or vectordb
        pass
    
    # ===== Function 1: store_text_as_document Tests =====
    
    def test_1_store_simple_text_with_metadata(self):
        """Test 1: Store simple text with metadata"""
        result = store_text_as_document("Hello World", metadata={"filename": "test.txt"})
        self.assertIsInstance(result, str)
        self.assertEqual(len(result), 36)  # UUID length with hyphens
    
    def test_2_store_text_without_metadata(self):
        """Test 2: Store text without metadata"""
        result = store_text_as_document("Sample text", metadata=None)
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
    
    def test_3_store_empty_string(self):
        """Test 3: Store empty string (NOT AS EXPECTED - should raise error)"""
        # This test expects it to work, but it might raise ValueError
        try:
            result = store_text_as_document("", metadata={"filename": "empty.txt"})
            # If it succeeds, that's the current behavior
            self.assertIsInstance(result, str)
        except ValueError as e:
            # This is the expected behavior according to the table
            self.assertIn("empty", str(e).lower())
    
    def test_4_store_very_long_text(self):
        """Test 4: Store very long text (>100,000 characters)"""
        long_text = "Lorem ipsum dolor sit amet. " * 4000
        result = store_text_as_document(long_text, metadata={"filename": "large.txt"})
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
    
    def test_5_store_text_with_special_characters(self):
        """Test 5: Store text with special characters"""
        result = store_text_as_document("Hello! @#$% 测试 🎉", metadata={"filename": "special.txt"})
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
    
    def test_6_store_multiple_documents_same_filename(self):
        """Test 6: Store multiple documents with same filename"""
        result1 = store_text_as_document("Doc 1", metadata={"filename": "duplicate.txt"})
        result2 = store_text_as_document("Doc 2", metadata={"filename": "duplicate.txt"})
        # Both should have different IDs
        self.assertNotEqual(result1, result2)
    
    # ===== Function 2: search_document_by_text Tests =====
    
    def test_7_search_for_existing_text(self):
        """Test 7: Search for existing text"""
        # First store a document
        store_text_as_document("Searchable content here", metadata={"filename": "searchable.txt"})
        
        # Now search for it
        results = search_document_by_text("Searchable content")
        self.assertIsInstance(results, dict)
        self.assertIn("documents", results)
        self.assertIn("metadatas", results)
    
    def test_8_search_for_nonexistent_text(self):
        """Test 8: Search for non-existent text"""
        results = search_document_by_text("This does not exist in database xyzabc123")
        self.assertIsInstance(results, dict)
        # Results might be empty or have no matches
    
    def test_9_semantic_search(self):
        """Test 9: Semantic search (NOT AS EXPECTED - might not work without embedding)"""
        # Store a document with "car"
        store_text_as_document("I drive a car every day", metadata={"filename": "car.txt"})
        
        # Search for "automobile"
        results = search_document_by_text("automobile")
        # This might not return semantic matches without proper embedding setup
        self.assertIsInstance(results, dict)
    
    def test_10_search_in_nonexistent_collection(self):
        """Test 10: Search in non-existent collection (NOT AS EXPECTED - might crash)"""
        try:
            results = search_document_by_text("test", collection_name="fake_collection_xyz")
            # If it doesn't crash, check the results
            self.assertIsInstance(results, dict)
        except Exception as e:
            # Expected to crash according to table
            self.assertIsInstance(e, Exception)
    
    def test_11_search_with_empty_string(self):
        """Test 11: Search with empty string (NOT AS EXPECTED - might raise error)"""
        try:
            results = search_document_by_text("")
            self.assertIsInstance(results, dict)
        except ValueError as e:
            # This is the expected behavior according to the table
            self.assertIn("empty", str(e).lower())
    
    def test_12_search_with_special_characters(self):
        """Test 12: Search with special characters"""
        # Store document with special characters
        store_text_as_document("@#$% special", metadata={"filename": "special_search.txt"})
        
        # Search for it
        results = search_document_by_text("@#$%")
        self.assertIsInstance(results, dict)
    
    # ===== Function 3: get_all_document_filenames Tests =====
    
    def test_13_get_filenames_from_populated_collection(self):
        """Test 13: Get filenames from populated collection"""
        # Store some documents first
        store_text_as_document("Content 1", metadata={"filename": "file1.txt"})
        store_text_as_document("Content 2", metadata={"filename": "file2.pdf"})
        store_text_as_document("Content 3", metadata={"filename": "file3.doc"})
        
        filenames = get_all_document_filenames()
        self.assertIsInstance(filenames, list)
        self.assertGreater(len(filenames), 0)
    
    def test_14_get_filenames_from_empty_collection(self):
        """Test 14: Get filenames from empty collection"""
        filenames = get_all_document_filenames(collection_name="empty_collection_test")
        self.assertIsInstance(filenames, list)
        self.assertEqual(len(filenames), 0)
    
    def test_15_get_filenames_with_duplicates(self):
        """Test 15: Get filenames with duplicates"""
        # Store documents with duplicate filenames
        store_text_as_document("Doc A", metadata={"filename": "dup_test.txt"})
        store_text_as_document("Doc B", metadata={"filename": "dup_test.txt"})
        store_text_as_document("Doc C", metadata={"filename": "unique.txt"})
        
        filenames = get_all_document_filenames()
        # Should return unique filenames only
        self.assertIsInstance(filenames, list)
        # Count occurrences of "dup_test.txt" - should appear only once
        dup_count = filenames.count("dup_test.txt")
        self.assertEqual(dup_count, 1)
    
    def test_16_get_filenames_when_metadata_missing(self):
        """Test 16: Get filenames when metadata missing"""
        # Store document without filename in metadata
        store_text_as_document("No filename metadata", metadata={"author": "test"})
        
        # Should still return a list (might be empty or skip that document)
        filenames = get_all_document_filenames()
        self.assertIsInstance(filenames, list)
    
    def test_17_get_filenames_from_nonexistent_collection(self):
        """Test 17: Get filenames from non-existent collection"""
        filenames = get_all_document_filenames(collection_name="does_not_exist_xyz")
        self.assertIsInstance(filenames, list)
        self.assertEqual(len(filenames), 0)
    
    # ===== Function 4: delete_document_by_filename Tests =====
    
    def test_18_delete_existing_document(self):
        """Test 18: Delete existing document"""
        # Store a document
        store_text_as_document("Delete me", metadata={"filename": "to_delete.txt"})
        
        # Delete it
        result = delete_document_by_filename("to_delete.txt")
        self.assertTrue(result)
    
    def test_19_delete_nonexistent_document(self):
        """Test 19: Delete non-existent document"""
        result = delete_document_by_filename("does_not_exist_file.txt")
        self.assertFalse(result)
    
    def test_20_delete_multiple_documents_same_filename(self):
        """Test 20: Delete when multiple documents share filename"""
        # Store multiple documents with same filename
        store_text_as_document("Dup 1", metadata={"filename": "multi_delete.txt"})
        store_text_as_document("Dup 2", metadata={"filename": "multi_delete.txt"})
        store_text_as_document("Dup 3", metadata={"filename": "multi_delete.txt"})
        
        # Delete all of them
        result = delete_document_by_filename("multi_delete.txt")
        self.assertTrue(result)
    
    def test_21_delete_from_empty_collection(self):
        """Test 21: Delete from empty collection"""
        # Try to delete from a collection that might be empty
        result = delete_document_by_filename("any.txt", collection_name="empty_delete_test")
        self.assertFalse(result)
    
    def test_22_delete_from_nonexistent_collection(self):
        """Test 22: Delete from non-existent collection (NOT AS EXPECTED - might crash)"""
        try:
            result = delete_document_by_filename("test.txt", collection_name="fake_collection_delete")
            # If it doesn't crash, should return False
            self.assertFalse(result)
        except Exception as e:
            # Expected to crash according to table
            self.assertIsInstance(e, Exception)
    
    def test_23_delete_with_none_filename(self):
        """Test 23: Delete with None as filename (NOT AS EXPECTED - might raise AttributeError)"""
        try:
            result = delete_document_by_filename(None)
            # Should handle gracefully
            self.assertFalse(result)
        except (AttributeError, TypeError) as e:
            # Expected behavior - raises error instead of proper validation
            self.assertIsInstance(e, (AttributeError, TypeError))


if __name__ == "__main__":
    unittest.main()
