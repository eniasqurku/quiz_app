# Quiz app API

## Setup

- Activate virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

- Install requirements

```bash
pip install -r requirements.txt
```

- Create database by migrating

```
python manage.py migrate
```

- Load initial data

```
python manage.py loaddata groups.yaml
```

- You can now use the api by registering as creator or participant.
  If you want to create an admin user run:

```
python manage.py createsuperuser
```

- Finally run the server

```
python manage.py runserver localhost:8000
```

You can now access the api through http://localhost:8000/. For the admin interface go to http://localhost:8000/admin/

## Docs

You can find the api documentation on http://localhost:8000/doc/

## Testing

To run tests execute:

```
pytest
```


