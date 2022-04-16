"""Some functions to tasks app"""
from django.contrib.auth.hashers import make_password, check_password
from tasks.models import Account

def login(request):
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