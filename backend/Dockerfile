# Use Python 3.9 slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create assets directory
RUN mkdir -p /app/assets

# Copy assets
COPY assets/* /app/assets/


# Set environment variables
ENV PORT=8080

# Expose port
EXPOSE 8080

# Run the application
CMD ["python", "init.py"]
