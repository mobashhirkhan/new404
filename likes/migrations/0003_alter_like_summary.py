# Generated by Django 4.2.6 on 2023-11-13 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('likes', '0002_like_type_alter_like_id_alter_like_summary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='summary',
            field=models.CharField(default='', max_length=255),
        ),
    ]
