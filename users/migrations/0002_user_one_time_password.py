# Generated by Django 5.0.4 on 2024-06-01 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='one_time_password',
            field=models.CharField(default='', max_length=64),
        ),
    ]
