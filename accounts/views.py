from django.shortcuts import render, redirect
from .models import Account
from .forms import AccountCreationForm, AccountAuthenticationForm, AccountAssignmentFormSet
from django.contrib.auth import login, logout, authenticate
from .filters import AccountFilter
from django.contrib.admin.views.decorators import staff_member_required
# Create your views here.


# User assign role

@staff_member_required
def account_assignment(request):
    message = None
    message_status = None
    formset = AccountAssignmentFormSet()
    if request.method == 'POST':
        formset = AccountAssignmentFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            formset = AccountAssignmentFormSet()
            message = "User updated successfully"
            message_status = 200
        else:
            message = 'There was a problem updating this user'
            message_status = 400
    else:
        formset = AccountAssignmentFormSet()

    context = {
        'formset': formset,
        'message': message,
        'message_status': message_status
    }
    return render(request, 'account_extra/account_assignment.html', context)

#Authorization and Authentication

def registration(request):
    form = AccountCreationForm()

    if request.method == 'POST':
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            new_account = form.save()
            new_account = authenticate(email=form.cleaned_data['email'], password = form.cleaned_data['password1'])
            login(request, new_account)
            return redirect('tracker:homepage')

    context = {
        'form': form
    }

    return render(request,'registration/registration.html', context)


def loginPage(request):
    form = AccountAuthenticationForm()

    if request.user.is_authenticated:
        return redirect('tracker:homepage')

    if request.method == 'GET':

        print(request.GET)
        if 'project_manager' in request.GET:
            pj = Account.objects.get(email="demo_admin@demo.com")
            login(request, pj)
            return redirect('tracker:homepage')

        if 'developer' in request.GET:
            pj = Account.objects.get(email="demo_dev@demo.com")
            login(request, pj)
            return redirect('tracker:homepage')

        if 'submiter' in request.GET:
            pj = Account.objects.get(email="demo_submiter@demo.com")
            login(request, pj)
            return redirect('tracker:homepage')

    if request.method == 'POST':
        form = AccountAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('tracker:homepage')

    context = {
        'form': form
    }
    return render (request, 'registration/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('tracker:homepage')