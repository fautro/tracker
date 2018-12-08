from django.shortcuts import render
from django.http import HttpResponse
from wtrack.models import Weight
from wtrack.forms import WeightForm, AdditionsForm
from django.contrib.auth.decorators import login_required
import hashlib, datetime


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
        weight_form = WeightForm(request.POST)
        additions_form = AdditionsForm(request.POST)
        if 'submit_weight' in request.POST and weight_form.is_valid():
            weight = weight_form.save(commit=False)
            weight.user = request.user
            weight.HKY = '799d239d94be7e2c994ba361912ad58b'
            weight.save()
        if 'submit_addition' in request.POST and additions_form.is_valid():
            additions_form.save()

    else:
        weight_form = WeightForm(request.POST)
        additions_form = AdditionsForm(request.POST)

    context['weight'] = weight_form
    context['additions'] = additions_form
    return render(request, 'wtrack/add_record.html', context)

def clean(self):
    cleaned_data = self.cleaned_data
    date = cleaned_data.get('date')
    cleaned_data['user'] = self.user_w
    HKY = self.calc_hash(self.user_w.username, date)
    cleaned_data['HKY'] = HKY
    return cleaned_data

def calc_hash(username, date):
    hash_obj = hashlib.md5((username + str(date)).encode())
    HKY = hash_obj.hexdigest()
    return HKY