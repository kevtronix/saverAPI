# Generated by Django 5.0.1 on 2024-01-28 02:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_rename_fufilled_shelterrequest_fulfilled'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shelterrequest',
            old_name='quantiy_requested',
            new_name='quantity_requested',
        ),
    ]
