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

def auction_url(auction_title):
  return f"{reverse('index')}auction/{auction_title}"


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

    bid_form = BidForm(request.POST)
    comment_form = CommentForm(request.POST)
    if bid_form.is_valid():
      if bid_form.cleaned_data["amount"] < auction.starting_bid:
        return HttpResponseRedirect(auction_url(auction.title))
      current_bid = Bid(
        amount=bid_form.cleaned_data["amount"], 
        bid_auction=auction,
        date=datetime.now(),
        user=request.user,
      )
      current_bid.save()
      return HttpResponseRedirect(auction_url(auction_title))
    elif comment_form.is_valid():
      comment = Comment(
        content=comment_form.cleaned_data["content"],
        date=datetime.now(),
        comment_auction=auction,
        user=request.user
      )
      comment.save()
      return HttpResponseRedirect(auction_url(auction_title))
    else:
      return HttpResponseRedirect(reverse("no_auction"))

  print(auction.Category.art.label)
  test = Auction.Category(auction.category)
  print(test.label)
  
  bids = auction.auction_bids.all()
  comments = auction.auction_comments.all()
  bid_form = BidForm()
  comment_form = CommentForm()
  category = Auction.Category(auction.category).label
  print(Auction.Category.choices)
  return render(request, "auctions/auction.html", {
    "auction": auction,
    "category": category,
    "bids": bids,
    "comments": comments,
    "bid_form": bid_form,
    "comment_form": comment_form,
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