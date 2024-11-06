# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install gunicorn
RUN pip install --no-cache-dir gunicorn

# Copy the current directory contents into the container
COPY . .

# Create a directory for the SQLite database
RUN mkdir -p /app/db

# Set PYTHONPATH so all modules are accessible
ENV PYTHONPATH=/app

# Expose the port on which the app will run
EXPOSE 5000

# Run the Gunicorn server with the Flask app
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]