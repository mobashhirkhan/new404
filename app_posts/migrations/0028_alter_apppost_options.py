# Generated by Django 4.2.6 on 2023-11-15 07:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_posts', '0027_apppost_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='apppost',
            options={'ordering': ['-published']},
        ),
    ]
