# Generated by Django 4.2.6 on 2023-10-29 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_posts', '0010_alter_apppost_contenttype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apppost',
            name='contentType',
            field=models.CharField(choices=[('plain', 'plain'), ('markdown', 'markdown')], default=('plain', 'plain'), max_length=10),
        ),
        migrations.AlterField(
            model_name='apppost',
            name='visibility',
            field=models.CharField(choices=[('PUBLIC', 'PUBLIC'), ('FRIENDS', 'FRIENDS'), ('PRIVATE', 'PRIVATE')], default=('PUBLIC', 'PUBLIC'), max_length=10),
        ),
    ]
