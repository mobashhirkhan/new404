# Generated by Django 4.2.6 on 2023-12-05 08:49

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('app_posts', '0037_apppost_friends_to_notify'),
    ]

    operations = [
        migrations.AddField(
            model_name='apppost',
            name='id2',
            field=models.TextField(default=uuid.uuid4, editable=False),
        ),
    ]
