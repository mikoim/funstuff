FROM python:3-alpine

RUN apk add --no-cache g++ gcc python3-dev mariadb-dev

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT ["python", "server.py"]

EXPOSE 3000
