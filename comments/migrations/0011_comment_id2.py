# Generated by Django 4.2.6 on 2023-12-05 09:35

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0010_alter_comment_origin'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='id2',
            field=models.TextField(default=uuid.uuid4, editable=False),
        ),
    ]
