from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils import simplejson
from users.models import Friendship
import users.forms as userform


def register(request):
    if request.is_ajax() and request.method == 'POST':
        result = {'success': -1, 'message': 'Error desconocido'}
        form = userform.RegisterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            u = User.objects.create_user(name, email, password)
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
        form = userform.RegisterForm()
        title = 'Registrar usuario'
    return render(request, 'users/register.html', {'title': title, 'registerform': form})


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
            if u.pk == int(user_id):
                view_title = 'Tu perfil'
                return render(request, 'users/profile.html',
                              {'user': u, 'title': view_title})
            else:
                ue = get_object_or_404(User, pk=user_id)
                f = Friendship.objects.filter(follower=u.pk, followed=user_id)[:1]
                if f:
                    f = 'Dejar de seguir'
                else:
                    f = 'Seguir'
                view_title = 'Perfil de: '+str(ue.username)
                context = {'title': view_title, 'user': u,
                           'user_external': ue, 'follow_status': f}
                return render(request, 'users/external_profile.html', context)
    else:
        return redirect('/')


def follow_or_unfollow(request, followed_id):
    result = {'success': -1, 'message': 'Seguir'}
    if request.user.is_authenticated():
        if request.is_ajax() and request.method == "POST":
            u = request.user
            ue = User.objects.get(pk=followed_id)
            followed, created = Friendship.objects.get_or_create(follower=u, followed=ue)
            if created:
                result['success'] = 1
                result['message'] = 'Dejar de seguir'
            else:
                followed.delete()
    json = simplejson.dumps(result)
    return HttpResponse(json, mimetype='application/json')


def loginuser(request):
    msj = ''
    if request.method == 'POST':
        form = userform.LoginForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            password = form.cleaned_data['password']
            u = authenticate(username=name, password=password)
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
        form = userform.LoginForm()
    return render(request, 'users/login.html', {'msj': msj, 'loginform': form})


def logoutuser(request):
    if request.user.is_authenticated():
        logout(request)
    return redirect('index')
