from django.urls import path

from .views.projects import (
    CreateUpdateProjectView,
    ProjectsPublicView,
    FounderCreateUpdateView,
    PitchDeckSectionCreateUpdateView,
    ProjectDetailView,
    ProjectSearchListView,
    CategoryListView,
    ProjectApplicationsListView,
)

from .views.company import (
    CreateCompanyView,
    CompanyUpdateView,
    UserCompanyDetailView,
    CompanyListView,
)

from .views.statistics import (
    StatisticsView, 
    StatisticsUpdateView, 
    StatisticsDeleteView,
)

from .views.testimonials import (
    TestimonialListView, 
    TestimonialCreateView, 
    TestimonialUpdateView, 
    TestimonialDeleteView,
)

from .views.partners import (
    PartnerListView,
    PartnerCreateView,
    PartnerUpdateView,
    PartnerDeleteView
)

from .views.contact import (
    ContactDetailsView,
    SendQuestionCreateView,
)

from .views.application import (
    ApplicationCreateView,
    ApplicationUpdateView,
)

from .views.faq import (
    FAQListView,
    FAQCreateUpdateDeleteView,
    RaisingContactCreateView,
)

from .views.moderator import (
    ModeratorApplicationListView,
    ModeratorReviewView,
    ModeratorUpdateView,
    ModeratorProfileView,
    ApplicationNotificationListView,
    AddBankAccountForClub
)

from .views.bank_secretary import (
    BankSecretaryPendingApplicationsView,
    BankSecretaryApprovalView,
    BankMemberCreateView,
    BankSecretaryProfileView, 
    BankMemberListView,
    CouncilMeetingCreateView,
    CouncilMeetingListView,
)

from .views.bank_council import (
    BankCouncilMeetingDetailView,
    BankCouncilMeetingListView,
    BankCouncilMemberProjectsView,
    BankCouncilMemberProfileView,
    ApplicationScoringView,
    ApprovedByBankSecretaryView,
    ApplicationsByBankMemberView,
    CouncilMembersView,
)

from .views.investor import (
    BankAccountInfoListView, 
    InvestorDocumentView,
    AllTransactionsListView,
    TransactionListView,
    BusinessAngelInvestorListView,
    VentureFundInvestorListView,
    ProjectsInvestorView,
    InvestorUpdateView,
    InvestorProfileView,
    DashBordApiView
)

from .views.aboutus import (\
    AboutUsListView,    
    OfertaHTMLView,
)

from app.views.club import (
    ClubUpdateCreateApiView,
    ClubListApiView,
    ClubListGetMyClubs,
    JoinClubApiView,
    RequestsApiView,
    JoinClubApiView,
    ApproveClubApiView,
    ModeratorNotApprovedClubs
)

from app.views.club_payment import (
    PaymentForClubApiView,
    PaymentConfirmForClub,
    GetTransactionsClubApiView,
    PaymentProjectFromClub,
    CheckCreateForProjectFromClub
)

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

from app.views.blog import(
    BlogPostListView
)

from user.views import UserTokenObtainPairView

from app.views.glossary import GlossaryView

from app.views.report import ReportListView

from app.views.company_info import CompanyInfoListView, CompanyInfoDetailView

from app.views.investor_company import (
    InvestmentCompanyListView, 
    InvestmentStatisticsView, 
    InvestmentCompanyUpdateView
)

from .views.payment import (
    CreateCard,
    ConfirmCard,
    GetCard,
    DeleteCardApiView,
    PaymentForProject,
    CheckCreateForProject,

)
urlpatterns = [

    #project
    path('project/create/', CreateUpdateProjectView.as_view(), name='project-create'),
    path('project/update/<int:id>/', CreateUpdateProjectView.as_view(), name='project-update'),
    path('project/visible/', ProjectsPublicView.as_view(), name='project-visible'),
    path('project/visible/<int:id>/', ProjectDetailView.as_view(), name='project-detail'),
    path('project/search/', ProjectSearchListView.as_view(), name='project-search'),
    path('project/founder/', FounderCreateUpdateView.as_view(), name='founder-create'),
    path('project/founder/', FounderCreateUpdateView.as_view(), name='founder-update'),
    path('project/pitchdeck/', PitchDeckSectionCreateUpdateView.as_view(), name='pitchdeck-create'),
    path('project/pitchdeck/', PitchDeckSectionCreateUpdateView.as_view(), name='pitchdeck-update'),
    path('project/categories/', CategoryListView.as_view(), name='category-list'),
    path('projects/<int:project_id>/applications/', ProjectApplicationsListView.as_view(), name='project-applications'),


    #company
    path('company/create/', CreateCompanyView.as_view(), name='company-create'),
    path('company/update/<int:pk>/', CompanyUpdateView.as_view(), name='company-update'),
    path('company/my/', UserCompanyDetailView.as_view(), name='user_company_detail'),
    path('companies/', CompanyListView.as_view(), name='company_list'),


    #application
    path('application/create/', ApplicationCreateView.as_view(), name='application-create'),
    path('application/update/', ApplicationUpdateView.as_view(), name='application-update'),   


    #moderator
    path('moderator/application/', ModeratorApplicationListView.as_view(), name='moderator-application'),
    path('moderator/application/review/<int:application_id>/', ModeratorReviewView.as_view(), name='moderator-application-review'), 
    path('moderator/profile/update/', ModeratorUpdateView.as_view(), name='moderator-profile-update'),  
    path('moderator/profile/', ModeratorProfileView.as_view(), name='moderator-profile'),
    path('moderator/created-clibs/',ModeratorNotApprovedClubs.as_view(),name='moderator-clubs'),
    path('moderator/approve/clubs/',ApproveClubApiView.as_view(),name='moderator-approve-club'),
    path('moderator/add-bank-account/', AddBankAccountForClub.as_view(), name='add-club-bank-account'),
    path('moderator/notification/', ApplicationNotificationListView.as_view(), name='moderator-notification'),
    

    #banksecretary
    path('bank/secretary/application/', BankSecretaryPendingApplicationsView.as_view(), name='secretary-application'),
    path('bank/secretary/application/review/<int:application_id>/', BankSecretaryApprovalView.as_view(), name='secretary-application-review'), 
    path('bank/secretary/profile/', BankSecretaryProfileView.as_view(), name='secretary-profile'), 
    path('bank/secretary/create/meeting/', CouncilMeetingCreateView.as_view(), name='secretary-profile'), 
    path('bank/secretary/meetings/', CouncilMeetingListView.as_view(), name='secretary-profile'), 
    path('bank/secretary/create/bankmember/', BankMemberCreateView.as_view(), name='secretary-profile'), 
    path('bank/secretary/bankmembers/', BankMemberListView.as_view(), name='secretary-profile'), 


    #bankcouncil
    path('bank/council/profile/', BankCouncilMemberProfileView.as_view(), name='council-profile'),  
    path('bank/council/profile/update/', BankCouncilMemberProfileView.as_view(), name='council-profile-update'),  
    path('bank/council/score/<int:application_id>/', ApplicationScoringView.as_view(), name='council-score'),  
    path('bank/council/meetings/', BankCouncilMeetingListView.as_view(), name='council-meetings'),
    path('bank/council/meetings/detail/<int:meeting_id>/', BankCouncilMeetingDetailView.as_view(), name='council-meetings-detail'),
    path('bank/council/projects/', BankCouncilMemberProjectsView.as_view(), name='council-projects'),
    path('bank/council/applications/all/', ApprovedByBankSecretaryView.as_view(), name='council-applications-all'),
    path('bank/council/applications/', ApplicationsByBankMemberView.as_view(), name='council-applications-self'),
    path('bank/council/members/', CouncilMembersView.as_view(), name='council-members'),
    

    #investor
    path('investor/bank-cards/', GetCard.as_view(), name='bank-card-list'),
    path('investor/bank-accounts/', BankAccountInfoListView.as_view(), name='bank-account-info-list'),
    path('investor/documents/', InvestorDocumentView.as_view(), name='investor-document-list-create'),
    path('investor/documents/<int:pk>/', InvestorDocumentView.as_view(), name='investor-document-detail'),
    path('investor/transactions/', TransactionListView.as_view(), name='transaction-list'),
    path('investor/transactions/all/', AllTransactionsListView.as_view(), name='transaction-list'),
    path('investor/business/angel/', BusinessAngelInvestorListView.as_view(), name='nusiness-angels'),
    path('investor/business/venture/', VentureFundInvestorListView.as_view(), name='venture-fund'),
    path('investor/projects/', ProjectsInvestorView.as_view(), name='investor-projects'),
    path('investor/update/info/',InvestorUpdateView.as_view(),name='investor-update-info'),
    path('investor/profile/details/<int:id>/',InvestorProfileView.as_view(),name='investor-details'),
    path('investor/dashboard/',DashBordApiView.as_view(),name='dashboard'),


    #statistics
    path('statistics/', StatisticsView.as_view(), name='statistics'),   
    path('statistics/update/<int:pk>/', StatisticsUpdateView.as_view(), name='statistics-update'),
    path('statistics/delete/<int:pk>/', StatisticsDeleteView.as_view(), name='statistics-delete'),


    #testimonials
    path('testimonials/', TestimonialListView.as_view(), name='testimonial-list'),
    path('testimonials/create/', TestimonialCreateView.as_view(), name='testimonial-create'),
    path('testimonials/update/<int:pk>/', TestimonialUpdateView.as_view(), name='testimonial-update'),
    path('testimonials/delete/<int:pk>/', TestimonialDeleteView.as_view(), name='testimonial-delete'),


    #partners
    path('partners/', PartnerListView.as_view(), name='partner-list'),
    path('partners/create/', PartnerCreateView.as_view(), name='partner-create'),
    path('partners/update/<int:pk>/', PartnerUpdateView.as_view(), name='partner-update'),
    path('partners/delete/<int:pk>/', PartnerDeleteView.as_view(), name='partner-delete'),


    #contact
    path('contact-details/', ContactDetailsView.as_view(), name='contact-details-view'),
    path('contact-details/sendquestion/', SendQuestionCreateView.as_view(), name='contact-question'),


    #faq
    path('faqs/', FAQListView.as_view(), name='faq-list'), 
    path('faqs/manage/', FAQCreateUpdateDeleteView.as_view(), name='faq-create'),
    path('faqs/manage/<int:pk>/', FAQCreateUpdateDeleteView.as_view(), name='faq-manage'), 
    path('raising/contact/', RaisingContactCreateView.as_view(), name='faq-list'), 

    #aboutus
    path('about-us/', AboutUsListView.as_view(), name='about-us-list'),
    path('oferta/html/', OfertaHTMLView.as_view(), name='oferta-html'),


    #blog
    path('blog/', BlogPostListView.as_view(), name='blog-list'),


    #glossary
    path('glossaries/', GlossaryView.as_view(), name='glossary-view'),


    #report
    path('reports/', ReportListView.as_view(), name='report-view'),


    #investor-company
    path('investor-company/', InvestmentCompanyListView.as_view(), name='investor-company'),
    path('investor-company/<int:pk>/', InvestmentCompanyListView.as_view(), name='investor-company'),
    path('investor-company/statistics/<int:pk>/', InvestmentStatisticsView.as_view(), name='investor-company-statistics'),
    path('investment_company/update/<int:pk>/', InvestmentCompanyUpdateView.as_view(), name='investment-company-update'),


    #company-info
    path('companies-info/', CompanyInfoListView.as_view(), name='company-info-list'),
    path('companies-info/<int:id>/', CompanyInfoDetailView.as_view(), name='company-info-detail'),


    #token
    path('token/', UserTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),


    #club
    path('club/create/',ClubUpdateCreateApiView.as_view(),name='club-create'),
    path('club/update/<int:pk>/',ClubUpdateCreateApiView.as_view(),name='club-update'),
    path('club/get/',ClubListApiView.as_view(), name ='get-clubs'),
    path('club/join/',JoinClubApiView.as_view(),name='join-club-request'),
    path('club/join/requestes/',RequestsApiView.as_view(),name='club-requests'),
    path('club/myclubs/member/',ClubListGetMyClubs.as_view(),name='get-myclubs-member'),
    path('club/join/approve/',JoinClubApiView.as_view(),name='approved-or-reject'),
    path('club/payment/project/',PaymentProjectFromClub.as_view(),name='payment-from-club'),
    path('club/payment/project/confirm/',CheckCreateForProjectFromClub.as_view(),name = 'payment-from-club-confirm'),


    #card
    path('card/create/', CreateCard.as_view(), name='card-create'),
    path('card/confirm/',ConfirmCard.as_view(),name='cord-confirm'),
    path('card/get/',GetCard.as_view(),name='card-get'),
    path('card/delete/',DeleteCardApiView.as_view(),name='delete-card'),
    path('payment/project/',PaymentForProject.as_view(),name='payment-project'),
    path('payment/confirm/',CheckCreateForProject.as_view(),name='payment-confirm'),
]
