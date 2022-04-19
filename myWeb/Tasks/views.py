import os
from random import randint, random
from captcha.image import ImageCaptcha
from django.shortcuts import render
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect
from django.urls import reverse
from tasks.models import Account, Session, Captcha


def index(request, error_message=''):
    if 'sid' not in request.COOKIES.keys():
        return render(request, 'registration/login.html', {
            'error_message': error_message
            })
    else:
        return home(request)

def registration(request, error_message=''):
    image        = ImageCaptcha(width=290, height=90)
    letters_list = 'ABCDEFGHIJKLMNOPQR'
    captcha_text = ''.join([letters_list[index] for index in [randint(0,(len(letters_list) - 1)) for i in range(6)]])
    captcha      = Captcha.objects.create(captcha_text=captcha_text)
    image.write(captcha_text, f'tasks/static/captcha/{captcha.id}.png')
    return render(request, 'registration/registration.html', {
        'captcha_id': captcha.id,
        'error_message': error_message
    })

def processRegistration(request):
    if request.method == 'POST':
        captcha = Captcha.objects.get(pk=request.POST['captcha_id'])
        if request.POST['captcha'].upper() == captcha.captcha_text:
            if len(request.POST['password']) > 8:
                if request.POST['password'] == request.POST['passwordrep']:
                    try:
                        if len(request.POST['user']) < 5:
                            error_message = "El usuario debe tener 5 caracteres"
                        else:
                            Account.objects.get(username=request.POST['user'])
                            error_message = "El usuario ya existe"
                        create_user = False
                    except Account.DoesNotExist:
                        create_user = True
                    if create_user:
                        Account.objects.create(username=request.POST['user'], password=make_password(request.POST['password']))
                        return HttpResponseRedirect(reverse('tasks:index'))
                    else:
                        captcha.delete()
                        os.remove(f"tasks/static/captcha/{request.POST['captcha_id']}.png")
                        return registration(request, error_message)
                else:
                    error_message = 'Las contraseñas no coinciden'
                    captcha.delete()
                    os.remove(f"tasks/static/captcha/{request.POST['captcha_id']}.png")
                    return registration(request, error_message)
            else:
                error_message = 'Contraseña muy corta (minimo 8 caracteres)'
                captcha.delete()
                os.remove(f"tasks/static/captcha/{request.POST['captcha_id']}.png")
                return registration(request, error_message)
        else:
            error_message = 'Código captcha incorrecto'
            captcha.delete()
            os.remove(f"tasks/static/captcha/{request.POST['captcha_id']}.png")
            return registration(request, error_message)
    else:
        captcha.delete()
        os.remove(f"tasks/static/captcha/{request.POST['captcha_id']}.png")
        return HttpResponseRedirect(reverse('tasks:index'))



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
               return render(request, 'registration/login.html')

def modifyTask(request):
    if request.method == 'POST':
        try:
            session = Session.objects.get(pk=request.COOKIES['sid'])
            account = session.account_id
            if "newTask" in request.POST.keys():
                new_task = request.POST['newTask']
                duplicates_found = account.task_set.filter(task_text=new_task).count()
                if duplicates_found == 0:
                    account.task_set.create(task_text=new_task)
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

def logout(request):
    if 'sid' in request.COOKIES.keys():
        try:
            session = Session.objects.get(pk=request.COOKIES['sid'])
            session.delete()
            return HttpResponseRedirect(reverse('tasks:index'))
        except Session.DoesNotExist:
            return HttpResponseRedirect(reverse('tasks:index'))
    else:
        return HttpResponseRedirect(reverse('tasks:index'))