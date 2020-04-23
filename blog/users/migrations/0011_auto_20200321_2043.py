# Generated by Django 2.2.3 on 2020-03-21 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20200321_2034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='followers',
            field=models.ManyToManyField(related_name='followed_by', to='users.UserProfile'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='following',
            field=models.ManyToManyField(related_name='following_to', to='users.UserProfile'),
        ),
    ]
