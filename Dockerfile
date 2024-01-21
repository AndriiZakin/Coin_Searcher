FROM python:3.11-slim-buster AS base

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set default environment variables
ENV BINANCE_API_KEY=default_api_key
ENV BINANCE_SECRET_KEY=default_secret_key

CMD ["python", "u", "main_search.py"]