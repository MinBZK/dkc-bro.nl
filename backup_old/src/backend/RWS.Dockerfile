FROM python:3.10

# Copy needed code into image
ADD ./app /app
ADD ./alembic /alembic

# Install dependencies
RUN pip3 install -r app/requirements.txt

# Expose ports
EXPOSE 8000:8000

# Set python path
ENV PYTHONPATH="$PYTHONPATH:/"
