# Generated by Django 5.1 on 2024-08-27 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('english', '0009_rename_text_correct_answer_key_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='correct_answer',
            name='index',
            field=models.IntegerField(null=True),
        ),
    ]
