# Use the official Python image
FROM python:3.8

# Set the working directory inside the container
WORKDIR /app

# Install git to clone the repository
RUN apt-get update && apt-get install -y git

# Clone the repository
RUN git clone https://github.com/Rory-Thompson/Share-Market-Analysis /app

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Expose port 8050 for Dash
EXPOSE 8050

# Set the command to run your Dash app
CMD ["python", "/app/src/main.py"]