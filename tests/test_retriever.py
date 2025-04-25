# tests/test_retriever.py
import unittest
import os
import shutil
from agents.retriever import SECRetriever

class TestSECRetriever(unittest.TestCase):
    
    def setUp(self):
        # Create a test directory
        self.test_output_dir = "test_data/filings"
        os.makedirs(self.test_output_dir, exist_ok=True)
        self.retriever = SECRetriever(output_dir=self.test_output_dir)
    
    def tearDown(self):
        # Clean up test directory
        if os.path.exists("test_data"):
            shutil.rmtree("test_data")
    
    def test_get_cik(self):
        # Test retrieval of CIK for a known ticker
        cik = self.retriever._get_cik("AAPL")
        self.assertIsNotNone(cik)
        self.assertTrue(cik.isdigit())
    
    def test_invalid_ticker(self):
        # Test handling of invalid ticker
        cik = self.retriever._get_cik("INVALIDTICKER12345")
        self.assertIsNone(cik)

if __name__ == "__main__":
    unittest.main()
