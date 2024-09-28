from django.db import models

class CompanyInfo(models.Model):
    # Basic Company Info
    name = models.CharField(max_length=255)
    sector = models.CharField(max_length=100)  # E.g., Ecommerce, Fintech
    founded_year = models.IntegerField()
    headquarters = models.CharField(max_length=255, null=True, blank=True)

    # Founders and Investors
    founders = models.TextField(null=True, blank=True)  # Comma-separated names of founders
    country = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    number_of_investors = models.IntegerField(default=0)

    # Financial Info
    amount_raised = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    amount_raised_currency = models.CharField(max_length=10, default="USD")
    company_type = models.CharField(max_length=100, null=True, blank=True)  # Funded, Public, etc.
    last_funding_type = models.CharField(max_length=100, null=True, blank=True)  # Series A, Debt Financing, etc.
    last_funding_stage = models.CharField(max_length=100, null=True, blank=True)  # Seed, Growth, Late Stage, etc.
    ipo_status = models.CharField(max_length=20, null=True, blank=True)  # Public or Private
    number_of_employees = models.IntegerField(null=True, blank=True)

    # Social Links
    website = models.URLField(null=True, blank=True)
    facebook_url = models.URLField(null=True, blank=True)
    linkedin_url = models.URLField(null=True, blank=True)
    twitter_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name



class Funding(models.Model):
    LAST_STAGE_CHOICES = [
        ('seed', 'Seed Stage'),
        ('bridge', 'Bridge Stage'),
        ('growth', 'Growth Stage'),
        ('late', 'Late Stage'),
        ('undisclosed', 'Undisclosed'),
    ]

    company = models.ForeignKey('CompanyInfo', related_name='funding_rounds', on_delete=models.CASCADE, null=True, blank=True)
    
    # Amount and Funding Round Details
    amount_raised = models.DecimalField(max_digits=15, decimal_places=2)  # Increased to accommodate large values
    currency = models.CharField(max_length=10, default="USD")  # To store the currency used (e.g., USD, INR)
    round_type = models.CharField(max_length=100)  # E.g., Secondary Market, Private Equity Round, Series A
    number_of_investors = models.IntegerField(default=0)  # Number of investors in the funding round
    announced_date = models.DateField()  # Date when the funding was announced
    last_funding_stage = models.CharField(max_length=50, choices=LAST_STAGE_CHOICES, default='undisclosed')  # Last funding stage

    def __str__(self):
        return f"{self.company.name} - {self.round_type} ({self.amount_raised} {self.currency})"



class CompanyInvestment(models.Model):
    company = models.ForeignKey('CompanyInfo', related_name='investments', on_delete=models.CASCADE, null=True, blank=True)
    portfolio_company = models.CharField(max_length=255)  # The name of the company Flipkart invested in
    sector = models.CharField(max_length=100, null=True, blank=True)  # Sector of the portfolio company
    stage = models.CharField(max_length=100)  # Seed, Series A, Growth, etc.
    amount_invested = models.DecimalField(max_digits=12, decimal_places=2)
    date_announced = models.DateField()

    def __str__(self):
        return f"{self.company.name} invested in {self.portfolio_company} - {self.stage}"



class Acquisition(models.Model):
    company = models.ForeignKey('CompanyInfo', related_name='acquisitions', on_delete=models.CASCADE, null=True, blank=True)
    acquired_company = models.CharField(max_length=255)  # Name of the company acquired
    sector = models.CharField(max_length=100, null=True, blank=True)  # Sector of the acquired company (e.g., Healthtech)
    acquisition_date = models.DateField()
    acquisition_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)  # Price, if disclosed

    def __str__(self):
        return f"{self.company.name} acquired {self.acquired_company}"



class Financials(models.Model):
    company = models.ForeignKey('CompanyInfo', related_name='financials', on_delete=models.CASCADE, null=True, blank=True)
    year = models.IntegerField()

    # Revenue and Profit Metrics
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2)
    total_expenses = models.DecimalField(max_digits=12, decimal_places=2)
    profit_before_tax = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    profit_after_tax = models.DecimalField(max_digits=12, decimal_places=2)

    # Balance Sheet Metrics
    total_assets = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    total_liabilities = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    equity_share_capital = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    current_liabilities = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    non_current_liabilities = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    # Cash Flow Metrics
    cash_flow_operating = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    cash_flow_investing = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    cash_flow_financing = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    cash_balance = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    # Financial Ratios
    net_profit_margin = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    return_on_assets = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    current_ratio = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    debt_equity_ratio = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.company.name} - Financials {self.year}"


class Story(models.Model):
    company = models.ForeignKey('CompanyInfo', related_name='stories', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255)  # Title of the story/news article
    author = models.CharField(max_length=100, null=True, blank=True)  # Author of the story
    date_published = models.DateField()
    url = models.URLField()  # Link to the full story

    def __str__(self):
        return f"{self.company.name} - {self.title}"