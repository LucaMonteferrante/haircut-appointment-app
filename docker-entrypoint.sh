#!/bin/sh

echo "Waiting for MySQL to be ready..."

until python -c "
import os
import mysql.connector
mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    port=int(os.getenv('DB_PORT')),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME')
)
print('MySQL is ready')
"; do
  echo "MySQL not ready yet, retrying in 2 seconds..."
  sleep 2
done

echo "Starting Flask app..."
python app.py