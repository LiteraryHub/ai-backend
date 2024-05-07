# Use the Bitnami PyTorch image as the base
FROM bitnami/pytorch:2.2.0

# Set the working directory to /code
WORKDIR /code

# Copy the requirements file into the container at /code
COPY ./requirements.txt /code/requirements.txt

# Install any needed packages specified in the requirements file
RUN pip install --no-cache-dir -r /code/requirements.txt

# Install Tesseract-OCR and its dependencies
RUN apt-get update && \
    apt-get install -y tesseract-ocr tesseract-ocr-ara

# Copy the current directory contents into the container at /code/src
COPY ./src /code/src

# Copy cache directory for Hugging Face Transformers within the /code directory
COPY ./.cache/ /code/.cache/

# Set NLTK_DATA and TESSERACT_CMD environment variables
ENV NLTK_DATA=/code/nltk_data \
    TESSERACT_CMD=/usr/bin/tesseract

# Create NLTK data directory
RUN mkdir -p $NLTK_DATA

# Expose port 8000 to the outside world.
EXPOSE 8000

# Command to run the application
CMD ["python", "-m", "uvicorn", "src.main:app", "--reload",  "--proxy-headers", "--host", "0.0.0.0", "--port", "8000", "--log-config=config/log_conf.yaml"]
