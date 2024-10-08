# Generated by Django 5.0.6 on 2024-09-05 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0016_alter_role_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='name',
            field=models.CharField(choices=[('regular', 'Regular User'), ('company', 'Company'), ('investor', 'Investor'), ('moderator', 'Moderator'), ('bank_secretary', 'Bank Secretary'), ('bank_council', 'Bank Council')], max_length=50, unique=True),
        ),
    ]
