# Generated by Django 4.2.6 on 2023-12-05 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_posts', '0038_apppost_id2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apppost',
            name='id2',
            field=models.TextField(editable=False, null=True),
        ),
    ]