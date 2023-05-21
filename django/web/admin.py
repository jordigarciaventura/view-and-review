from django.contrib import admin
from web.models import *

# Register your models here.
admin.site.register(Movie)
admin.site.register(Watchlist)
admin.site.register(Favlist)
admin.site.register(Review)
admin.site.register(ReviewVote)
admin.site.register(Rating)