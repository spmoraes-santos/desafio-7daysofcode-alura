# Image from python
FROM python:3.12-slim

# Define the directory where the project files will be copied
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install libraries from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script to the container
COPY . .

# Run the script
CMD ["python", "analysis_1.py"]
