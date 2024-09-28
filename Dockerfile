FROM python:3.10-alpine

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Create a folder.
RUN mkdir -p /home/user

ENV HOME=/home/user
ENV APP_HOME=/home/user/web

WORKDIR ${APP_HOME}

# Install build dependencies in a single RUN command
RUN apk update && \
    apk add --no-cache postgresql-dev gcc python3-dev musl-dev zlib zlib-dev jpeg-dev bash

# Upgrade pip
RUN pip install --upgrade pip

# Install a specific package to debug further
RUN pip install --no-cache-dir psycopg2-binary

# Copy requirements file and install remaining dependencies
COPY ./requirements.txt ${APP_HOME}/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt --ignore-installed

# Copy project files
COPY . ${APP_HOME}

# Create the directory for static files
RUN mkdir -p ${APP_HOME}/static
RUN mkdir -p ${APP_HOME}/staticfiles


# Copy wait-for-it script and ensure it is executable
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# Copy entrypoint.sh script and ensure it is executable
COPY entrypoint.sh /home/user/web/entrypoint.sh
RUN chmod +x /home/user/web/entrypoint.sh

# Expose the port
EXPOSE 8000

# Run the entrypoint script
ENTRYPOINT [ "/wait-for-it.sh", "db:5432", "--", "/home/user/web/entrypoint.sh" ]
