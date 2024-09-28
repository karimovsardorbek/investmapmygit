from django.db import models
from user.models import CustomUser

class InvestmentCompany(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="investment_company")
    company_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    date_founded = models.DateField(null=True, blank=True)
    headquarters = models.CharField(max_length=255, null=True, blank=True)

    total_investments = models.IntegerField(default=0)
    number_of_exits = models.IntegerField(default=0)
    number_of_portfolio_organizations = models.IntegerField(default=0)
    total_portfolio_value = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    # Company profile data
    sectors = models.CharField(max_length=255, blank=True, null=True)  # Sectors like "Venture Capital, Finance"
    twitter_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    facebook_url = models.URLField(blank=True, null=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def update_metrics(self):
        # Automatically update metrics based on related investments
        self.total_investments = self.investments.count()
        self.total_portfolio_value = sum(investment.amount for investment in self.investments.all())
        self.number_of_portfolio_organizations = self.portfolio_companies.count()
        self.save()

    def __str__(self):
        return self.company_name


class PortfolioCompany(models.Model):
    name = models.CharField(max_length=255)
    sector = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    date_founded = models.DateField(null=True, blank=True)
    investment_company = models.ForeignKey(InvestmentCompany, related_name='portfolio_companies', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name


class Investment(models.Model):
    STAGE_CHOICES = [
        ('seed', 'Seed Stage'),
        ('bridge', 'Bridge Stage'),
        ('undisclosed', 'Undisclosed'),
        ('growth', 'Growth Stage'),
        ('late', 'Late Stage'),
    ]
    portfolio_company = models.ForeignKey(PortfolioCompany, related_name='investments', on_delete=models.CASCADE)
    investment_company = models.ForeignKey(InvestmentCompany, related_name='investments', on_delete=models.CASCADE)
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES, default='seed')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    investment_type = models.CharField(max_length=255, blank=True, null=True) 

    def __str__(self):
        return f'{self.investment_company.company_name} -> {self.portfolio_company.name} ({self.stage})'