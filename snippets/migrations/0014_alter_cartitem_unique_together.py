# Generated by Django 4.1.6 on 2023-03-07 03:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0013_cart_cartitem'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cartitem',
            unique_together=set(),
        ),
    ]