# Generated by Django 5.1 on 2024-08-27 11:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('english', '0008_remove_sentence_sentence_sentence_correct_sentence_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='correct_answer',
            old_name='text',
            new_name='key',
        ),
        migrations.RenameField(
            model_name='wrong_answer',
            old_name='text',
            new_name='key',
        ),
    ]
