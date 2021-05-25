#Dockerfile
FROM python:3.8-slim
# Python latest version docker image
RUN apt-get update -y
# Update the packages of the container
RUN apt-get install -y python-pip python-dev build-essential
# Install the required essentials in the container
COPY . /app
# Copy the current directory into the app folder in the container
WORKDIR /app
# Change the working directory to app folder
RUN pip install -r requirements.txt
# Install the requirements present in the requirements.txt file
ENTRYPOINT ["python"]
# Specify the entry point
CMD ["app.py"]
# Command file to execute