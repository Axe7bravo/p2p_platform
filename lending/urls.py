from django.urls import path

from . import views

urlpatterns = [
    path('homepage/', views.homepage, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create-loan/',views.create_loan, name='create_loan'),
    path('list-loans/', views.list_loans, name='list_loans'),
    path('invest/<int:loan_id>/', views.invest_in_loan, name='invest_in_loan'),

    
]