# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
# WORKDIR ./

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port the app runs on (update if necessary)
EXPOSE 8000

# Set the command to run the application (update as needed)
CMD ["python", "download_and_search.py"]
