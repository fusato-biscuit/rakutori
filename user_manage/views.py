from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            input_username = form.cleaned_data['username']
            input_password = form.cleaned_data['password1']
            new_user = authenticate(username=input_username, password=input_password)
            if new_user is not None:
                login(request, new_user)
                return redirect('user_manage:signup_success')
    else:
        form = CustomUserCreationForm()
    return render(request, 'user_manage/signup.html', {'form': form})

def signup_success(request):
    return render(request, 'user_manage/signup_success.html')
