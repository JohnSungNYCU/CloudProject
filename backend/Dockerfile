# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y default-libmysqlclient-dev netcat-traditional

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./wait-for-db.sh /app
RUN chmod +x /app/wait-for-db.sh

EXPOSE 8000

# Run manage.py when the container launches
# CMD ["python", "manage.py", "runserver"]
