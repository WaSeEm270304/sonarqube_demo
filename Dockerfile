
# Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy only required files
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy source code
COPY src/ src/

# Expose port
EXPOSE 8000

# Command to run FastAPI
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
