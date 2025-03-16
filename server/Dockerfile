# Use a lightweight Python image
FROM python:3.11-slim

# Set environment variables to prevent Python from writing .pyc files and buffering output
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y default-jdk-headless && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /DeepContext
WORKDIR /DeepContext/server

# Copy only requirements.txt first for efficient caching
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . . 

# Install the application in editable mode
WORKDIR /DeepContext/server/src
RUN pip install --no-cache-dir -e .

WORKDIR /DeepContext

# Expose Flask default port
EXPOSE 5000

# Command to run the Flask app with Gunicorn
CMD ["flask", "--app", "deepcontext", "run", "--host=0.0.0.0", "--port=5000"]
