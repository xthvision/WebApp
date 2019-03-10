from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth

# Create your views here.
def home(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'],
        password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('main')
        else:
            return render(request, 'accounts/home.html', {'erro': 'User name or password is inccorect.'})
    else:
        return render(request, 'accounts/home.html')
def signup(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['passwordconfirm'] and request.POST['username'] and request.POST['email']:
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'accounts/signup.html', {'error': "User already exists"})
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password'], email=request.POST['email'])
                auth.login(request, user)
                return redirect('home')
        else: 
            return render(request, 'accounts/signup.html', {'error': "password do not match or a filed is empty."})
    else:
        return render(request, 'accounts/signup.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')
    else:
        auth.logout(request)
        return redirect('home')