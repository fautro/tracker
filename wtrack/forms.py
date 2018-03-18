from django import forms
from wtrack.models import Weight, Additions
from datetime import date, timedelta

class WeightForm(forms.ModelForm):
    date = forms.DateField(initial=date.today(), required=True)
    morning_weight = forms.DecimalField(max_digits=5, decimal_places=2, required=True)

    class Meta:
        model = Weight
        exclude = ()

class AdditionsForm(forms.ModelForm):
    CLIMBING_FLAGS = (
        ('B', 'Bouldering'),
        ('BM', 'Bouldering on Moonboard'),
        ('L', 'Lead'),
        ('D', 'Dry')
    )

    GYM_FLAGS = (
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

    class Meta:
        model = Additions
        exclude = ()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        queryset_date_interval = date.today() - timedelta(days=14)
        query_set = Weight.objects.filter(date__gte = queryset_date_interval).order_by('-date')
        if query_set.count() < 14:
            queryset_date_interval = date.today() - timedelta(days=21)
            query_set = Weight.objects.filter(date__gte=queryset_date_interval).order_by('-date')
        self.fields['date'].queryset = query_set
