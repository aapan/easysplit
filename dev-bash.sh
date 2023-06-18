#!/bin/bash
export `cat ./.env`
docker exec -it $PROJECT_NAME bash