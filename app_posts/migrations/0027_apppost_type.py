# Generated by Django 4.2.6 on 2023-11-13 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_posts', '0026_alter_apppost_comment_count_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='apppost',
            name='type',
            field=models.CharField(default='Post', editable=False, max_length=200),
        ),
    ]
