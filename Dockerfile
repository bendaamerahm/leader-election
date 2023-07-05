FROM python:3.9-alpine

# Set the working directory
WORKDIR /app

# Copy the Python files into the container
COPY main.py k8s_client.py ./

# Install additional dependencies from requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Set the command to run the Python script
CMD ["python", "main.py"]
