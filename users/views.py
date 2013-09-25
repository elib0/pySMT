from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User

def register(request):
    context = 'Esto es la pagina de registro'
    return render(request, 'users/register.html', {'context': context})
