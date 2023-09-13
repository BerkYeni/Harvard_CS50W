from django import forms
from .models import Auction


fs = forms

bid_amount_field = fs.FloatField(
    label='',
    min_value=0,
    widget=fs.NumberInput(attrs={
      'step': '0.01',
      'min': '0',
      # 'placeholder': 'Starting bid'
    })
  )

category_field = fs.ChoiceField(
  choices=Auction.Category.choices,

)

# def bid_amount_field(attrs) -> list:
#   return fs.FloatField(
#     label='',
#     min_value=0,
#     widget=fs.NumberInput(attrs={
#       'step': '0.01',
#       'min': '0',
#       # 'placeholder': 'Starting bid'
#     })
#   )

class BidForm(fs.Form):
  amount = bid_amount_field


class AuctionForm(fs.Form):
  title = fs.CharField(
    label='', 
    # max_length=Auction.title.max_length,
    max_length=64,
    widget=fs.TextInput(attrs={'placeholder': 'Title'})
  )

  category = category_field

  description = fs.CharField(
    label='', 
    # max_length=Auction.description.max_length,
    max_length=2048,
    widget=fs.Textarea(attrs={
      'placeholder': 'Description',
      'rows': 5,
      'cols': 40,
    })
  )

  starting_bid = bid_amount_field

  picture_url = fs.URLField(
    required=False,
    label='',
    max_length=128,
    widget=fs.TextInput(attrs={
      'placeholder': 'Picture URL (optional)',
    })
  )


class CommentForm(fs.Form):
  content = fs.CharField(
    label='',
    max_length=1024,
    widget=fs.Textarea(attrs={
      'placeholder': 'Comment here.',
      'rows': 5,
      'cols': 45,
    })
  )