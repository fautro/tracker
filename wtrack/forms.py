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
        return cleaned_data

    def __init__(self, user, *args, **kwargs):
        self.user_w = user
        super(WeightForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Weight
        exclude = ('HKY', 'user')

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

    #HKY
    date = forms.ModelChoiceField(queryset=None,
                                 #to_field_name = 'date',
                                 required=True)
    #date = forms.DateField(widget=forms.SelectDateWidget(), initial=date.today())
    evening_weight = forms.DecimalField(max_digits=5, decimal_places=2, required=True)
    sleep_hours = forms.IntegerField()
    calories_consumed = forms.IntegerField()
    climbing_flag = forms.CharField(max_length=2, widget=forms.Select(choices=CLIMBING_FLAGS))
    gym_flag = forms.CharField(max_length=2, widget=forms.Select(choices=GYM_FLAGS))
    alco_flag = forms.CharField(max_length=2, widget=forms.Select(choices=ALCO_FLAGS), required=True)

    def clean(self):
        cleaned_data = self.cleaned_data
        return cleaned_data

    class Meta:
        model = Additions
        exclude = ()#'HKY',)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        queryset_date_interval = date.today() - timedelta(days=14)
        query_set = Weight.objects.filter(date__gte = queryset_date_interval).order_by('-date')
        if query_set.count() < 14:
            queryset_date_interval = date.today() - timedelta(days=21)
            query_set = Weight.objects.filter(date__gte=queryset_date_interval).order_by('-date')
        self.fields['HKY'].queryset = query_set
        self.user_a = user

