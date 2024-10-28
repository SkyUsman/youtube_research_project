# Use the official Python image as a base
FROM python:3.11

# Install necessary dependencies
RUN apt-get update && \
    apt-get install -y curl gnupg2 unixodbc-dev && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/$(lsb_release -rs)/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Set the working directory in the container
WORKDIR /app

# Copy requirements and install
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Specify the command to run on container start
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
