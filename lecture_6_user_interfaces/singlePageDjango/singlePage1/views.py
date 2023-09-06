from django.http import Http404, HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
  return render(request, 'singlePage1/index.html')

texts = [
  'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean nec mi eget nisl volutpat sodales. Nullam pharetra massa mauris.',
  'Curabitur eget orci vitae lectus elementum lacinia. Phasellus dignissim enim in diam dignissim, sed rutrum mi viverra. Fusce condimentum ac ipsum luctus porta. Suspendisse ut mollis sem. Aliquam convallis malesuada vulputate. Etiam id tincidunt dui. Nulla facilisi. Vestibulum quis congue ex, ac feugiat purus. Sed sed interdum sem, eu auctor magna. Integer eget augue justo. Vestibulum in convallis lectus, non pretium nibh. Vestibulum porta fringilla odio, eget ornare arcu vehicula at. Curabitur consequat tristique condimentum. Nulla sit amet lobortis tellus, sit amet porttitor erat. Sed feugiat rhoncus sagittis.',
  'Duis eleifend lacus nisl, in accumsan lorem accumsan ac. Quisque ligula dolor, mattis ut justo eget, hendrerit pellentesque ex. Sed eros erat, maximus non mollis nec, euismod a lacus. Nam ante ligula, efficitur vitae bibendum id, condimentum sed ipsum. Vivamus maximus fermentum fringilla. Maecenas aliquet semper auctor. Morbi pharetra ipsum urna, ac viverra eros hendrerit et. In hac habitasse platea dictumst.',
]

def section(request, sectionNumber: str):
  if not (1 <= sectionNumber <= 3):
    return Http404('No such section.')
  
  return HttpResponse(texts[sectionNumber - 1])