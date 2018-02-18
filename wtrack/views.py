from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    context_dict = {'boldmessage': "You\'ll get your fat ass moving when this is over."}
    return render(request, 'wtrack/index.html', context=context_dict)

def about(request):
    return HttpResponse("This is a future \"About\" page.")
