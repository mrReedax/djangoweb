from django.shortcuts import render
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect
from django.urls import reverse
from tasks.models import Account, Session


def index(request, error_message=''):
    if 'sid' not in request.COOKIES.keys():
        return render(request, 'registration/login.html', {
            'error_message': error_message
            })
    else:
        return home(request)

def registration(request):
    return render(request, 'registration/registration.html')

def home(request, *args, **kwargs):
    if 'sid' not in request.COOKIES.keys():
        if request.method == 'POST':
            user      = request.POST['user']
            password  = request.POST['password']
            try:
                account         = Account.objects.get(username=user)
            except Account.DoesNotExist:
                return index(request,'*Usuario no encontrado')
            else:
                if check_password(password, account.password):
                    tasks = account.task_set.all()
                    try:
                        sid = account.session_set.create()
                        sid = sid.session_id
                    except Exception as e:
                        print(e)
                        print(f'Attempting to generate sid for user {account}')
                        return index(request,'No se ha podido iniciar sesion')
                    response = render(request, 'tasks/home.html', {
                                'tasks':tasks,
                                'user': user
                            })
                    response.set_cookie(key='sid',value=sid)
                    return response
                else:
                    return index(request,'*Contraseña incorrecta')
        else:
           return index(request,'Inicia sesion para continuar')
    else:
        try:
            session = Session.objects.get(pk=request.COOKIES['sid'])
            account = session.account_id
            tasks = account.task_set.all()
            response = render(request, 'tasks/home.html', {
                                'tasks':tasks,
                                'user': account.username
                            })
            return response
        except Exception as e:
            return index(request,'*No se ha podido iniciar sesion')


def modifyTask(request):
    if request.method == 'POST':
        try:
            session = Session.objects.get(pk=request.COOKIES['sid'])
            account = session.account_id
            if "newTask" in request.POST.keys():
                # TODO: validar si la tarea existe antes de agregarla
                #account.task_set.get(task_text=request.POST["newTask"])
                account.task_set.create(task_text=request.POST['newTask'])
            else:
                task    = account.task_set.get(pk=request.POST['task_id'])
                if "completeTask" in request.POST.keys():
                    task.changeTaskCompletionState()
                    task.save()
                elif "deleteTask" in request.POST.keys():
                    task.delete()
        except Exception as e:
            print(f'Error {e}')
        finally:
            return HttpResponseRedirect(reverse('tasks:home'))
    else:
        return HttpResponseRedirect(reverse('tasks:home'))

def records(request):
    if 'sid' in request.COOKIES.keys():
        session = Session.objects.get(pk=request.COOKIES['sid'])
        account = session.account_id
        records = account.task_set.filter(completed=True).order_by('-completion_date')
        return render(request, 'tasks/records.html', {
                    'user':account.username,
                    'records': records
                    })
    else:
        return index(request,'Inicia sesion para continuar')
