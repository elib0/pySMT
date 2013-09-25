from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.utils import simplejson


def register(request):
    context = 'Esto es la pagina de registro'
    return render(request, 'users/register.html', {'context': context})


def save(request):
    result = {'success': -1, 'message': 'Error desconocido'}
    if request.is_ajax():
        post = request.POST
        u = User.objects.create_user(post['name'], post['email'], post['pass'])
        try:
            u.save()
            result['success'] = 1
            result['message'] = 'Usuario registrado'
        except:
            result['success'] = 0
            result['message'] = 'Su voto no a sido registrado'
    json = simplejson.dumps(result)
    return HttpResponse(json, mimetype='application/json')


def loginuser(request):
    msj = 'Error Desconocido'
    if request.method == 'POST':
        post = request.POST
        u = authenticate(username=post['name'], password=post['pass'])
        if u is not None:
            if u.is_active:
                login(request, u)
            else:
                msj = 'lo sentimos este usuario no se encuntra disponible'

            return redirect('/')
        else:
            msj = 'Usuario invalido'
            redirect('users/login.html', {'msj': msj})
    else:
        return render(request, 'users/login.html', {'msj': msj})
