# Generated by Django 4.1.1 on 2022-10-11 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_mailingmessage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('telegram_id', models.BigIntegerField(primary_key=True, serialize=False, unique=True)),
            ],
        ),
    ]