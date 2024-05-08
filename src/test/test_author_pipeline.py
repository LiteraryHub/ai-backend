import unittest
import requests
from unittest.mock import patch
import os

class TestAuthorPipelineEndpoint(unittest.TestCase):
    base_url = "http://127.0.0.1:8000/pipeline/author-pipeline"
    cwd = os.getcwd()
    test_dir = os.path.join(cwd, 'src', 'test')

    def test_success_word(self):
        """Test the endpoint with a PDF file that exists."""
        file_path = os.path.join(self.test_dir, 'arabic_word_doc.docx')
        arabic_book_title = "كتاب عربي"
        authors_uuids_list = ["d1ee1723-daca-465f-b30f-ca46e07a57ba"]
        payload = {
            "file_path": file_path,
            "title": arabic_book_title,
            "authors_ids": authors_uuids_list,
            "book_summary": "كتاب عربي يتحدث عن اللغة العربية."
        }
        
        response = requests.post(self.base_url, json=payload)
        print(response.json())
        self.assertEqual(response.status_code, 200)
        self.assertIn('book_id', response.json())

    def test_file_not_found(self):
        """Test the endpoint with a file that does not exist."""
        file_path = os.path.join(self.test_dir, 'arabic_pdf_doc_no_exist.pdf')
        arabic_book_title = "كتاب عربي"
        authors_uuids_list = ["d1ee1723-daca-465f-b30f-ca46e07a57ba"]
        payload = {
            "file_path": file_path,
            "title": arabic_book_title,
            "authors_ids": authors_uuids_list,
            "book_summary": "كتاب عربي يتحدث عن اللغة العربية."
        }
        response = requests.post(self.base_url, json=payload)
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()