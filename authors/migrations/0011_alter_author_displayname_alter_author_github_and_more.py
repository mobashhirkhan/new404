# Generated by Django 4.2.6 on 2023-10-28 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0010_alter_author_is_staff_alter_author_is_superuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='displayName',
            field=models.CharField(blank=True, editable=False, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='author',
            name='github',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='author',
            name='host',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='author',
            name='url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
