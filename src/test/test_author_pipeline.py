import unittest
import requests
from unittest.mock import patch


class TestAuthorPipelineEndpoint(unittest.TestCase):
    base_url = "http://localhost:8000/author-pipeline"

    def test_success_pdf(self):
        """Test the endpoint with a PDF file that exists."""
        payload = {
            "file_path": "/path/to/book.pdf",
            "title": "My Book",
            "authors_ids": [1, 2],
            "book_summary": "This is a book about..."
        }
        with patch('os.path.exists', return_value=True), \
                patch('requests.get') as mocked_get:
            mocked_get.return_value.json.return_value = {
                "extracted_texts": [{"text": "Some text"}]}
            response = requests.post(self.base_url, json=payload)
            self.assertEqual(response.status_code, 200)
            self.assertIn('book_id', response.json())

    def test_file_not_found(self):
        """Test the endpoint with a file path that does not exist."""
        payload = {
            "file_path": "/path/to/nonexistent.pdf",
            "title": "Nonexistent Book",
            "authors_ids": [1],
            "book_summary": "This book does not exist."
        }
        with patch('os.path.exists', return_value=False):
            response = requests.post(self.base_url, json=payload)
            self.assertEqual(response.status_code, 404)
            self.assertIn('detail', response.json())
            self.assertEqual(
                response.json()['detail'], 'File not found. Please provide a valid file path.')

    def test_unsupported_file_format(self):
        """Test the endpoint with an unsupported file format."""
        payload = {
            "file_path": "/path/to/book.txt",
            "title": "Unsupported Format Book",
            "authors_ids": [3],
            "book_summary": "This is a book in txt format."
        }
        with patch('os.path.exists', return_value=True):
            response = requests.post(self.base_url, json=payload)
            self.assertEqual(response.status_code, 400)
            self.assertIn('detail', response.json())
            self.assertEqual(response.json()[
                             'detail'], 'Unsupported file format. Please provide a PDF or Word file.')

    def test_error_during_processing(self):
        """Test the endpoint when an error occurs during file processing."""
        payload = {
            "file_path": "/path/to/book.docx",
            "title": "Error Book",
            "authors_ids": [4],
            "book_summary": "This book causes an error."
        }
        with patch('os.path.exists', return_value=True), \
                patch('requests.get') as mocked_get, \
                patch('src.nlp.plagiarism_checker.builder.add_embeddings', side_effect=Exception("Test error")):
            mocked_get.return_value.json.return_value = {
                "extracted_texts": [{"text": "Error text"}]}
            response = requests.post(self.base_url, json=payload)
            self.assertEqual(response.status_code, 500)
            self.assertIn('detail', response.json())
            self.assertTrue("An error occurred" in response.json()['detail'])


if __name__ == '__main__':
    unittest.main()
