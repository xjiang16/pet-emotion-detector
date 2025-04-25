# Use a lightweight base image with Python 3.10
FROM python:3.10-slim

# Set working directory
WORKDIR /app
COPY . .

# Install system dependencies (opencv needs these)
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy project files into the container
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port if you're using Flask's default
EXPOSE 5000

# Command to run your app
CMD ["python3", "app.py"]
