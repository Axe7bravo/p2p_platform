from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('homepage/', views.homepage, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create-loan/',views.create_loan, name='create_loan'),
    path('example/', views.test_view, name='example'),
    path('list-loans/', views.list_loans, name='list_loans'),
    path('invest/<int:loan_id>/', views.invest_in_loan, name='invest_in_loan'),
    path('profile/', views.user_profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('loans/', views.list_loans, name='loans'),
    path('payments/', views.list_payments, name='payments'),
    path('loan-applications/', views.list_loan_applications, name='loan_applications'),
    path('loan-applications/<int:application_id>/', views.loan_application_details, name='application_details'),
     path('loan-applications/<int:application_id>/edit/', views.edit_loan_application, name='edit_loan_application'),
    path('loan-applications/<int:application_id>/delete/', views.delete_loan_application, name='delete_loan_application'),
    path('offering/', views.offerings, name='offering'),
    path('about/', views.about_view, name='about'),
    path('faqs/', views.faq_view, name='faqs'),
    path('contact/', views.contact_view, name='contact'),
    path('verification/', views.verification_view, name='borrower_verification'),
    path('verification-submitted/', views.verification_submitted, name='verification_submitted'),
    path('loan-application/', views.loan_application, name='loan_application'),
    path('loan-application-submitted/', views.application_submitted, name='application_submitted'),


    
]