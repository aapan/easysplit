#!/bin/bash
export `cat ./easysplit/.env`
echo "$@";
docker exec -it $PROJECT_NAME bash -c "python manage.py `echo "$@"`"