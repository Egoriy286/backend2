# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose port 5050
EXPOSE 5050

# Specify the command to run your application with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5050"]
