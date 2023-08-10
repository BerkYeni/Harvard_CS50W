from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Bid, Comment, Auction

class AdminAuction(admin.ModelAdmin):
  list_display = ("id", "title", "description", "holder")

class AdminBid(admin.ModelAdmin):
  list_display = ("amount", "bid_auction")

admin.site.register(User, UserAdmin)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Auction, AdminAuction)