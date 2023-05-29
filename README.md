# This project is to practice django by using rest_framework

### This project follow by this tutorial:
`https://www.django-rest-framework.org/tutorial/quickstart/`

### For db, we can use sqlite or postgres (currently, this project based on postgres)

### First of all, you need to run this command to create environment for this project
`cd project_name`

`python3 -m venv venv`

`source venv/bin/activate`

`pip install -r requirements.txt`

### If you don't have db yet, please follow this instruction:
`sudo -i -u postgres psql`

`CREATE DATABASE django_tutorial_rest_framework;`

`CREATE USER fudo4 WITH PASSWORD 'admin123';`

`GRANT ALL PRIVILEGES ON DATABASE django_tutorial_rest_framework TO fudo4;`

### Then you need to config db info by:
### In tutorial/settings.py file, find `DATABASES` variable and setting postgresdb based on it
### After that, run this command to migrate database
`python3 manage.py migrate`

### Now, you need to create a new user:
`python3 manage.py createsuperuser`
### Run server:
`python3 manage.py runserver`
### After finished, you can go to home page `127.0.0.1/8000` to try login

### Now, you are good to go
### Other information i've comment in the code
### Try to read it to know how to use this api project

### ----------------------------------------------------------------------------------------------

# Additional knowledge:

## Signals:

### signals is a feature of django (similar as observer in Magento2)
### which can use to `write custom code before or after the main function is called`
### it support `pre_save, post_save, pre_delete, post_delete`
### you can read about it in `auth_custom/signals/handler.py`

### ----------------------------------------------------------------------------------------------

# Notes:

### Whenever we create new project for django, we need to override the "user" model first, even if we gonna use it or not

### Or else, when we override it later when the project already run, it gonna cause an error:

### `admin.0001_initial is applied before its dependency app.0001_initial on database 'default'`

### To solve this error, we must drop the database, and that's not good, so we need to prevent that situation

### Please check module "auth_custom" for more information

### ----------------------------------------------------------------------------------------------

### For authenticate, we use jwt of "djoser"

### Setup by 2 steps:
### https://djoser.readthedocs.io/en/latest/getting_started.html
### https://djoser.readthedocs.io/en/latest/authentication_backends.html#json-web-token-authentication

### After that, we could use "permission" to check authenticate
### You can check in file:
### `snippets/views.py`

### ----------------------------------------------------------------------------------------------

### We can create serializer for a field which doesn't exist in the model
### Please check:
`snippets/serializers.py class CreateOrderSerializer()`

### After that, we can override the response if we don't comfortable with that
### Please check:
`snippets/views.py OrderViewSet.create()`

### ----------------------------------------------------------------------------------------------
