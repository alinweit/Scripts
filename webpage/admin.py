from django.contrib import admin
from .models import User, Raeume, MyBookings
# Register your models here.

admin.site.register(User)
admin.site.register(Raeume)
admin.site.register(MyBookings)