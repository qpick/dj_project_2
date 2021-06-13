from django.contrib import admin
from .models import Category, AdListing, Comment, Bid

# Register your models here.
admin.site.register(Category)
admin.site.register(AdListing)
admin.site.register(Comment)
admin.site.register(Bid)
