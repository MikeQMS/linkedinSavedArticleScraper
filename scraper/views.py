from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from . import scraper
from rest_framework import viewsets
from .serializers import PostsSerializer
from .models import Posts, LoginForm
# from django.shortcuts import redirect
import json
from django.http import JsonResponse


# Filter data by search text
def search(request):
    if request.method == 'POST':
        search_string=json.loads(request.body).get('searchText')
        result = Posts.objects.filter(title__icontains=search_string) | Posts.objects.filter(
                                      subtitle__icontains=search_string) | Posts.objects.filter(
                                      shared_by__icontains=search_string) | Posts.objects.filter(
                                      content_summary__icontains=search_string) | Posts.objects.filter(
                                      content_link__icontains=search_string)
        data = result.values()
        return JsonResponse(list(data), safe=False)


# Query database for all posts, if non exist load start scraper
def start_page(request):
    queryset = Posts.objects.all()
    form = LoginForm()
    # if not queryset:
    #     scraper.run(False)
    return render(request, "index.html", {'queryset' : queryset, 'form' : form})


# update the database
@csrf_exempt
def get_savedfeed(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            scraper.run(False, request.POST)
            queryset = Posts.objects.all()
            return render(request, "index.html", {'queryset': queryset, 'form': form})
        else:
            form = LoginForm()
    return render(request, "index.html", {'form': form})


# creates api
class PostsViewSet(viewsets.ModelViewSet):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer
