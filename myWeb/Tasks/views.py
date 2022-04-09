from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'registration/login.html')

def registration(request):
    return render(request, 'registration/registration.html')

def login(request):
    return render(request, 'tasks/home.html')