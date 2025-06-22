from django.contrib import admin
from .models import *
from accounts.models import Profile

admin.site.register(Month)
admin.site.register(Tag)
admin.site.register(LookCard)
admin.site.register(Event)
admin.site.register(LookItem)
admin.site.register(Comment)
admin.site.register(Profile)