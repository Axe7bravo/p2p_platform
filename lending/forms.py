from django import forms
from .models import Loan, Investment, User, UserProfile
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    
class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['amount', 'interest_rate', 'term_months']

class InvestmentForm(forms.ModelForm):
    class Meta:
        model = Investment
        fields = ['amount']
        
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=30, widget=forms.EmailInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control'}))
    user_type =forms.ChoiceField(choices=[('borrower', 'Borrower'), ('lender', 'Lender')], widget=forms.Select(attrs={'class':'btn btn-primary dropdown-toggle'}))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'user_type')
        
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        
        
class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
    
    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'bio')