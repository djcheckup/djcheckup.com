# DJ Checkup

## Intro

Source code for the [DJ Checkup website](https://djcheckup.com)

## Set up

- Clone the repository
- Create the virtual environment
- Pip install the requirements
- Create the .env file from the env.template (optional)
- Run the migrations

```bash
python manage.py migrate
```

- If creating a new database, create the super user

```bash
python manage.py createsuperuser
```

- Create the staticfiles folder

```bash
mkdir staticfiles
```

- Run the Collectstatic command

```bash
python manage.py collectstatic
```

- Run the server to get the website up

```bash
python manage.py runserver
```

- To submit URLS to be checked, you need a Redis server. Configure one in the .env file, or just run a local Redis Docker container for testing:

```bash
docker run --name local-redis -d redis
```

- Then run the Django-RQ worker in a second terminal window (make sure the same virtual environment is activated in the new window):

```bash
python manage.py rqworker checks
```
