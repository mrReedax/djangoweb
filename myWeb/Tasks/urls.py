from django.urls import path
from tasks import views


app_name = 'tasks'
urlpatterns = [
    path('', views.index, name='index'),
    path('<error_message>', views.index, name='loginerror'),
    path('registration/', views.registration, name='registration'),
    path('account/home', views.login, name='login'),
    path('account/home', views.home, name='home'),
    path('account/home/<int:user_id>/changeState', views.changeState, name='changeState'),

    ]