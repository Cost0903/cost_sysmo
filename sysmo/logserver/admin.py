from django.contrib import admin
from .models import Machine, MachineGroup, Policy, Performance

# Register your models here.
admin.site.register(Machine)
admin.site.register(MachineGroup)
admin.site.register(Policy)
admin.site.register(Performance)
