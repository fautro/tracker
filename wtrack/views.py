from django.shortcuts import render
from django.http import HttpResponse
from wtrack.models import Record
from wtrack.forms import RecordForm, MorningWeightForm, EveningWeightForm

def index(request):
    record_list = Record.objects.values('date', 'sleep_hours', 'calories_consumed', \
                                        'climbing_flag', 'gym_flag', 'alco_flag', \
                                        'morningweight__morning_weight', \
                                        'eveningweight__evening_weight').order_by('-date')[:30]
    context_dict = {'records': record_list}
    return render(request, 'wtrack/index.html', context=context_dict)

def about(request):
    return render(request, 'wtrack/about.html')

def add_record(request):

    form = RecordForm()

    if request.method == 'POST':
        form = RecordForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
    return render(request, 'wtrack/add_record.html', {'form': form})

def add_morning_weight(request):

    form = MorningWeightForm()

    if request.method == 'POST':
        form = MorningWeightForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
    return render(request, 'wtrack/add_record.html', {'form': form})


def add_evening_weight(request):

    form = EveningWeightForm()
    if request.method == 'POST':
        form = EveningWeightForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
    return render(request, 'wtrack/add_record.html', {'form': form})
