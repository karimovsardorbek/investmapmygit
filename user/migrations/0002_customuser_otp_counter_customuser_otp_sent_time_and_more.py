# Generated by Django 5.0.6 on 2024-08-14 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='otp_counter',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='customuser',
            name='otp_sent_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='otp_tried',
            field=models.BooleanField(default=False),
        ),
    ]
