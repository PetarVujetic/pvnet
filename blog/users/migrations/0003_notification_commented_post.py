# Generated by Django 3.0.8 on 2020-08-11 13:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('entries', '0001_initial'),
        ('users', '0002_notification_notification_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='commented_post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='entries.Entry'),
        ),
    ]