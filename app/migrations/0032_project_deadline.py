# Generated by Django 5.0.6 on 2024-09-05 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0031_project_project_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='deadline',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
