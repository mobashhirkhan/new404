# Generated by Django 4.2.6 on 2023-11-16 00:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_posts', '0028_alter_apppost_options'),
        ('comments', '0005_comment_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-published']},
        ),
        migrations.AddField(
            model_name='comment',
            name='contentMarkdown',
            field=models.TextField(default='', editable=False),
        ),
        migrations.AddField(
            model_name='comment',
            name='contentPlain',
            field=models.TextField(default='', editable=False),
        ),
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='comment',
            name='contentType',
            field=models.CharField(choices=[('plain', 'plain'), ('markdown', 'markdown')], default=('plain', 'plain'), max_length=20),
        ),
        migrations.AlterField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_posts.apppost'),
        ),
    ]
