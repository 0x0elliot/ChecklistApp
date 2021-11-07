#!/bin/bash

echo "Starting backend API"

python3 db_check.py
python3 manager.py db upgrade
exec python3 manager.py runserver