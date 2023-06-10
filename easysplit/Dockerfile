FROM python:3.8.5
LABEL maintainer rex.ultra
ENV PYTHONUNBUFFERED 1
RUN mkdir /project
RUN apt-get -y update && apt-get install -y vim

WORKDIR /project
COPY . /project
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
RUN chmod a+x docker-entrypoint.sh
