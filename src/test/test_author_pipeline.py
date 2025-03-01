import unittest
import requests
from unittest.mock import patch
import os
import json 



class TestAuthorPipelineEndpoint(unittest.TestCase):
    base_url = "https://da6b-45-240-51-111.ngrok-free.app/pipeline/author-pipeline"
    # base_url = "http://localhost:8000/pipeline/author-pipeline"
    cwd = os.getcwd()
    test_dir = os.path.join(cwd, 'src', 'test')

    def test_success_word(self):
        """Test the endpoint with a DOCX file that exists."""
        file_path = os.path.join(self.test_dir, 'arabic_word_doc.docx')
        arabic_book_title = "كتاب عربي"
        authors_uuids_list = ["1", "2"]  # Assuming authors_ids should be integers
        book_summary = "كتاب عربي يتحدث عن اللغة العربية."

        with open(file_path, 'rb') as f:
            files = {
                'file': (
                    os.path.basename(file_path),
                    f,
                    'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                )
            }
            data = {
                'title': arabic_book_title,
                'authors_ids': authors_uuids_list,
                'book_summary': book_summary
            }
            # Converting authors_uuids_list to string
            data_str = {key: str(value) if isinstance(
                value, list) else value for key, value in data.items()}

            response = requests.post(self.base_url, files=files, data=data_str)

        print(f"Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")

        try:
            response_json = response.json()
            print(response_json)
            self.assertEqual(response.status_code, 200)
            self.assertIn('book_id', response_json)
        except requests.exceptions.JSONDecodeError:
            print("Response is not in JSON format.")
            self.fail("Response is not in JSON format.")
    # def test_file_not_found(self):
    #     """This test should be updated to test an error scenario that can be captured, such as invalid file type."""
    #     arabic_book_title = "كتاب عربي"
    #     authors_uuids_list = [1, 2]  # Assuming authors_ids should be integers
    #     book_summary = "كتاب عربي يتحدث عن اللغة العربية."
    #     fake_file_path = os.path.join(self.test_dir, 'fake_file.xyz')

    #     with open(fake_file_path, 'wb') as f:  # Creating a fake file with unsupported format
    #         f.write(b"Dummy content")

    #     with open(fake_file_path, 'rb') as f:
    #         files = {'file': (os.path.basename(fake_file_path),
    #                           f, 'application/octet-stream')}
    #         data = {'title': arabic_book_title,
    #                 'authors_ids': authors_uuids_list, 'book_summary': book_summary}
    #         response = requests.post(self.base_url, files=files, data=data)

    #     os.remove(fake_file_path)  # Clean up the fake file
    #     self.assertEqual(response.status_code, 400)

    # def test_success_pdf(self):
    #     """Test the endpoint with a PDF file that exists."""
    #     file_path = os.path.join(self.test_dir, 'test_full_book.pdf')
    #     arabic_book_title = "كتاب عربي"
    #     authors_uuids_list = [1, 2]  # Assuming authors_ids should be integers
    #     book_summary = "كتاب عربي يتحدث عن اللغة العربية."

    #     with open(file_path, 'rb') as f:
    #         files = {'file': (os.path.basename(file_path), f, 'application/pdf')}
    #         data = {'title': arabic_book_title,
    #                 'authors_ids': authors_uuids_list, 'book_summary': book_summary}
    #         response = requests.post(self.base_url, files=files, data=data)

    #     print(response.json())
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn('book_id', response.json())

if __name__ == '__main__':
    unittest.main()