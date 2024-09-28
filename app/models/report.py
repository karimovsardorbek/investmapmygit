from django.db import models

class Report(models.Model):
    # Updated Category options (English only)
    CATEGORY_CHOICES = [
        ('agritech', 'Agritech'),
        ('annual', 'Annual'),
        ('case_study', 'Case Study'),
        ('cleantech', 'Cleantech'),
        ('consumer_internet', 'Consumer Internet'),
        ('consumer_services', 'Consumer Services'),
        ('d2c', 'D2C'),
        ('deeptech', 'DeepTech'),
        ('ecommerce', 'Ecommerce'),
        ('edtech', 'Edtech'),
        ('electric_vehicle', 'Electric Vehicle'),
        ('enterprisetech', 'Enterprisetech'),
        ('financials', 'Financials'),
        ('fintech', 'Fintech'),
        ('foodtech', 'Foodtech'),
        ('gaming', 'Gaming'),
        ('healthtech', 'Healthtech'),
        ('insurtech', 'Insurtech'),
        ('internet', 'Internet'),
        ('ipo', 'IPO'),
        ('media_entertainment', 'Media & Entertainment'),
        ('ott', 'OTT'),
        ('quarterly', 'Quarterly'),
        ('saas', 'SaaS'),
        ('sentiment', 'Sentiment'),
        ('startup_ecosystem', 'Startup Ecosystem'),
        ('super_apps', 'Super Apps'),
        ('survey', 'Survey'),
        ('unicorns', 'Unicorns'),
        ('venture_capital', 'Venture Capital'),
        ('vertical_marketplace', 'Vertical Marketplace'),
        ('web3', 'Web3'),
    ]

    # Industry and Report Type options remain unchanged
    INDUSTRY_CHOICES = [
        ('startup_ecosystem', 'Startup Ecosystem'),
        ('ecommerce', 'Ecommerce'),
        ('fintech', 'Fintech'),
        ('deeptech', 'DeepTech'),
    ]

    REPORT_TYPE_CHOICES = [
        ('ecosystem_report', 'Ecosystem Report'),
        ('funding_report', 'Funding Report'),
        ('index_report', 'Index Report'),
        ('ipo_report', 'IPO Report'),
        ('sector_report', 'Sector Report'),
    ]

    # Titles, descriptions, files, and image
    title_uz = models.CharField(max_length=500)
    title_ru = models.CharField(max_length=500)
    title_en = models.CharField(max_length=500)
    
    description_uz = models.TextField(blank=True, null=True)
    description_ru = models.TextField(blank=True, null=True)
    description_en = models.TextField(blank=True, null=True)

    file_uz = models.FileField(upload_to='reports/uz/', blank=True, null=True)
    file_ru = models.FileField(upload_to='reports/ru/', blank=True, null=True)
    file_en = models.FileField(upload_to='reports/en/', blank=True, null=True)

    image = models.ImageField(upload_to='reports/images/', blank=True, null=True)

    # Updated category field
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    industry = models.CharField(max_length=50, choices=INDUSTRY_CHOICES)
    report_type = models.CharField(max_length=50, choices=REPORT_TYPE_CHOICES)

    publish_date = models.DateField()
    page_count = models.IntegerField()

    def get_title(self, language_code):
        return getattr(self, f'title_{language_code}', self.title_en)  # Default to English

    def get_description(self, language_code):
        return getattr(self, f'description_{language_code}', self.description_en)  # Default to English

    def get_file(self, language_code):
        return getattr(self, f'file_{language_code}', self.file_en)  # Default to English file

    def __str__(self):
        return self.title_en  # Default to English display
