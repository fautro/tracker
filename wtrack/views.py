from django.shortcuts import render
from django.http import HttpResponse
from wtrack.models import Record

def index(request):
    record_list = Record.objects.values('date', 'sleep_hours', 'calories_consumed', \
                                        'climbing_flag', 'gym_flag', 'alco_flag', \
                                        'morningweight__morning_weight', \
                                        'eveningweight__evening_weight').order_by('-date')[:30]
    context_dict = {'records': record_list}
    return render(request, 'wtrack/index.html', context=context_dict)

def about(request):
    return render(request, 'wtrack/about.html')
