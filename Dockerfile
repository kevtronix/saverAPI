# Use official Python runtime as base image
FROM python:latest

# Set Enviorment Variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONNUNBUFFERED 1

# Set the working directory in the container
WORKDIR /usr/src/app

# Install Dependancies 
COPY  requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Copy the current directory contents into the container at /usr/src/app
COPY . /usr/src/app


# Run app.py when the container launches
CMD ["gunicorn" , "-b", "0.0.0:8000", "food_saver.wsgi:application"]