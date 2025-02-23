FROM python:3.9

# Set working directory for the URL Shortener service
WORKDIR /app/URLShortenerService

# Copy only dependencies first for caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose service port
EXPOSE 5000

# Start the service
CMD ["python", "run.py"]