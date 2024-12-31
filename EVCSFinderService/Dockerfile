# Stage 1: Base Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy necessary files
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose the Flask app port
EXPOSE 5000

# Set the entrypoint to run the Flask app
ENTRYPOINT ["python", "src/app.py"]
