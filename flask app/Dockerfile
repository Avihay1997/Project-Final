# Use official Python image as base
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the application files into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir flask

# Expose port 5000 for Flask
EXPOSE 5000

# Define the command to run the application
CMD ["python", "app.py"]
