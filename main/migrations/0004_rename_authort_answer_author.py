# Generated by Django 4.0.6 on 2022-07-26 00:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_answer_authort'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='authort',
            new_name='author',
        ),
    ]
