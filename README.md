# EasySplit

EasySplit is a web application that simplifies bill splitting among friends or groups. It allows users to track shared expenses, split bills evenly or unequally, and settle debts easily within a group.

## Table of Contents

- [Features](#features)
- [Local Deployment](#local-deployment)
- [Production Deployment](#production-deployment)
- [References](#references)

## Features

- Create groups and invite friends to join.
- Add expenses and specify the participants.
- Split bills equally or unequally based on individual contributions.
- Keep track of individual balances and group expenses.

## Local Deployment

To deploy EasySplit locally using Docker Compose, follow these steps:

1. Make sure Docker and Docker Compose are installed on your machine.
    
2. Set the necessary environment variables in the .env file.

3. Build and start the containers using the `docker-compose-local.yml` file:

```shell
docker-compose -f docker-compose-local.yml up -d
```

Access the application at http://localhost:8000.

## Production Deployment

To deploy EasySplit in a production environment using Docker Compose, follow these steps:

1. Make sure Docker and Docker Compose are installed on your server.

2. Set the necessary environment variables in the .env file.

3. Build and start the containers using the `docker-compose.yml` file:

```shell
docker-compose up -d
```

Access the application using the appropriate domain or IP address.

## References

This project utilizes the following resources and libraries:
- [Django](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Swagger](https://swagger.io/tools/swagger-ui/)
- [Nginx](https://nginx.org/)
