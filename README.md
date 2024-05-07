# LiteraryHub - AI Backend README

Welcome to the README for the LiteraryHub AI backend, a component of the LiteraryHub platform. This document provides all the necessary details to get started with the AI backend development, testing, and deployment.

## API Definition

The backend API is defined using a Swagger interface. You can find the detailed API specification in the [literaryhub_swagger_file.yaml](./literaryhub_swagger_file.yaml) file.

### Overview

The LiteraryHub platform enables publishers to generate book covers and audio books. It also allows authors to update unpublished books in Word or PDF format. Additionally, the platform includes features for plagiarism detection and restricted topics detection.

### Recommended dev environment

Please use the following dev environment:

- Platform: linux-64
- Python: See the first line in `/Dockerfile`. Please consider creating a new,
  dedicated conda-based environment for using this repo in order to avoid depenedencies and
  constraints with python modules you don't need for this repo.
- IDE: VS Code
- Version control: git

### Installation

- Clone the repository:

  ```bash
  git clone https://github.com/LiteraryHub/ai-backend.git

  ```

- Navigate to the project directory:

  ```bash
  cd ai-backend

  ```

- Install dependencies using pip:

  ```bash
  pip install --user -r requirements.txt

  ```

### Run the FastAPI server to serve the AI backend API
- Run the FastAPI app:

  ```bash
  python -m uvicorn src.main:app --reload --proxy-headers --host 0.0.0.0 --port 8000 --log-config=config/log_conf.yaml
  ```

- Run the FastAPI app with vscode debugger:
    - Open the project in vscode
    - Navigate to the debug tab
    - Click on the play button to start the server

### Testing
- **Unit Tests**: The `src/test` directory contains unit tests for each group or endpoint, ensuring comprehensive test coverage.
    
To run the unit tests, navigate to the project's root directory in your terminal and run the following command:
```bash
python -m unittest discover -s src/test -p "*_test.py"
```


### Creating the docker image
Use the docker engine to build the image from current code:

This command will list details such as the image ID, repository, tag, and size for each image. It's useful for managing your Docker images, including removing old or unused ones to free up disk space.


Use the docker engine to create a docker container and run a particular image with image name:
```
docker build -t literaryhub_ai_backend_image:latest .
```

### Pushing the docker image to Docker Hub
After creating the image locally, you'll want to push it to Docker Hub as follows:

```bash
docker tag literaryhub_ai_backend_image:latest literaryhub/ai-backend:latest
docker push literaryhub/ai-backend:latest
```

### Running the docker image locally

Disclaimer: The host 0.0.0.0 specified in the Dockerfile does not accept connections locally.
In order to run the docker image locally, a local modification to the host specified in the Dockerfile
is necessary, to 127.0.0.1, but please do not submit this change because it is likely to break our
deployment process.

Use the docker engine to create a docker container and run a particular image:
```
sudo docker run -d -p 8000:8000 literaryhub_ai_backend_image:latest
```

To see all the containers that you have locally, run:

```
docker ps -a
```

To see what containers are current running, remove the `-a` parameter.

### Test The Docker Image with Python Script (using request python function)

- Make sure that docker image is running
- Run any test script in `src/test` directory which is contains unit tests for each group or endpoint, ensuring comprehensive test coverage.


Notes: 
- In order to see the logs on the container, use its Container ID, e.g.,
```
docker logs <container_id>
```

After a container has been created with the previous command, you can stop/start it using the commands:
```
docker start <container_id>
sudo docker end <container_id>
```
Note: you can't reuse the same container name multiple times, even if you're running the same image. 
