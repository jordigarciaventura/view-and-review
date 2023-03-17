# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10-slim

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install python packages
RUN pip install poetry

# Copy only requirements to cache them in docker layer
WORKDIR /app
COPY poetry* pyproject* /app/

# Project initialization
RUN poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-ansi

# Copy files
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# File wsgi.py was not found. Please enter the Python path to wsgi file.
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "pythonPath.to.wsgi"]