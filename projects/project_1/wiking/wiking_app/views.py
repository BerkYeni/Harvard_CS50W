from django.shortcuts import render
from .models import Entry
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from random import choice
from markdown2 import Markdown

md = Markdown()

def get_entry(entry_title):
  try:
    entry = Entry.objects.get(title=entry_title)
  except Entry.DoesNotExist:
    entry = None
  return entry

def entry_url(entry_title):
  return f'{reverse("index")}{entry_title}'


# Create your views here.
def index(request):
  all_entries = Entry.objects.all()

  return render(request, "wiking_app/index.html", {
    "all_entries": all_entries,
  })

def entry(request, entry_title):
  entry = get_entry(entry_title)
  
  if not entry:
    return HttpResponseRedirect(reverse("no_such_entry"))

  if request.method == "POST":
    if "delete_entry" in request.POST:
      entry.delete()
      return HttpResponseRedirect(reverse("index"))


  entry_content = md.convert(entry.content)
  return render(request, "wiking_app/entry.html", {
    "entry_title": entry.title,
    "entry_content": entry_content,
  })

def new_entry(request):
  if request.method == "POST":
    title = request.POST["title"]
    try:
      Entry.objects.get(title=title)
    except Entry.DoesNotExist:
      exists = False
    else:
      exists = True

    if not exists:
      content = request.POST["content"]
      Entry(title=title, content=content).save()
      return HttpResponseRedirect(entry_url(title))
      # return HttpResponseRedirect(reverse("entry_added"))
    else:
      return HttpResponseRedirect(reverse("entry_add_failed"))

  return render(request, "wiking_app/new_entry.html", {
  })

def no_such_entry(request):
  return render(request, "wiking_app/no_such_entry.html", {

  })

def entry_added(request):
  return render(request, "wiking_app/entry_added.html")

def entry_add_failed(request):
  return render(request, "wiking_app/entry_add_failed.html")

def random_redirect(request):
  random_entry = choice(Entry.objects.all())

  return HttpResponseRedirect(entry_url(random_entry.title))

def edit_entry(request, entry_title):
  entry = get_entry(entry_title)

  if request.method == "POST":
    entry.content = request.POST["content"]
    entry.save()
    return HttpResponseRedirect(entry_url(entry.title))


  return render(request, "wiking_app/edit_entry.html", {
    "entry_title": entry.title,
    "entry_content": entry.content,
  })


def search(request):
  search_text = request.GET["title"]
  entry = get_entry(search_text)

  if entry:
    return HttpResponseRedirect(entry_url(entry.title))
  
  search_results = Entry.objects.filter(title__contains=search_text)
  return render(request, "wiking_app/search.html", {
    "search_results": search_results,
  })