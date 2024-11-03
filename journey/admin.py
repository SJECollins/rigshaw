from django.contrib import admin

from .models import Journey, Request, Meeting


admin.site.register(Journey)
admin.site.register(Request)
admin.site.register(Meeting)