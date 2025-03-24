# Python run-time for the image; slim for smaller size.
FROM python:3.11.4-slim

# Set working dir.
WORKDIR /app

# Copy requirements to leverage layer caching.
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code.
COPY . .

# Export the port the Flask app runs on.
EXPOSE 5000

# Command to run the flask app.
CMD ["python", "run.py"]
