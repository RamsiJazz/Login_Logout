from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import never_cache


# Create your views here.
@never_cache
def index(request):
    if 'email' in request.session:
        return render(request, 'loggedin.html')
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST.get('email')
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if User.objects.filter(email=email).exists():
            return render(request, 'reg.html', {'error_message': 'User with this email id already exist'})
        if password != confirm_password:
            return render(request, 'reg.html', {'error_message': 'Password do not match.'})
        myuser = User.objects.create_user(username=email, email=email, password=password)
        myuser.first_name = first_name
        myuser.last_name = last_name
        myuser.save()
        return redirect('loginn')
    return render(request, 'reg.html')


@never_cache    
def loginn(request):
    if 'email' in request.session:
        return redirect('index')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Django built in authenticate function
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            request.session['email'] = email
            return redirect('index')
        else:
            request.session['alert_message'] = 'Username or password do not match. '
    alert_message =request.session.pop('alert_message',None)
    return render(request, 'login.html', {'alert_message': alert_message})


def signout(request):
    logout(request)
    return redirect(loginn)
