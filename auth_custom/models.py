from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

MEMBERSHIP_GOLD = 'G'
MEMBERSHIP_SILVER = 'S'
MEMBERSHIP_BRONZE = 'B'

MEMBERSHIP = [
    (MEMBERSHIP_GOLD, 'Gold'),
    (MEMBERSHIP_SILVER, 'Silver'),
    (MEMBERSHIP_BRONZE, 'Bronze')
]


# custom the default user model
# to make this custom work, we need to set AUTH_USER_MODEL in tutorial/settings.py
# and change all the related code to this new custom user model by using django.contrib.auth.get_user_model()
class User(AbstractUser):
    email = models.EmailField(unique=True)


# external information for default "user" table of django
class UserProfile(models.Model):
    phone = models.IntegerField(null=True)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP, default=MEMBERSHIP_BRONZE)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
