from django.urls import path
from tasks import views


app_name = 'tasks'
urlpatterns = [
    path('', views.index, name='index'),
    path('registration/', views.registration, name='registration'),
    path('account/', views.login, name='login')
    ]