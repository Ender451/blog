from django.contrib import admin
from home.models import Visitors
# Register your models here.

class VisitorsAdmin(admin.ModelAdmin):
    list_display = ('Visit_day','Visitors_number',)
    

admin.site.register(Visitors,VisitorsAdmin)
