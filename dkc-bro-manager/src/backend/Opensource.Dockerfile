FROM python:3.10

# Copy needed code into image
ADD ./app /app
ADD ./alembic /alembic
COPY ./start.sh /start.sh
COPY ./scripts /scripts

# Install pip 23.3.1
# RUN python -m pip install pip==23.3.1

# Install dependencies
RUN pip3 install -r app/requirements.txt

# Expose ports
EXPOSE 8000:8000

# Set python path
ENV PYTHONPATH="$PYTHONPATH:/"