#!/bin/bash
export `cat ./easysplit/.env`
docker exec -it $PROJECT_NAME bash