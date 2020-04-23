# Generated by Django 2.2.3 on 2020-03-21 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20200321_2017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='followers',
            field=models.ManyToManyField(related_name='_userprofile_followers_+', to='users.UserProfile'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='following',
            field=models.ManyToManyField(related_name='_userprofile_following_+', to='users.UserProfile'),
        ),
    ]
