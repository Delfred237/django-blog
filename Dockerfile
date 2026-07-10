# Use an official Python runtime as a parent image
FROM python:3.13-slim-trixie

# Prevent Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Ensure Python output is sent straight to the terminal
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Copy entrypoint
COPY entrypoint.sh /entrypoint.sh

# Make it executable
RUN chmod +x /entrypoint.sh

# Create a non-root user
RUN useradd -m django && \
    chown -R django:django /app

USER django

# Expose the Django port
EXPOSE 8000

# Start the development server
ENTRYPOINT ["/entrypoint.sh"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]