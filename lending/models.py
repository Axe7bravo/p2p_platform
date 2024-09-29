
# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    user_type = models.CharField(max_length=20, choices=[('borrower', 'Borrower'), ('lender', 'Lender')], default='borrower')
    last_name = models.CharField(max_length=100, blank=True)
    first_name = models.CharField(max_length=100, blank=True)
    profile = models.OneToOneField('UserProfile', on_delete=models.CASCADE, null=True, blank=True, related_name='user_profile')
    

    def __str__(self):
        return self.username  

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True, null=True)    
      
class Loan(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    term_months = models.PositiveIntegerField()
    outstanding_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('funded', 'Funded'), ('repaid', 'Repaid'), ('delinquent', 'Delinquent')])
    payment_frequency = models.CharField(max_length=20, choices=[('monthly','Monthly'),('weekly','Weekly'),('biweekly','Biweekly')])


class Investment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    investor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='investments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)

class Payment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    
    
  # Make bio optional