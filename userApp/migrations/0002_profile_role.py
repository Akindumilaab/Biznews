# Generated by Django 3.2.25 on 2024-09-26 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='role',
            field=models.CharField(choices=[('admin', 'admin'), ('staff', 'staff'), ('user', 'user')], default='user', max_length=12),
        ),
    ]