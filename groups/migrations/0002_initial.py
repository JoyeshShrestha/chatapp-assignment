# Generated by Django 4.2.5 on 2023-10-03 14:37

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('groups', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='groups',
            name='members',
            field=models.ManyToManyField(related_name='group', to=settings.AUTH_USER_MODEL),
        ),
    ]
