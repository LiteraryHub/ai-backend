from transformers import pipeline

def generate_summary(text):
    """
    Generate a summary of the given text using the Hugging Face transformers library.

    Parameters:
    - text (str): The input text to be summarized.

    Returns:
    - str: The generated summary.

    Example:
    summary = generate_summary("This is a long piece of text that needs summarization.")
    print(f"Generated Summary: {summary}")

    This function takes an input text and generates a summary using a pre-trained model from the Hugging Face transformers library.
    The generated summary is returned as a string.

    The summarization process is performed by initializing a summarization pipeline using a pre-trained model.
    The pipeline is then used to generate a summary of the input text based on certain length constraints.

    The generated summary is extracted from the result and returned as the output of the function.

    Note: The summarization model used in this function is "Falconsai/text_summarization".
    """

    # Initialize a summarization pipeline using a pre-trained model.
    summarizer = pipeline("summarization", model="Falconsai/text_summarization")

    # Generate a summary of the input text using the pipeline.
    result = summarizer(text, max_length=77, min_length=30, do_sample=False)

    # Extract the summary text from the result and return it.
    return result[0]['summary_text']