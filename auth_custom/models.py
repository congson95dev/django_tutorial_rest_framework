from django.contrib.auth.models import AbstractUser
from django.db import models


# custom the default user model
# to make this custom work, we need to set AUTH_USER_MODEL in tutorial/settings.py
# and change all the related code to this new custom user model by using django.contrib.auth.get_user_model()
class User(AbstractUser):
    email = models.EmailField(unique=True)
