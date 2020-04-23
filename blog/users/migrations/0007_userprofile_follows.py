# Generated by Django 2.2.3 on 2020-03-15 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20200306_2057'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='follows',
            field=models.ManyToManyField(related_name='follow', to='users.UserProfile'),
        ),
    ]
