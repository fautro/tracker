from django.shortcuts import render
from django.http import HttpResponse
from wtrack.models import Weight
from wtrack.forms import WeightForm, AdditionsForm

def index(request):
    record_list = Weight.objects.values('date', 'morning_weight', 'additions__sleep_hours', 'additions__calories_consumed', \
                                        'additions__climbing_flag', 'additions__gym_flag', 'additions__alco_flag', \
                                        'additions__evening_weight').order_by('-date')[:30]
    context_dict = {'records': record_list}
    return render(request, 'wtrack/index.html', context=context_dict)

def about(request):
    return render(request, 'wtrack/about.html')

def add_record(request):

    context = {}

    if request.method == 'POST':
        weight_form = WeightForm(request.POST)
        additions_form = AdditionsForm(request.POST)
        if 'submit_weight' in request.POST and weight_form.is_valid():
            weight_form.save()
        if 'submit_addition' in request.POST and additions_form.is_valid():
            additions_form.save()

    else:
        weight_form = WeightForm(request.POST)
        additions_form = AdditionsForm(request.POST)

    context['weight'] = weight_form
    context['additions'] = additions_form
    return render(request, 'wtrack/add_record.html', context)
