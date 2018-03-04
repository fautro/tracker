from django.db import models
import datetime as dt

class Record(models.Model):
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

    date = models.DateField(auto_now=False, auto_now_add=False, primary_key=True)
    ## day = models.CharField(max_length=3, default=day_of_week(date))
    sleep_hours = models.SmallIntegerField()
    calories_consumed = models.SmallIntegerField()
    climbing_flag = models.CharField(max_length=2, choices=CLIMBING_FLAGS)
    gym_flag = models.CharField(max_length=2, choices=GYM_FLAGS)
    alco_flag = models.CharField(max_length=1, choices=ALCO_FLAGS)

    def __str__(self):
        sDate = self.date.isoformat()
        return sDate

    ##def day_of_week(self.date):
    ##    day_nr = dt.datetime.weekday(date)
    ##    day_arr = ['Mo', 'Tue', 'Wed', 'Thu', 'Fr', 'Sat', 'Sun']
    ##    return day_arr[day_nr]


class MorningWeight(models.Model):
    date = models.OneToOneField(
        Record,
        on_delete=models.CASCADE
    )
    morning_weight = models.DecimalField(max_digits=5, decimal_places=2)

class EveningWeight(models.Model):
    date = models.OneToOneField(
        Record,
        on_delete=models.CASCADE
    )
    evening_weight = models.DecimalField(max_digits=5, decimal_places=2)