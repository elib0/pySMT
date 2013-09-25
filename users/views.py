from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
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
