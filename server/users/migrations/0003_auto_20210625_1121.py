# Generated by Django 3.2.4 on 2021-06-25 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_profile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='matches_lost',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='matches_won',
            field=models.PositiveIntegerField(default=0),
        ),
    ]