# Quiz app API

## Setup

- In order to run the project locally you need to install **Docker** and **docker-compose**.
  Then run:

```bash
docker-compose up
```

You can now access the api through http://0.0.0.0:8000/. For the admin interface go to http://0.0.0.0:8000/admin/

## Docs

You can find the api documentation on http://0.0.0.0:8000/api/schema/swagger-ui/ or
http://0.0.0.0:8000/api/schema/redoc/

## Testing

To run the tests execute:

```
docker exec -it quiz_app_web_1 pytest
```


