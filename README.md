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

```shell
cp .env.example .env
```

3. (Optional) If you are using Apple M1 or iOS with the Apple M2 chip, you may need to modify the mariadb image version in the docker-compose-local.yml file. Comment out the existing image line and uncomment the image line for the appropriate version for your architecture:

```yaml
mariadb:
    # image: mariadb:11.0.2
    image: arm64v8/mariadb:11.0.2
```

4. Build and start the containers using the `docker-compose-local.yml` file:

```shell
docker-compose -f docker-compose-local.yml up -d
```

5. Migrate the database and create a superuser when building the project for the first time.:

```shell
docker exec -it easysplit python manage.py migrate

docker exec -it easysplit python manage.py createsuperuser
```

Now, you can login and see the swagger document on: http://localhost:8000/__hiddenswagger.

## Production Deployment

To deploy EasySplit in a production environment using Docker Compose, follow these steps:

1. Make sure Docker and Docker Compose are installed on your server.

2. Set the necessary environment variables in the .env file.

3. Build and start the containers using the `docker-compose.yml` file:

```shell
docker-compose up -d
```

4. Migrate the database and create a superuser when building the project for the first time.:

```shell
docker exec -it easysplit python manage.py migrate

docker exec -it easysplit python manage.py createsuperuser
```

Access the application using the appropriate domain or IP address.

## References

This project utilizes the following resources and libraries:
- [Django](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Swagger](https://swagger.io/tools/swagger-ui/)
- [Nginx](https://nginx.org/)
