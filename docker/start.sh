#!/bin/bash

# Start MySQL in the background
service mysql start

# Wait for MySQL to be ready
until mysqladmin ping -h 127.0.0.1 --silent; do
    echo "Waiting for MySQL to be ready..."
    sleep 2
done

# Run database migrations
python3 url_shortner_server/manage.py migrate

# Start the Django development server without the autoreloader
python3 url_shortner_server/manage.py runserver 0.0.0.0:8000 --noreload
