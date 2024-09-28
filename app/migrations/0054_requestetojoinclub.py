# Generated by Django 5.0.6 on 2024-09-12 07:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0053_alter_pitchdecksection_project'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequesteToJoinClub',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Approved', 'Approved'), ('Rejected', 'Rejected'), ('Created', 'Created')], default='Created', max_length=8)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.club')),
                ('investor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.investor')),
            ],
        ),
    ]
