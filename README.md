# DJ Checkup

## Intro

Source code for the [DJ Checkup website](https://djcheckup.com)

## Set up

- Clone the repository
- Create the virtual environment
- Pip install the requirements
- Create the .env file from the env.template
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

- Run the server

```bash
python manage.py runserver
```
