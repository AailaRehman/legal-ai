FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for OCR and PDF
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-urd \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create data directories
RUN mkdir -p data/raw/pdfs data/vector_store data/processed

# Seed demo users
RUN python seed_users.py

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run
CMD ["streamlit", "run", "app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true", \
     "--browser.gatherUsageStats=false"]
