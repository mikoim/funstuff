# API

## Getting started

```sh
# 1. start containers
docker-compose up -d --build

# 2. apply migrations
docker-compose exec app python manage.py migrate

# 3. run unit tests (option)
docker-compose exec app python -m unittest
```
