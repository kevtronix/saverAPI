# Generated by Django 5.0.1 on 2024-01-28 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_rename_quantiy_requested_shelterrequest_quantity_requested'),
    ]

    operations = [
        migrations.AddField(
            model_name='shelterrequest',
            name='delivered',
            field=models.BooleanField(default=False),
        ),
    ]
