
# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in docker
WORKDIR /q

# Copy the current directory contents into the container at /data_app
COPY . /q/task_app

COPY requirements.txt /q
COPY requirements-dev.txt /q

#CMD ["dir"]

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Specify the command to run on container start
CMD ["uvicorn", "task_app.main:app", "--host", "0.0.0.0", "--port", "8000"]
