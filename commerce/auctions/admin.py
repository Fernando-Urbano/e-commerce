from django.contrib import admin

# Register your models here.
from .models import Auction, User, Bid, Comment, Category

admin.site.register(Auction)
admin.site.register(User)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Category)