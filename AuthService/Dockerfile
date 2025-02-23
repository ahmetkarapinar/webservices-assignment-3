# Use an official Python runtime as base image
# 1. Use a lightweight Python image
FROM python:3.9

# 2. Set the working directory inside the container
WORKDIR /app/AuthService

# 3. Copy only dependencies first (to leverage caching)
COPY requirements.txt .

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the entire application after installing dependencies
COPY . .

# 6. Expose the Flask app port
EXPOSE 5001

# 7. Define the default command to run the app
CMD ["python", "app.py"]