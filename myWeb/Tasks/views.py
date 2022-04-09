from django.shortcuts import render
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from tasks.models import Account, Task


def index(request, error_message=''):
    return render(request, 'registration/login.html', {
        'error_message': error_message
        })

def registration(request):
    return render(request, 'registration/registration.html')

def login(request):
    user      = request.POST['user']
    password  = request.POST['password']
    try:
        savedPassword   = Account.objects.get(username=user).password
        account         = Account.objects.get(username=user)
    except Account.DoesNotExist:
        return HttpResponseRedirect(reverse("tasks:loginerror", args=('Usuario no encontrado',)))
    else:
        if check_password(password, savedPassword):
            return render(request, 'tasks/home.html', {
                'account':account
            })
        else:
            return HttpResponseRedirect(reverse("tasks:loginerror", args=('Contraseña incorrecta',)))