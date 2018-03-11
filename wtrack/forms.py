from django import forms
from wtrack.models import Record, MorningWeight, EveningWeight

class RecordForm(forms.ModelForm):
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

    date = forms.DateField(widget=forms.SelectDateWidget(), required=True)
    ## day = models.CharField(max_length=3, default=day_of_week(date))
    sleep_hours = forms.SmallIntegerField()
    calories_consumed = forms.SmallIntegerField()
    climbing_flag = forms.CharField(max_length=2, widget=forms.Select())#choices=CLIMBING_FLAGS)
    gym_flag = forms.CharField(max_length=2, widget=forms.Select())#choices=GYM_FLAGS)
    alco_flag = forms.CharField(max_length=2, widget=forms.Select(), required=True)#choices=ALCO_FLAGS)

    class Meta:
        model = Record
        exclude = ()

class MorningWeightForm(forms.ModelForm):
    date = forms.ChoiseField(choices=Record.objects.values('date').order_by('-date'), required=True)
    morning_weight = forms.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        model = MorningWeight,
        exclude = ()

class EveningWeightForm(form.ModelForm):
    date = forms.ChoiseField(choices=Record.objects.values('date').order_by('-date'), required=True)
    evening_weight = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        model = EveningWeight
        exclude = ()