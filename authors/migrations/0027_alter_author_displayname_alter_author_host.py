# Generated by Django 4.2.6 on 2023-11-15 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0026_alter_author_followers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='displayName',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='author',
            name='host',
            field=models.TextField(blank=True, null=True),
        ),
    ]
