from django.shortcuts import render
from django.http import HttpResponse
from wtrack.models import Record

def index(request):
    record_list = Record.objects.order_by('-date')[:30]
    context_dict = {'records': record_list}
    return render(request, 'wtrack/index.html', context=context_dict)

def about(request):
    return render(request, 'wtrack/about.html')
