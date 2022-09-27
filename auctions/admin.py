from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Listings)
admin.site.register(User)
admin.site.register(Bid)
admin.site.register(Watchlist)