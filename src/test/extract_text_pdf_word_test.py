import unittest
import requests
import os

class TestDocumentProcessingAPI(unittest.TestCase):
    # Base URL of the running FastAPI application
    BASE_URL = "http://127.0.0.1:8000"
    cwd = os.getcwd()
    test_dir = os.path.join(cwd, 'src', 'test')

    def test_pdf_extraction(self):
        """Test PDF extraction endpoint with a given file path."""
        # Assuming the server expects a local file path query
        file_path = os.path.join(self.test_dir, 'arabic_pdf_doc.pdf')
        response = requests.get(f"{self.BASE_URL}/extractor/extract-text-pdf", params={"file_path": file_path})
        self.assertEqual(response.status_code, 200)
        self.assertIn('extracted_texts', response.json())
        print(len(response.json()['extracted_texts']))

    def test_word_extraction(self):
        """Test Word extraction endpoint with a given file path."""
        file_path = os.path.join(self.test_dir, 'arabic_word_doc.docx')
        response = requests.get(f"{self.BASE_URL}/extractor/extract-text-word", params={"file_path": file_path})
        self.assertEqual(response.status_code, 200)
        self.assertIn('extracted_texts', response.json())
        print(response.json())

    def test_invalid_pdf_request(self):
        """Test PDF extraction with an invalid file path."""
        file_path = '/path/to/nonexistent/document.pdf'
        response = requests.get(f"{self.BASE_URL}/extractor/extract-text-pdf", params={"file_path": file_path})
        # Assuming 400 is returned for invalid input
        self.assertEqual(response.status_code, 400)

    def test_invalid_word_request(self):
        """Test Word extraction with an invalid file path."""
        file_path = '/path/to/nonexistent/document.docx'
        response = requests.get(f"{self.BASE_URL}/extractor/extract-text-word", params={"file_path": file_path})
        # Assuming 400 is returned for invalid input
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
