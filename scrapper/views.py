from django.shortcuts import render
from . import scrapper
from rest_framework import viewsets
from .serializers import PostsSerializer
from .models import Posts
from django.shortcuts import redirect
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


# Query database for all posts, if non exist load start scrapper
def start_page(request):
    queryset = Posts.objects.all()
    if not queryset:
        scrapper.run(False)
    return render(request, "index.html", {'queryset' : queryset})


# update the database
def get_savedfeed(request):
    scrapper.run(False)
    return redirect("/")


# creates api
class PostsViewSet(viewsets.ModelViewSet):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer
