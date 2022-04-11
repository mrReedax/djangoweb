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

def home(request, account):
    return render(request, 'tasks/home.html', {\
        'account':account
        })

def login(request):
    if request.method == 'POST':
        user      = request.POST['user']
        password  = request.POST['password']
        try:
            savedPassword   = Account.objects.get(username=user).password
            account         = Account.objects.get(username=user)
        except Account.DoesNotExist:
            return HttpResponseRedirect(reverse("tasks:loginerror", args=('*Usuario no encontrado',)))
        else:
            if check_password(password, savedPassword):
                return home(request, account)
            else:
                return HttpResponseRedirect(reverse("tasks:loginerror", args=('*Contraseña incorrecta',)))
    else:
        return HttpResponseRedirect(reverse("tasks:index"))

def changeState(request, user_id):
    if request.method == 'POST':
        account = Account.objects.get(pk=user_id)
        task    = account.task_set.get(pk=request.POST['task_id'])
        task.changeTaskCompletionState()
        task.save()
        return home(request, account)