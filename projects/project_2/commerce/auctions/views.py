from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .forms import AuctionForm, BidForm, CommentForm

from .models import User, Bid, Comment, Auction

# TODO: user shouldn't be able to bid self auction, if already bid should only be able to update the bid
# TODO: fixed auction image size
# TODO: in new auction, if no url is provided, display a default img


def index(request):
  auctions = Auction.objects.all()

  return render(request, "auctions/index.html", {
    "auctions": auctions,
  })


def login_view(request):
  if request.method == "POST":

    # Attempt to sign user in
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)

    # Check if authentication is successful
    if user is not None:
      login(request, user)
      return HttpResponseRedirect(reverse("index"))
    else:
      return render(request, "auctions/login.html", {
        "message": "Invalid username and/or password.",
      })
  else:
    return render(request, "auctions/login.html")


def logout_view(request):
  logout(request)
  return HttpResponseRedirect(reverse("index"))


def register(request):
  if request.method == "POST":
    username = request.POST["username"]
    email = request.POST["email"]

    # Ensure password matches password confirmation
    password = request.POST["password"]
    password_confirmation = request.POST["confirmation"]
    if password != password_confirmation:
      return render(request, "auctions/register.html", {
          "message": "Passwords must match.",
      })

    # Attempt to create new user
    try:
      user = User.objects.create_user(username, email, password)
      user.save()
    except IntegrityError:
      return render(request, "auctions/register.html", {
        "message": "Username already taken.",
      })
    login(request, user)
    return HttpResponseRedirect(reverse("index"))
  else:
    return render(request, "auctions/register.html")


def auction(request, auction_title):
  try:
    auction = Auction.objects.get(title=auction_title)
  except:
    return HttpResponseRedirect(reverse("no_auction"))

  if request.method == "POST":
    if not request.user.is_authenticated:
      return HttpResponseRedirect(reverse("login"))

    if "bid" in request.POST:
      bid_form = BidForm(request.POST)
      if not bid_form.is_valid():
        return render(request, "auctions/no_auction.html")

      amount = bid_form.cleaned_data["amount"]

      try:
        bid_on_auction(user=request.user, auction=auction, amount=amount)

      except Bid.MultipleObjectsReturned:
        return render(request, "auctions/no_auction.html")
      except TooSmallBidAmount:
        return HttpResponseRedirect(auction_url(auction_title))

      return HttpResponseRedirect(auction_url(auction_title))


    if "comment" in request.POST:
      comment_form = CommentForm(request.POST)
      if not comment_form.is_valid():
        return render(request, "auctions/no_auction.html")
      comment_on_auction(user=request.user, auction=auction, content=comment_form.cleaned_data["content"])
      return HttpResponseRedirect(auction_url(auction_title))

    if "watchlist" in request.POST:
      request.user.watchlist.add(auction)
      return HttpResponseRedirect(auction_url(auction_title))

    if "remove_from_wathclist" in request.POST:
      request.user.watchlist.remove(auction)
      return HttpResponseRedirect(auction_url(auction_title))

    if "sell_to_highest_bidder" in request.POST:
      try:
        sell_auction_to_highest_bidder(auction=auction)
      except NoBids:
        return HttpResponseRedirect(reverse("no_auction"))

      return HttpResponseRedirect(auction_url(auction_title))

    return HttpResponseRedirect(reverse("no_auction"))


  user_owns_auction = False
  is_in_watchlist = False
  if request.user.is_authenticated:
    # reverse look up for many to many relationship works like below
    is_in_watchlist = bool(Auction.objects.filter(user__username=request.user.username, title=auction_title))
    user_owns_auction = auction.holder == request.user

  bids = sorted(auction.auction_bids.all(), key= lambda bid: bid.amount, reverse=True)
  comments = auction.auction_comments.all()
  bid_form = BidForm()
  comment_form = CommentForm()
  category = Auction.Category(auction.category).label
  return render(request, "auctions/auction.html", {
    "auction": auction,
    "category": category,
    "bids": bids,
    "comments": comments,
    "bid_form": bid_form,
    "comment_form": comment_form,
    "is_in_watchlist": is_in_watchlist,
    "user_owns_auction": user_owns_auction,
    "bids_exist": bool(len(bids))
  })

def no_auction(request):
  return render(request, "auctions/no_auction.html")

def new_auction_view(request):
  if not request.user.is_authenticated:
    return HttpResponseRedirect(reverse("login"))

  if request.method == "POST":
    auction_form = AuctionForm(request.POST)
    if not auction_form.is_valid():
      return HttpResponseRedirect(reverse("no_auction"))
    data = auction_form.cleaned_data
    auction = Auction(
      title=data["title"], 
      description=data["description"],
      date=datetime.now(),
      holder=request.user,
      starting_bid=data["starting_bid"],
      picture_url=data["picture_url"],
      category=data["category"],
    )
    auction.save()
    return HttpResponseRedirect(auction_url(auction.title))

  auction_form = AuctionForm()
  return render(request, "auctions/new_auction.html", {
    "auction_form": auction_form
  })

def categories(request):
  categories_list = []
  # put "other" category to end for visual purposes
  category_choices = Auction.Category.choices
  choice_other_index = category_choices.index(
    list(filter(lambda choice: choice[0] == Auction.Category.other, category_choices))[0]
  )
  choice_other = category_choices.pop(choice_other_index)
  category_choices.append(choice_other)

  for category, label in category_choices:
    auctions = Auction.objects.filter(category=category)
    categories_list.append({"name": label, "auctions": auctions})

  return render(request, "auctions/categories.html", {
    "categoriesList": categories_list,
  })

def watchlist(request):
  if not request.user.is_authenticated:
    return HttpResponseRedirect(reverse("login"))

  if request.method == "POST":
    if "remove_from_wathclist" in request.POST:
      print(request.POST["remove_from_wathclist"])
      try:
        auction = Auction.objects.get(title=request.POST["auction_title"])
      except:
        return HttpResponseRedirect(reverse("no_auction"))

      request.user.watchlist.remove(auction)
      return HttpResponseRedirect(reverse("watchlist"))

    return HttpResponseRedirect(reverse("no_auction"))


  watched_auctions = request.user.watchlist.all()

  return render(request, "auctions/watchlist.html", {
    "watched_auctions": watched_auctions,
  })


def auction_url(auction_title):
  return f"{reverse('index')}auction/{auction_title}"

class TooSmallBidAmount(Exception):
  pass
class NoBids(Exception):
  pass

def bid_on_auction(user, auction, amount):
  if amount < auction.starting_bid:
    raise TooSmallBidAmount
  if len(auction.auction_bids.all()) > 0:
    highest_bid = max(auction.auction_bids.all(), key= lambda bid: bid.amount).amount
    if amount <= highest_bid:
      raise TooSmallBidAmount


  existing_bid = None
  try:
    existing_bid = Bid.objects.get(user=user, bid_auction=auction)

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
      user=user,
    )
    current_bid.save()
    return

  existing_bid.amount = amount
  existing_bid.save()


def comment_on_auction(user, auction, content):
  comment = Comment(
    content=content,
    date=datetime.now(),
    comment_auction=auction,
    user=user,
  )
  comment.save()

def sell_auction_to_highest_bidder(auction):
  bids = auction.auction_bids.all()
  if (not len(bids)):
    # this should not happen cuz it should be disabled
    raise NoBids
  bid_list = sorted(list(bids), key=lambda bid: bid.amount)
  # bid_list.sort(key=lambda bid: bid.amount)
  highest_bid = bid_list[-1]
  auction.taken_bid = highest_bid
  auction.save()
