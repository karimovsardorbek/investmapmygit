# Generated by Django 5.0.6 on 2024-09-05 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0034_alter_company_logo_alter_investordocument_file_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='deadline',
        ),
        migrations.AddField(
            model_name='project',
            name='time_limit',
            field=models.PositiveIntegerField(default=10),
        ),
    ]
