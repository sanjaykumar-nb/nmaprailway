# Use an official Python runtime as the base image
FROM python:3.10-slim

# Install Nmap (and other needed system packages)
RUN apt-get update && apt-get install -y nmap && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 (if needed; polling doesn't require HTTP exposure, but might be useful for logs)
EXPOSE 5000

# Start the bot using your main.py file
CMD ["python", "main.py"]
