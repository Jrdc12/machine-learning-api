# Start with a minimal base image of Python 3
FROM python:3.9-alpine

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the working directory
COPY . .

# Expose the port that the application will listen on
EXPOSE 5000

# Set the command to start the application
CMD ["python", "app.py"]
