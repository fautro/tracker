from django.contrib import admin
from wtrack.models import Record, MorningWeight, EveningWeight

# Register your models here.

admin.site.register(Record)
admin.site.register(MorningWeight)
admin.site.register(EveningWeight)