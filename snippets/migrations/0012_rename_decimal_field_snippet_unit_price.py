# Generated by Django 4.1.6 on 2023-03-03 09:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0011_alter_snippettag_snippet'),
    ]

    operations = [
        migrations.RenameField(
            model_name='snippet',
            old_name='decimal_field',
            new_name='unit_price',
        ),
    ]