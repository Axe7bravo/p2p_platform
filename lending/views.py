
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, LoanForm, InvestmentForm, RegistrationForm, UserProfileForm
from .forms import VerificationForm
from .models import Loan, Payment, UserProfile,BorrowerVerification
from django.core.mail import send_mail
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid() and form.cleaned_data['password1'] == form.cleaned_data['password2']:
            user = form.save()
            user_profile = UserProfile(user=user, first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'])
            user_profile.save()
            login(request, user)
            return redirect('home')  # Replace 'home' with the URL name of your home page
    else:
        form = RegistrationForm()
        return render(request, 'lending/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username'] 

            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('home') 
  # Replace 'home' with the actual URL name of your homepage
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'The form is invalid.')  # Add an error message for invalid form
    else:
        form = LoginForm()
    return render(request, 'lending/login.html', {'form': form})
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logout   

def homepage(request):
    return render(request, 'lending/homepage.html')

def offerings(request):
    return render(request, 'lending/offerings.html')


@login_required
def create_loan(request):
    if request.method == 'POST':
        form = LoanForm(request.POST)
        if form.is_valid():
            loan = form.save(commit=False)
            loan.borrower = request.user 
            loan = form.save()
            return redirect('list_loans')
    else:
        form = LoanForm()
    return render(request, 'lending/create_loan.html', {'form': form})

def list_loans(request):
    loans = Loan.objects.filter(status='pending')
    return render(request, 'lending/list_loans.html', {'loans': loans})

def invest_in_loan(request, loan_id):
    loan = Loan.objects.get(id=loan_id)
    if request.method == 'POST':
        form = InvestmentForm(request.POST)
        if form.is_valid():
            investment = form.save(commit=False)
            investment.loan = loan
            investment.investor = request.user
            investment.save()
            return redirect('list_loans')
    else:
        form = InvestmentForm()
        return render(request, 'lending/invest_in_loan.html', {'loan': loan, 'form': form})

def make_payment(request, loan_id):
    loan = Loan.objects.get(id=loan_id)
    if request.method == 'POST':
        payment_amount = request.POST.get('payment_amount')

        # Calculate interest based on payment frequency
        if loan.payment_frequency == 'monthly':
            interest_rate_per_period = loan.interest_rate / 12
        elif loan.payment_frequency == 'weekly':
            interest_rate_per_period = loan.interest_rate / 52
        # ... other payment frequencies ...

        interest_amount = loan.outstanding_balance * interest_rate_per_period
        total_payment = payment_amount + interest_amount

        # Update outstanding balance and status
        
        update = loan.outstanding_balance - total_payment
        update_loan_status(update)
        
        #if loan.outstanding_balance <= 0:
        #    loan.status = 'Repaid'
        #loan.save()

        # Create payment record
        payment = Payment(loan=loan, amount=total_payment)
        payment.save()

        return redirect('list_loans')
    return render(request, 'loans/make_payment.html', {'loan': loan})

def list_payments(request, loan_id):
    loan = Loan.objects.get(id=loan_id)
    payments = loan.payments.all()
    return render(request, 'lending/list_payments.html', {'loan': loan, 'payments': payments})

def update_loan_status(loan):
    total_paid = loan.payments.aggregate(sum('amount'))['amount__sum'] or 0
    if total_paid >= loan.amount:
        loan.status = 'repaid'
    elif total_paid > 0:
        loan.status = 'partially_repaid'
    else:
        loan.status = 'pending'
    loan.save()
    
def user_profile(request):
    user = request.user
    profile = user.profile
    return render(request, 'lending/profile.html', {'user': user, 'profile': profile})

def edit_profile(request):
    user = request.user
    profile = user.profile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'lending/edit_profile.html', {'form': form})

def borrower_dashboard(request):
    user = request.user
    loans = Loan.objects.filter(borrower=user)
    payments = Payment.objects.filter(loan__borrower=user)

    context = {
        'loans': loans,
        'payments': payments,
    }

    return render(request, 'lending/dashboard.html', context)

def index(request):
    return render(request, './index.html')

def about_view(request):
    return render(request, 'lending/about.html')

def test_view(request):
    return render  (request, 'lending/example.html')

def faq_view(request):
    return render(request, 'lending/faq.html')


def contact_view(request):
    if request.method == 'POST': 

        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Send email
        send_mail( 

            'Contact Form Submission',
            message,
            email,
            ['thato.dice@gmail.com'],  # Replace with your email address
        )

        return redirect('contact')  # Redirect back to the contact page

    return render(request, 'lending/contact.html')

def verification_view(request):
    if request.user.user_type == 'borrower':
        if request.method == 'POST':
            form = VerificationForm(request.POST, request.FILES)
            if form.is_valid():
                verification = BorrowerVerification(user=request.user, **form.cleaned_data)
                verification.save()
                return redirect('verification_submitted')
        else:
            form = VerificationForm()
        return render(request, 'lending/borrower_verification.html', {'form': form})
    else:
        return redirect('home')  # Redirect to homepage if not a borrower

def verification_submitted(request):
    return render(request, 'lending/verification_submitted.html')