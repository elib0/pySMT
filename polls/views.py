from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from polls.models import Poll,Choice
# Create your views here.

def index(request):
    latest_poll_list = Poll.objects.filter().order_by('-pub_date')[:5]
    context = {'latest_poll_list': latest_poll_list}
    return render(request, 'polls/index.html', context)

def detail(request, poll_id):
    num_votes = 0;
    poll = get_object_or_404(Poll, pk=poll_id)
    return render(request, 'polls/detail.html', {'poll': poll})

def results (request, poll_id): 
    return HttpResponse("You're looking at the results of poll %s." % poll_id)

def vote(request, poll_id):
    p = Poll.objects.get(pk=poll_id)
    c = p.choice_set.get(pk=request.POST['choice'])
    c.votes += 1
    c.save()
    # json = simplejson.dumps(msg)
    # return HttpResponse(json, mimetype='application/json')
    return redirect('index')