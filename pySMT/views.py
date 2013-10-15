from polls.models import Poll
from django.shortcuts import render

context = {'title': ''}

def index(request):
    latest_poll_list = Poll.objects.order_by('-pub_date')[:5]
    context['latest_poll_list'] = latest_poll_list
    context['title'] = 'Bienvenido a sistema de encuestas'
    return render(request, 'index.html', context)
