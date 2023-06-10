#!/bin/bash
export `cat ./easysplit/.env`
docker exec -it $PROJECT_NAME bash -c "python manage.py makemigrations && python manage.py migrate --noinput"