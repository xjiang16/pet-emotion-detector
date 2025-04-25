# Pet Emotion Detector

We hosted the model on AWS, you can host it yourself on your local machine!

## Clone the Repository
```bash
# Clone the repository
git clone https://github.com/yourusername/pet-emotion-detector
cd pet-emotion-detector
```

## Option 1: Run with Docker (Recommended)

```bash
# Build the image
docker build -t pet-emotion-app .

# Run the app
docker run -p 5000:5000 pet-emotion-app

# Visit website!
Visit http://localhost:5000 in your browser
```

## Option 2: Run with Python

```bash
# Setup an virtual environment
python3.10 -m venv petenv
source petenv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run the app
python3 app.py

# Visit website!
Visit http://localhost:5000 in your browser
```
