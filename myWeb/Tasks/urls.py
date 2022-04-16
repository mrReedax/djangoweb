from django.urls import path
from tasks import views


app_name = 'tasks'
urlpatterns = [
    path('', views.index, name='index'),
    path('registration/', views.registration, name='registration'),
    path('home', views.home, name='home'),
    path('home/modifyTask', views.modifyTask, name='modifyTask'),
    path('records', views.records, name='records'),
    path('logout', views.logout, name='logout')
    ]