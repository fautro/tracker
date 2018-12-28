from django.shortcuts import render
from django.http import HttpResponse
from wtrack.models import Weight
from wtrack.forms import WeightForm, AdditionsForm
import hashlib
from datetime import date, timedelta
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    record_list = Weight.objects.values('date', 'morning_weight', 'additions__sleep_hours', 'additions__calories_consumed',
                                        'additions__climbing_flag', 'additions__gym_flag', 'additions__alco_flag',
                                        'additions__evening_weight').filter(user = request.user).order_by('-date')[:30]

    graph_list = Weight.objects.values('date', 'morning_weight',
                                       'additions__evening_weight').filter(user = request.user).order_by('-date')[:30]
    context_dict = {'records':      record_list,
                    'graph_points': graph_list}

    return render(request, 'wtrack/index.html', context=context_dict)

def about(request):
    return render(request, 'wtrack/about.html')

### ----------------the function below is for testing purposes only -----------------###
def test(request):
    record_list = Weight.objects.values('date', 'morning_weight', 'additions__sleep_hours',
                                        'additions__calories_consumed', \
                                        'additions__climbing_flag', 'additions__gym_flag', 'additions__alco_flag', \
                                        'additions__evening_weight').order_by('-date')[:30]
    context_dict = {'records': record_list}

    return render(request, 'wtrack/index2.html', context=context_dict)

###---------------------------------------------------------------------------------###
@login_required
def add_record(request):

    context = {}

    if request.method == 'POST':
        weight_form = WeightForm(request.user, request.POST)
        additions_form = AdditionsForm(request.user, request.POST)
        if 'submit_weight' in request.POST and weight_form.is_valid():
            weight = weight_form.save(commit=False)
            weight.user = request.user
            concat_date = request.POST['date_year']+request.POST['date_month']+request.POST['date_day']
            weight.HKY = calc_hash(request.user.username, concat_date)
            weight.save()
        if 'submit_addition' in request.POST and additions_form.is_valid():
            addition = additions_form.save(commit=False)
            #addition.user = request.user
            #concat_date = request.POST['date_year']+request.POST['date_month']+request.POST['date_day']
            #addition.date = 'asdasd'#date.today()
            #addition.HKY = calc_hash(request.user.username, concat_date)
            addition.save()

    else:
        weight_form = WeightForm(request.POST)
        additions_form = AdditionsForm(request.POST)

    context['weight'] = weight_form
    context['additions'] = additions_form
    return render(request, 'wtrack/add_record.html', context)

def calc_hash(username, date):
    hash_obj = hashlib.md5((username + str(date)).encode())
    HKY = hash_obj.hexdigest()
    return HKY