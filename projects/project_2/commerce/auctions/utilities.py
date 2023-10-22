from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .forms import AuctionForm, BidForm, CommentForm

from .models import User, Bid, Comment, Auction

class InvalidForm(Exception):
  pass

class TooSmallBidAmount(Exception):
  pass

def bid_on_auction(request, auction):
  bid_form = BidForm(request.POST)
  if not bid_form.is_valid():
    raise InvalidForm
    # return render(request, "auctions/no_auction.html")

  amount = bid_form.cleaned_data["amount"]

  highest_bid = max(Bid.objects.filter(bid_auction=auction), key= lambda bid: bid.amount).amount
  if amount < auction.starting_bid or amount <= highest_bid:
    raise TooSmallBidAmount

  existing_bid = None
  try:
    existing_bid = Bid.objects.get(user=request.user, bid_auction=auction)

  except Bid.DoesNotExist:
    pass

  except Bid.MultipleObjectsReturned:
    # should not happen
    raise Bid.MultipleObjectsReturned

  if not existing_bid:
    current_bid = Bid(
      amount=amount, 
      bid_auction=auction,
      date=datetime.now(),
      user=request.user,
    )
    current_bid.save()

  existing_bid.amount = amount
  existing_bid.save()


def auction_url(auction_title):
  return f"{reverse('index')}auction/{auction_title}"
