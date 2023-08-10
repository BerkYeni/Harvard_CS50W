from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
  return render(request, "hello/index.html")

def user(request):
  return HttpResponse("hello user")

def developer(request):
  return HttpResponse("hello developer")

def greet(request, name):
  return render(request, "hello/greet.html", {
    "name": name.capitalize(),
  })