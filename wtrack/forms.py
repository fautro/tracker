from django import forms
from wtrack.models import Weight, Additions
from datetime import date, timedelta
from django.contrib.auth.models import User
import hashlib

class WeightForm(forms.ModelForm):
    date = forms.DateField(widget=forms.SelectDateWidget(), initial=date.today(), required=True)
    morning_weight = forms.DecimalField(max_digits=5, decimal_places=2, required=True)

    def clean(self):
        cleaned_data = self.cleaned_data
        date = cleaned_data['date']
        cleaned_data['user'] = self.user_w
        cleaned_data['HKY'] = self.calc_hash(self.user_w, date)
        return cleaned_data

    def calc_hash(self, username, date):
        hash_obj = hashlib.md5((username + date).encode())
        HKY = hash_obj.hexdigest()
        return HKY

    def __init__(self, user, *args, **kwargs):
        self.user_w = kwargs.pop('user', None)
        super(WeightForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Weight
        exclude = ()

class AdditionsForm(forms.ModelForm):
    CLIMBING_FLAGS = (
        ('R', 'Rest'),
        ('B', 'Bouldering'),
        ('BM', 'Bouldering on Moonboard'),
        ('L', 'Lead'),
        ('D', 'Dry')
    )

    GYM_FLAGS = (
        ('R', 'Rest'),
        ('L', 'Leg Day'),
        ('LS', 'Leg Day Short'),
        ('U', 'Upper Body Day'),
        ('US', 'Upper Body Day Short'),
        ('W', 'Whole Body Workout'),
        ('C', 'Cardio')
    )

    ALCO_FLAGS = (
        ('Y', 'YES'),
        ('N', 'NO')
    )

    date = forms.ModelChoiceField(queryset=None)
    ## day = models.CharField(max_length=3, default=day_of_week(date))
    sleep_hours = forms.IntegerField()
    calories_consumed = forms.IntegerField()
    climbing_flag = forms.CharField(max_length=2, widget=forms.Select(choices=CLIMBING_FLAGS))
    gym_flag = forms.CharField(max_length=2, widget=forms.Select(choices=GYM_FLAGS))
    alco_flag = forms.CharField(max_length=2, widget=forms.Select(choices=ALCO_FLAGS), required=True)

    def clean(self):
        cleaned_data = self.cleaned_data
        date = cleaned_data['date']
        cleaned_data['HKY'] = self.calc_hash(self.user_a, date)
        return cleaned_data

    def calc_hash(self, username, date):
        hash_obj = hashlib.md5((username + date).encode())
        HKY = hash_obj.hexdigest()
        return HKY

    class Meta:
        model = Additions
        exclude = ()
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        queryset_date_interval = date.today() - timedelta(days=14)
        query_set = Weight.objects.filter(date__gte = queryset_date_interval).order_by('-date')
        if query_set.count() < 14:
            queryset_date_interval = date.today() - timedelta(days=21)
            query_set = Weight.objects.filter(date__gte=queryset_date_interval).order_by('-date')
        self.fields['date'].queryset = query_set
        self.user_a = kwargs.pop('user', None)

