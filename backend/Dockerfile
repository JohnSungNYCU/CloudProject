# Use an official Python runtime as a parent image
FROM python:3.11.5

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt update && apt install -y default-libmysqlclient-dev gcc

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN python manage.py migrate
RUN python manage.py init_sys
RUN python manage.py init_wf
RUN python manage.py init_ticket
RUN python manage.py init_leave
# RUN ./init.sh
# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run manage.py when the container launches
CMD ["python", "manage.py", "runserver"]
