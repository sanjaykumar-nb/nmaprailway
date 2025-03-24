FROM python:3.12-slim

# Install required dependencies
RUN apt-get update && apt-get install -y nmap && apt-get clean

# Set working directory
WORKDIR /app

# Copy all project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Start the bot
CMD ["python", "main.py"]
