# Generated by Django 4.2.6 on 2023-10-23 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('host', models.CharField(max_length=255)),
                ('displayName', models.CharField(max_length=255)),
                ('url', models.CharField(max_length=255)),
                ('github', models.CharField(max_length=255)),
                ('profileImage', models.CharField(max_length=255)),
            ],
        ),
    ]
