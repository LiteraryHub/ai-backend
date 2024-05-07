import requests


def upload_file(url, file_path):
    # Open the file in binary mode
    with open(file_path, 'rb') as f:
        # Define the request files parameter
        files = {'file': (file_path, f)}
        # Send the POST request
        response = requests.post(url, files=files)
    return response


if __name__ == "__main__":
    # URL of the FastAPI endpoint
    url = 'http://127.0.0.1:8001/word-text-extractor/upload-word'
    # Path to your .docx file
    file_path = './src/test/arabic_word_doc.docx'

    # Call the function and get the response
    response = upload_file(url, file_path)

    # Print the status code and response data
    print(f"Status Code: {response.status_code}")
    print("Response Body:", response.json())
