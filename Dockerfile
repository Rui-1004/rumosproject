# Use an official Python runtime as a parent image
FROM python:3.11.5

# Set environment variables for Python
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# All these next environment variables have placeholder values, that will be replaced when the Docker container is pushed to the Azure Web app.
# These placeholder values will be replaced by the Azure Web App's environment variables set up in its application settings.

# Database settings
ENV DB_ENGINE="your_db_engine"
ENV DB_NAME="your_db_name"
ENV DB_USER="your_db_user"
ENV DB_PASSWORD="your_db_password"
ENV DB_HOST="your_db_host"
ENV DB_PORT="your_db_port"

# Django settings
ENV SECRET_KEY="your_secret_key"
ENV DEBUG="your_debug_value"

# Create and set the working directory
WORKDIR /rumosproject

# Copy the requirements file into the container
COPY requirements.txt .

# Install pip and any needed dependencies in requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . .

# Expose port 80, default HTTP port
EXPOSE 80

CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:80"]