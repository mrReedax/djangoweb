# Generated by Django 4.0.3 on 2022-04-18 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_alter_session_session_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='session_id',
            field=models.UUIDField(default='6e83030b279a4f05a5e8162e78061aad', primary_key=True, serialize=False),
        ),
    ]
