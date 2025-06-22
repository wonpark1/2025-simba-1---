from django.contrib import admin
from .models import *
from accounts.models import Profile

# Register your models here.
admin.site.register(Month)
admin.site.register(Tag)
admin.site.register(Event)
admin.site.register(LookCard)
admin.site.register(LookItem)
admin.site.register(Comment)
admin.site.register(Profile)