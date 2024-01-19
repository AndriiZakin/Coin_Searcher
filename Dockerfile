FROM python:3.11-slim-buster AS base

WORKDIR /app

COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
# (This is optional and depends on your specific application)
# EXPOSE 80

# Define environment variable for running Python in unbuffered mode
ENV PYTHONUNBUFFERED 1

# Run app.py when the container launches
CMD ["python", "src/main.py"]
