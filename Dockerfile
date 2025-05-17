# Use official Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy API code and requirements
COPY ./app ./app

# Install dependencies
RUN pip install --no-cache-dir -r ./app/requirements.txt

# Copy your local .pkl model if you want to package it directly (optional)
# COPY ./models/wine_quality_model.pkl ./wine_quality_model.pkl

# Expose API on port 8000
EXPOSE 8000

# Run FastAPI app with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]

