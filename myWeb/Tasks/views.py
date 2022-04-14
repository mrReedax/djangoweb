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

def home(request):
    if request.method == 'POST':
        user      = request.POST['user']
        password  = request.POST['password']
        try:
            savedPassword   = Account.objects.get(username=user).password
            account         = Account.objects.get(username=user)
        except Account.DoesNotExist:
            return index(request,'*Usuario no encontrado')
        else:
            if check_password(password, savedPassword):
                return render(request, 'tasks/home.html', {
                            'account':account
                        })
            else:
                return index(request,'*Contraseña incorrecta')
    else:
        return HttpResponseRedirect(reverse("tasks:index"))

def modifyTask(request, user_id):
    if request.method == 'POST':
        try:
            print(request.POST)
            account = Account.objects.get(pk=user_id)
            if "newTask" in request.POST.keys():
                #account.task_set.get(task_text=request.POST["newTask"])
                account.task_set.create(task_text=request.POST['newTask'])
            else:
                task    = account.task_set.get(pk=request.POST['task_id'])
                if "completeTask" in request.POST.keys():
                    task.changeTaskCompletionState()
                    task.save()
                elif "deleteTask" in request.POST.keys():
                    print(f"Task {task} deleted")
                    task.delete()
        except Exception as e:
            print(f'Error {e}')
        finally:
            return render(request, 'tasks/home.html', {
                        'account':account
                    })

def records(request):
    return render(request, 'tasks/records.html')
