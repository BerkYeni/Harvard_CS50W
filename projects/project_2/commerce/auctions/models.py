from django.db import models
from django.contrib.auth.models import AbstractUser

ms = models


class User(AbstractUser):
  pass

class Auction(ms.Model):
  title = ms.CharField(max_length=64)
  description = ms.CharField(max_length=2048)
  date = ms.DateTimeField()
  holder = ms.ForeignKey(
    User, on_delete=ms.CASCADE, related_name="user_auctions"
  )
  starting_bid = ms.FloatField()
  picture_url = ms.URLField(max_length=128)

#   bids = ms.ForeignKey(
#     Bid, on_delete=ms.CASCADE, related_name="auction_bids"
#   )
#   comments = ms.ForeignKey(
#     Comment, on_delete=ms.CASCADE, related_name="auction_comments"
#   )


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
