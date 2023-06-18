#!/bin/bash
export `cat ./.env`
docker exec -it $PROJECT_NAME bash -c "python manage.py makemigrations && python manage.py migrate --noinput"