from django.db.models.signals import post_save
from django.dispatch import receiver

from auth_custom.models import UserProfile
from snippets.signals import order_created
from tutorial import settings


# signals is a feature of django (similar as observer in Magento2)
# which can use to write custom code before or after the main function is called
# it support pre_save, post_save, pre_delete, post_delete
# to use this, we need to import this in auth_custom/apps.py AuthCustomConfig.ready() function


# to register signal, we need 2 step.
# step 1: create snippets/signals/__init__.py and define the name of register signal
# step 2: call that register signal from somewhere, for example, snippets/serializers.py CreateOrderSerializer.save()


# default signal of django
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile_whenever_user_created(sender, **kwargs):
    if kwargs['created']:
        UserProfile.objects.create(user=kwargs['instance'])


# custom signal that we registered previously
@receiver(order_created)
def test_register_signal(sender, **kwargs):
    print(kwargs['order'])
