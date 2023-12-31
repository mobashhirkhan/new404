# Generated by Django 4.2.6 on 2023-10-30 19:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_posts', '0014_alter_apppost_contenttype'),
        ('comments', '0003_rename_text_comment_content_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='app_posts.apppost'),
        ),
    ]
