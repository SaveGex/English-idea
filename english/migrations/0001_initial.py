# Generated by Django 5.1 on 2024-08-17 18:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Model_Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=50, verbose_name='name_post')),
                ('comment', models.CharField(max_length=500)),
                ('sentence', models.TextField(default=None)),
                ('publish_date', models.DateTimeField(default=datetime.datetime(2024, 8, 17, 18, 44, 13, 206671, tzinfo=datetime.timezone.utc))),
            ],
        ),
    ]
