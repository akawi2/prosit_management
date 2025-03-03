# Use the official Python image from Docker Hub
FROM python:3.12.4

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt /app/

# Install the dependencies
RUN pip install -r requirements.txt

RUN python manage.py collectstatic --noinput

# Copy the entire project
COPY . /app/
    
# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]