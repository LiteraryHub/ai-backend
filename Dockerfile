# For more details: https://hub.docker.com/r/bitnami/pytorch/
# The latest version of bitnami/pytorch is 2.2.0 in the time of writing this Dockerfile (2-17-2024).
FROM bitnami/pytorch:2.2.0


# Set the working directory to /code
WORKDIR /code

# Copy the requirements file into the container at /code
COPY ./requirements.txt /code/requirements.txt

# Install any needed packages specified in the resolved requirements file
RUN pip install --no-cache-dir -r /code/requirements.txt

# Copy the current directory contents into the container at /code/src
COPY ./src /code/src

# Copy cache directory for Hugging Face Transformers within the /code directory
COPY ./.cache/ /code/.cache/

# Set NLTK_DATA environment variable to a writable directory
ENV NLTK_DATA=/code/nltk_data

# Create NLTK data directory
RUN mkdir -p $NLTK_DATA

# Expose port 8000 to the outside world.
EXPOSE 8000

# Run the application
CMD ["python", "-m", "uvicorn", "src.main:app", "--reload",  "--proxy-headers", "--host", "0.0.0.0", "--port", "8000", "--log-config=config/log_conf.yaml"]
