# Use an official Python runtime as a parent image
FROM python:3.11.5

# Set environment variables for Python
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# All these next environment variables have placeholder values, that will be replaced when the Docker container is pushed to the Azure Web app.
# These placeholder values will be replaced by the Azure Web App's environment variables set up in its application settings.

# Database settings
#ENV DB_ENGINE='dbengine'
#ENV DB_NAME='dbname'
#ENV DB_USER='dbuser'
#ENV DB_PASSWORD='dbpassword'
#ENV DB_HOST='dbhost'
#ENV DB_PORT='dbport'

# Storage settings
#ENV DEFAULT_FILE_STORAGE='defaultfilestorage'
#ENV AZURE_ACCOUNT_NAME='azaccountname'
#ENV AZURE_ACCOUNT_KEY='azaccountkey'
#ENV AZURE_CONTAINER='azcontainer'

# Django settings
#ENV SECRET_KEY="your_secret_key"
#ENV DEBUG="your_debug_value"

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
#RUN python manage.py makemigrations website
#RUN python manage.py migrate


# Expose port 80, default HTTP port
EXPOSE 80

CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:80"]