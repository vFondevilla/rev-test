# Use an official Python runtime as the parent image
FROM python:3.9-slim-buster

# Set the working directory in the docker
WORKDIR /usr/src/app

COPY requirements.txt ./
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . .


# Specify the command to run on container start
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]