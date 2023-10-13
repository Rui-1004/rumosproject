# Use an official Python runtime as a parent image
FROM python:3.11.5

# Set environment variables for Python
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# All these next environment variables have placeholder values, that will be replaced when the Docker container is pushed to the Azure Web app.
# These placeholder values will be replaced by the Azure Web App's environment variables set up in its application settings.

# Database build arguments
ARG DB_ENGINE
ARG DB_NAME
ARG DB_USER
ARG DB_PASSWORD
ARG DB_HOST
ARG DB_PORT

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

# Apply database migrations
RUN python manage.py migrate

# Create a superuser
RUN echo "from django.contrib.auth.models import User; User.objects.create_superuser('$SUPERUSER_USERNAME', '$SUPERUSER_EMAIL', '$SUPERUSER_PASSWORD')" | python manage.py shell

# Expose port 80, default HTTP port
EXPOSE 80

CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:80"]   