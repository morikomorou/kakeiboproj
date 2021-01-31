from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.db import IntegrityError

# Create your views here.
def signupfunc(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.create_user(username, '', password)
            return redirect('login')
        except IntegrityError:
            return render(request, 'accounts/signup.html', {'error':'このユーザはすでに登録されています。'})

    return render(request, 'accounts/signup.html', {})


def loginfunc(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/kakeibo/list')
        else:
            return render(request, 'accounts/login.html', {})
    return render(request, 'accounts/login.html', {})