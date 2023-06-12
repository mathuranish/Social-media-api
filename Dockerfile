# This is a multi-stage docker file

# Stage: 1
FROM python:3.9-slim-buster

# set env variable
ENV PYTHONUNBUFFERED=1

# Upgrade pip
RUN pip install --upgrade pip

# Install project dependencies
COPY requirements.txt /
RUN pip install -r requirements.txt

# Copy project code
COPY . /code/

# Set work directory
WORKDIR /code

# listen on this port
EXPOSE 8000

