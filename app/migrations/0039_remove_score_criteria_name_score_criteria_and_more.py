# Generated by Django 5.0.6 on 2024-09-06 07:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0038_alter_approvalhistory_date_of_action_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='score',
            name='criteria_name',
        ),
        migrations.AddField(
            model_name='score',
            name='criteria',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='app.criteria'),
        ),
        migrations.AlterField(
            model_name='bankmember',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_bank_members', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_bank_council_meeting', to=settings.AUTH_USER_MODEL),
        ),
    ]
