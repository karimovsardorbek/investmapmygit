# Generated by Django 5.0.6 on 2024-09-05 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0036_alter_project_funding_goal'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='min_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True),
        ),
    ]
