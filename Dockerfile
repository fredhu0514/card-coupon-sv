# Use the official Python image as the base image
FROM python:3.8.13

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose port 5000 for the Flask app to listen on
EXPOSE 5000

# Set the entrypoint command to run the Flask app
CMD ["python", "app.py"]
