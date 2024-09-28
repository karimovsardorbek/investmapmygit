# Generated by Django 5.0.6 on 2024-09-20 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0067_glossary_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_uz', models.CharField(max_length=500)),
                ('title_ru', models.CharField(max_length=500)),
                ('title_en', models.CharField(max_length=500)),
                ('description_uz', models.TextField(blank=True, null=True)),
                ('description_ru', models.TextField(blank=True, null=True)),
                ('description_en', models.TextField(blank=True, null=True)),
                ('file_uz', models.FileField(blank=True, null=True, upload_to='reports/uz/')),
                ('file_ru', models.FileField(blank=True, null=True, upload_to='reports/ru/')),
                ('file_en', models.FileField(blank=True, null=True, upload_to='reports/en/')),
                ('image', models.ImageField(blank=True, null=True, upload_to='reports/images/')),
                ('category', models.CharField(choices=[('agritech', 'Agritech'), ('annual', 'Annual'), ('case_study', 'Case Study'), ('cleantech', 'Cleantech'), ('consumer_internet', 'Consumer Internet'), ('consumer_services', 'Consumer Services'), ('d2c', 'D2C'), ('deeptech', 'DeepTech'), ('ecommerce', 'Ecommerce'), ('edtech', 'Edtech'), ('electric_vehicle', 'Electric Vehicle'), ('enterprisetech', 'Enterprisetech'), ('financials', 'Financials'), ('fintech', 'Fintech'), ('foodtech', 'Foodtech'), ('gaming', 'Gaming'), ('healthtech', 'Healthtech'), ('insurtech', 'Insurtech'), ('internet', 'Internet'), ('ipo', 'IPO'), ('media_entertainment', 'Media & Entertainment'), ('ott', 'OTT'), ('quarterly', 'Quarterly'), ('saas', 'SaaS'), ('sentiment', 'Sentiment'), ('startup_ecosystem', 'Startup Ecosystem'), ('super_apps', 'Super Apps'), ('survey', 'Survey'), ('unicorns', 'Unicorns'), ('venture_capital', 'Venture Capital'), ('vertical_marketplace', 'Vertical Marketplace'), ('web3', 'Web3')], max_length=50)),
                ('industry', models.CharField(choices=[('startup_ecosystem', 'Startup Ecosystem'), ('ecommerce', 'Ecommerce'), ('fintech', 'Fintech'), ('deeptech', 'DeepTech')], max_length=50)),
                ('report_type', models.CharField(choices=[('ecosystem_report', 'Ecosystem Report'), ('funding_report', 'Funding Report'), ('index_report', 'Index Report'), ('ipo_report', 'IPO Report'), ('sector_report', 'Sector Report')], max_length=50)),
                ('publish_date', models.DateField()),
                ('page_count', models.IntegerField()),
            ],
        ),
    ]
