# Generated by Django 5.0.6 on 2024-08-21 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_news'),
    ]

    operations = [
        migrations.RenameField(
            model_name='news',
            old_name='content',
            new_name='content_uz',
        ),
        migrations.RenameField(
            model_name='news',
            old_name='title',
            new_name='title_uz',
        ),
        migrations.RenameField(
            model_name='testimonial',
            old_name='comment',
            new_name='comment_uz',
        ),
        migrations.RenameField(
            model_name='testimonial',
            old_name='title',
            new_name='title_uz',
        ),
        migrations.AddField(
            model_name='news',
            name='content_eng',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='news',
            name='content_ru',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='news',
            name='title_eng',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='news',
            name='title_ru',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='testimonial',
            name='comment_eng',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='testimonial',
            name='comment_ru',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='testimonial',
            name='title_eng',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='testimonial',
            name='title_ru',
            field=models.CharField(default='', max_length=255),
        ),
    ]
