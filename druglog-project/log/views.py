from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render 
from django.contrib.auth import authenticate, login 
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from .models import Profile 
from django.contrib import messages 
# Create your views here.

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated '\
                        'Successfully')
                else:
                    return HttpResponse('Disabled Account')
            else:
                return HttpResponse('Invalid Login')
    else: 
        form = LoginForm()
        return render(request, 'log/login.html', {'form': form})
        
@login_required
def dashboard(request):
    return render(request, 'log/dashboard.html', {'section': 'dashboard'})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create new user 
            new_user = user_form.save(commit=False)
            #set the chosen password 
            new_user.set_password(user_form.cleaned_data['password'])
            #save new user 
            new_user.save()
            #create the user profile 
            Profile.objects.create(user=new_user)
            return render(request, 'log/register_done.html', {'new_user': new_user })
    else:
        user_form = UserRegistrationForm() 
    return render(request, 'log/register.html', {'user_form': user_form })

@login_required 
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated'\
                 'Successfuly')
        else:
            messages.error(request, 'Error updating your profile! Recheck fields.')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(
            instance=request.user.profile
        )
    return render(request, 'log/edit.html', {'user_form': user_form, 'profile_form': profile_form})

        