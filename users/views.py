from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils import simplejson


def register(request):
    if request.method == 'POST':
        result = {'success': -1, 'message': 'Error desconocido'}
        if request.is_ajax():
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
            if request.user.pk == int(user_id):
                u = request.user
                return render(request, 'users/profile.html', {'user': u})
            else:
                u = get_object_or_404(User, pk=user_id)
                return HttpResponse('Perfil externo de: %s' % u.username)
    else:
        return redirect('/')


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
