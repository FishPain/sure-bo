# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Install curl
RUN apt-get update && apt-get install -y curl

# Copy the requirements.txt file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# download random forest model
ARG ASSET_NAME=rf.pkl
ARG LOCAL_FILENAME=src/models/${ASSET_NAME}
RUN curl -LJO https://github.com/FishPain/sure-bo/releases/download/v0.1.0/${ASSET_NAME}
RUN if [ ! -d /app/src/models ]; then mkdir -p /app/src/models; fi
RUN mv ${ASSET_NAME} ${LOCAL_FILENAME} \
    && ls -lh ${LOCAL_FILENAME} \
    && echo "File downloaded successfully."
    
# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
CMD ["python", "app.py"]
