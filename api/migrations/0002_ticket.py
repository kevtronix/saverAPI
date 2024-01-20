# Generated by Django 5.0.1 on 2024-01-20 18:09

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_category', models.IntegerField(choices=[(0, 'Meats'), (1, 'Vegetables'), (2, 'Non-Perishables')], default=0)),
                ('expiration_date', models.DateField(default=datetime.date.today)),
                ('checked', models.BooleanField(default=False)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.restaurant')),
            ],
        ),
    ]