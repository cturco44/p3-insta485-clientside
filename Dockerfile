# Configuration for insta485 web server Docker image
#
# Andrew DeOrio <awdeorio@umich.edu>

# Use a minimal Python image as a parent image
FROM python:3.8.1-slim-buster

# Copy list of production requirements into Docker container
COPY requirements-prod.txt /tmp

# Install Python package requirements
RUN pip install -r /tmp/requirements-prod.txt

# Copy application into image
COPY dist/insta485-0.1.0.tar.gz /tmp

# Install Insta485 web app
RUN pip install /tmp/insta485-0.1.0.tar.gz

# Run the web server in the container
CMD gunicorn \
  --workers 4 \
  --bind 0.0.0.0:8000 \
  insta485:app
