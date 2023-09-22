from django.db import models as ms
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy



class Auction(ms.Model):
  class Category(ms.TextChoices):
    other = "OT", "Other"
    electronics = "EL", "Electronics"
    fashion = "FA", "Fashion"
    art = "AR", "Art"

  title = ms.CharField(max_length=64)
  description = ms.CharField(max_length=2048)
  date = ms.DateTimeField()
  holder = ms.ForeignKey(
    "User", on_delete=ms.CASCADE, related_name="user_auctions"
  )
  starting_bid = ms.FloatField()
  picture_url = ms.URLField(max_length=128)
  category = ms.CharField(
    max_length=2,
    choices=Category.choices,
    default=Category.other,
  )

class User(AbstractUser):
  watchlist = ms.ManyToManyField(Auction)


class Comment(ms.Model):
  content = ms.CharField(max_length=1024)
  date = ms.DateTimeField()
  comment_auction = ms.ForeignKey(
    Auction, on_delete=ms.CASCADE, related_name="auction_comments"
  )
  user = ms.ForeignKey(
    User, on_delete=ms.CASCADE, related_name="user_comments"
  )


class Bid(ms.Model):
  amount = ms.FloatField()
  date = ms.DateTimeField()
  bid_auction = ms.ForeignKey(
    Auction, on_delete=ms.CASCADE, related_name="auction_bids"
  )
  user = ms.ForeignKey(
    User, on_delete=ms.CASCADE, related_name="user_bids"
  )
