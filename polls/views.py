from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from polls.models import Poll
from django.utils import simplejson
# Create your views here.


def index(request):
    latest_poll_list = Poll.objects.order_by('-pub_date')[:5]
    context = {'latest_poll_list': latest_poll_list}
    return render(request, 'index.html', context)


def detail(request, poll_id):
    if request.user.is_authenticated():
        p = get_object_or_404(Poll, pk=poll_id)
        return render(request, 'polls/detail.html', {'poll': p})
    else:
        return redirect('/')


def results(request, poll_id):
    if request.user.is_authenticated():
        p = get_object_or_404(Poll, pk=poll_id)
        context = {'poll': p}
        return render(request, 'polls/result.html', context)
    else:
        return redirect('/')


def vote(request, poll_id):
    result = {'success': -1, 'message': 'Error desconocido'}
    if request.is_ajax() and request.method == 'POST':
        p = Poll.objects.get(pk=poll_id)
        c = p.choice_set.get(pk=request.POST['choice'])
        c.votes += 1
        try:
            c.save()
            result['success'] = 1
            result['message'] = 'Su voto a sido registrado'
        except:
            result['success'] = 0
            result['message'] = 'Su voto no a sido registrado'

    json = simplejson.dumps(result)
    return HttpResponse(json, mimetype='application/json')
