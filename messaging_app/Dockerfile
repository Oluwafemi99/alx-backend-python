# Use Python 3.10 base image
FROM python:3.10

# Set working directory inside container
WORKDIR /app:

# Copy requirements and install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire messaging_app code
COPY . .

# Expose Django's default port
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
