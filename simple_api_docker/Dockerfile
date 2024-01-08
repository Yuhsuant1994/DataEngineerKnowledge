# Use an official Python 3.9 runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy the current directory contents into the container at /app
COPY ./backend /app
COPY pyproject.toml poetry.lock* /app/

# Disable virtualenvs created by Poetry
RUN poetry config virtualenvs.create false

# Install dependencies using Poetry
RUN poetry install --no-dev --no-interaction --no-ansi

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
