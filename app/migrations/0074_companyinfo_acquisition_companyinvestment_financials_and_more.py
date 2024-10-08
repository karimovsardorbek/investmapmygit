# Generated by Django 5.0.6 on 2024-09-27 09:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0073_investment_investment_type_alter_investment_stage'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('sector', models.CharField(max_length=100)),
                ('founded_year', models.IntegerField()),
                ('headquarters', models.CharField(blank=True, max_length=255, null=True)),
                ('founders', models.TextField(blank=True, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
                ('number_of_investors', models.IntegerField(default=0)),
                ('amount_raised', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('amount_raised_currency', models.CharField(default='USD', max_length=10)),
                ('company_type', models.CharField(blank=True, max_length=100, null=True)),
                ('last_funding_type', models.CharField(blank=True, max_length=100, null=True)),
                ('last_funding_stage', models.CharField(blank=True, max_length=100, null=True)),
                ('ipo_status', models.CharField(blank=True, max_length=20, null=True)),
                ('number_of_employees', models.IntegerField(blank=True, null=True)),
                ('website', models.URLField(blank=True, null=True)),
                ('facebook_url', models.URLField(blank=True, null=True)),
                ('linkedin_url', models.URLField(blank=True, null=True)),
                ('twitter_url', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Acquisition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acquired_company', models.CharField(max_length=255)),
                ('sector', models.CharField(blank=True, max_length=100, null=True)),
                ('acquisition_date', models.DateField()),
                ('acquisition_price', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='acquisitions', to='app.company')),
            ],
        ),
        migrations.CreateModel(
            name='CompanyInvestment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('portfolio_company', models.CharField(max_length=255)),
                ('sector', models.CharField(blank=True, max_length=100, null=True)),
                ('stage', models.CharField(max_length=100)),
                ('amount_invested', models.DecimalField(decimal_places=2, max_digits=12)),
                ('date_announced', models.DateField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='investments', to='app.company')),
            ],
        ),
        migrations.CreateModel(
            name='Financials',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('total_revenue', models.DecimalField(decimal_places=2, max_digits=12)),
                ('total_expenses', models.DecimalField(decimal_places=2, max_digits=12)),
                ('profit_before_tax', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('profit_after_tax', models.DecimalField(decimal_places=2, max_digits=12)),
                ('total_assets', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('total_liabilities', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('equity_share_capital', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('current_liabilities', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('non_current_liabilities', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('cash_flow_operating', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('cash_flow_investing', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('cash_flow_financing', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('cash_balance', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('net_profit_margin', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('return_on_assets', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('current_ratio', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('debt_equity_ratio', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='financials', to='app.company')),
            ],
        ),
        migrations.CreateModel(
            name='Funding',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_raised', models.DecimalField(decimal_places=2, max_digits=15)),
                ('currency', models.CharField(default='USD', max_length=10)),
                ('round_type', models.CharField(max_length=100)),
                ('number_of_investors', models.IntegerField(default=0)),
                ('announced_date', models.DateField()),
                ('last_funding_stage', models.CharField(choices=[('seed', 'Seed Stage'), ('bridge', 'Bridge Stage'), ('growth', 'Growth Stage'), ('late', 'Late Stage'), ('undisclosed', 'Undisclosed')], default='undisclosed', max_length=50)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='funding_rounds', to='app.company')),
            ],
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('author', models.CharField(blank=True, max_length=100, null=True)),
                ('date_published', models.DateField()),
                ('url', models.URLField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stories', to='app.company')),
            ],
        ),
    ]
