# Use an official Python image from Docker Hub
FROM python:3.9-slim

# Install Tesseract and necessary libraries
RUN apt-get update && \
    apt-get install -y tesseract-ocr libtesseract-dev && \
    apt-get clean

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 for Flask
EXPOSE 5000

# Set Tesseract data environment variable
ENV TESSDATA_PREFIX="/usr/share/tesseract-ocr/4.00/tessdata/"

# Command to run the Flask app using gunicorn in the container
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
