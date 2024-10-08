# Generated by Django 5.0.6 on 2024-08-20 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_project_temporary'),
    ]

    operations = [
        migrations.CreateModel(
            name='Statistics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('investor_count', models.PositiveIntegerField(default=0)),
                ('project_count', models.PositiveIntegerField(default=0)),
                ('description', models.TextField()),
                ('value', models.IntegerField()),
            ],
        ),
    ]
