from django.contrib import admin

from .models.projects import (
    Project, 
    Category, 
    SubCategory, 
    PitchDeckSection, 
    Founder,
)

from .models.statistics import Statistics
from .models.testimonials import Testimonial
from .models.partners import Partner
from .models.contact import ContactDetails, SendQuestion
from .models.faq import FAQ, RaisingContact
from .models.company import Company

from .models.bank_council import (
    BankCouncil, 
    BankMember, 
    Bank, 
    Position, 
    Criteria, 
    Meeting,
)

from .models.bank_secretary import BankSecretary
from .models.moderator import Moderator

from .models.investor import (
    Investor, 
    BankAccountInfo, 
    Card, 
    Transaction, 
    InvestorDocument,
    Invoice,
    Check,
    ProjectInvestment,
)

from .models.application import (
    Application, 
    ApplicationScore, 
    ApplicationNotification,
)

from .models.investor_company import (
    Investment,
    InvestmentCompany,
    PortfolioCompany,
)

from .models.approval import ApprovalHistory
from .models.aboutus import AboutUs, Oferta
from .models.club import Club, ClubBankAccountInfo
from .models.blog import BlogPost
from .models.glossary import Glossary, GlossarySection
from .models.report import Report
from .models.investor_company import InvestmentCompany

from .models.company_info import (
    CompanyInfo,
    Financials,
    Funding,
    CompanyInvestment,
    Acquisition,
    Story
)

@admin.register(Investor)
class InvestorAdmin(admin.ModelAdmin):
    list_display = ('user', 'investor_type')
    list_filter = ('investor_type',)
    search_fields = ('user__email',)


admin.site.register(Club)
admin.site.register(ClubBankAccountInfo)

admin.site.register(Invoice)
admin.site.register(Check)

admin.site.register(Meeting)

admin.site.register(Application)
admin.site.register(ApplicationScore)

admin.site.register(Project)
admin.site.register(PitchDeckSection)
admin.site.register(Category)
admin.site.register(SubCategory)

admin.site.register(Statistics)

admin.site.register(Testimonial)

admin.site.register(Partner)

admin.site.register(ContactDetails)

admin.site.register(FAQ)

admin.site.register(Company)

admin.site.register(BankCouncil)

admin.site.register(BankSecretary)

admin.site.register(Moderator)

admin.site.register(BankMember)
admin.site.register(Bank)
admin.site.register(Position)
admin.site.register(BankAccountInfo)
admin.site.register(Card)
admin.site.register(Transaction)
admin.site.register(InvestorDocument)
admin.site.register(Founder)
admin.site.register(Criteria)

admin.site.register(ApprovalHistory)

admin.site.register(SendQuestion)

admin.site.register(AboutUs)

admin.site.register(RaisingContact)

admin.site.register(BlogPost)

admin.site.register(ApplicationNotification)

admin.site.register(Oferta)

admin.site.register(ProjectInvestment)

admin.site.register(Glossary)
admin.site.register(GlossarySection)

admin.site.register(Report)

admin.site.register(InvestmentCompany)
admin.site.register(Investment)
admin.site.register(PortfolioCompany)

admin.site.register(CompanyInfo)
admin.site.register(Financials)
admin.site.register(Funding)
admin.site.register(CompanyInvestment)
admin.site.register(Acquisition)
admin.site.register(Story)