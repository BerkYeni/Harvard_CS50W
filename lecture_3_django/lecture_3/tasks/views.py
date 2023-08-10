from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.

class NewTaskForm(forms.Form):
  task = forms.CharField(label="New Task")

def index(request):
  if "all_tasks" not in request.session:
    request.session["all_tasks"] = []
  return render(request, "tasks/index.html", {
    "tasklist": request.session["all_tasks"],
  })

def add(request):
  if request.method == "POST":
    form = NewTaskForm(request.POST)
    if form.is_valid():
      task = form.cleaned_data["task"]
      request.session["all_tasks"] += [task]
      return HttpResponseRedirect(reverse("tasks:index"))
    else:
      return render(request, "tasks/add.html", {
        "form": form
      })

  return render(request, "tasks/add.html", {
    "form": NewTaskForm(),
  })