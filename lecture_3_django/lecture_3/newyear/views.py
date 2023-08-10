from django.shortcuts import render
from datetime import datetime

# Create your views here.
def index(request):
  today = datetime.now()
  return render(request, "newyear/index.html", {
    "isnewyear": today.month == 1 and today.day == 1,
  })