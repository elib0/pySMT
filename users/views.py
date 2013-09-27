from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils import simplejson
from users.models import Friendship


def register(request):
    if request.is_ajax() and request.method == 'POST':
        result = {'success': -1, 'message': 'Error desconocido'}
        p = request.POST
        u = User.objects.create_user(p['name'], p['email'], p['pass'])
        try:
            u.save()
            result['success'] = 1
            result['message'] = 'Usuario registrado'
        except:
            result['success'] = 0
            result['message'] = 'Usuario no registrado'
        json = simplejson.dumps(result)
        return HttpResponse(json, mimetype='application/json')
    else:
        return render(request, 'users/register.html')


def profile(request, user_id):
    #Solo si el usuario esta autenticado
    if request.user.is_authenticated():
        #SI es llamada por un form y peticion ajax guardo datos de profile
        if request.is_ajax() and request.method == 'POST':
            result = {'success': 0, 'message': 'No se han podido guardar los cambios'}
            u = request.user
            u.first_name = request.POST['name']
            u.last_name = request.POST['lastname']
            try:
                u.save()
                result['success'] = 1
                result['message'] = 'Datos guardados'
            except:
                pass
            json = simplejson.dumps(result)
            return HttpResponse(json, mimetype='application/json')
        #Si no es de un form muestro form de profile
        else:
            u = request.user
            if request.user.pk == int(user_id):
                return render(request, 'users/profile.html', {'user': u})
            else:
                userexternal = get_object_or_404(User, pk=user_id)
                context = {'user': u, 'user_external': userexternal}
                return render(request, 'users/external_profile.html', context)
    else:
        return redirect('/')


def follow_user(request):
    result = {'success': -1, 'message': 'Seguir'}
    if request.user.is_authenticated():
        if request.is_ajax() and request.method == "POST":
            u = request.user
            f = Friendship(u.id, request.POST[''])
            try:
                f.save()
                result['success'] = 1
                result['message'] = 'Seguido'
            except:
                pass
    json = simplejson.dumps(result)
    return HttpResponse(json, mimetype='application/json')


def loginuser(request):
    msj = ''
    if request.method == 'POST':
        post = request.POST
        u = authenticate(username=post['name'], password=post['pass'])
        if u is not None:
            if u.is_active:
                msj = 'Logueado correctamente'
                login(request, u)
            else:
                msj = 'lo sentimos este usuario no se encuntra disponible'

            return redirect('/')
        else:
            msj = 'Usuario invalido'
            return redirect('users/login.html', {'msj': msj})
    else:
        return render(request, 'users/login.html', {'msj': msj})


def logoutuser(request):
    if request.user.is_authenticated():
        logout(request)
    return redirect('index')
