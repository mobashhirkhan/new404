# Generated by Django 4.2.6 on 2023-12-08 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_posts', '0039_alter_apppost_id2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apppost',
            name='unlisted',
            field=models.BooleanField(default=False),
        ),
    ]
