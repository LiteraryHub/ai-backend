from sentence_transformers import SentenceTransformer
from concurrent.futures import ThreadPoolExecutor

# Load the sentence transformer model
model = SentenceTransformer('medmediani/Arabic-KW-Mdel')

# Function to compute embedding for a single text
def embed_text(item):
    """
    Embeds the text of an item using a pre-trained model.

    Args:
        item (dict): A dictionary containing the text to be embedded.

    Returns:
        dict: The input dictionary with an additional "embedding" key, which contains the embedded representation of the text.
    """
    embedding = model.encode(item["text"], convert_to_tensor=False)
    item["embedding"] = embedding.tolist()
    return item

# Function to add embeddings to a list of JSON objects
def add_embeddings(json_input):
    """
    Add embeddings to the extracted texts in the given JSON input.

    Args:
        json_input (dict): The JSON input containing the extracted texts.

    Returns:
        dict: The updated JSON input with embeddings added to the extracted texts.
    """
    # Extract texts from JSON objects
    paragraphs = [item for item in json_input["extracted_texts"]]

    # Use ThreadPoolExecutor to compute embeddings in parallel
    with ThreadPoolExecutor() as executor:
        update_items = list(executor.map(embed_text, paragraphs))

    json_input["extracted_texts"] = update_items
    return json_input


if __name__ == "__main__":
    # Example JSON input
    json_input = {
        "extracted_texts": [
            {"page_number": 1, "paragraph_index": 1, "text": "أهلاً وسهلاً"},
            {"page_number": 1, "paragraph_index": 2, "text": "مرحباً"},
        ]
    }

    # Add embeddings to the extracted texts
    json_output = add_embeddings(json_input)

    # display cosine similarity between the two paragraphs embeddings
    from sklearn.metrics.pairwise import cosine_similarity
    emb1 = json_output["extracted_texts"][0]["embedding"]
    emb2 = json_output["extracted_texts"][1]["embedding"]
    similarity = cosine_similarity([emb1], [emb2])[0][0]
    print(f"Cosine similarity between the two paragraphs: {similarity}")