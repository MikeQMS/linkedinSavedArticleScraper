from django.shortcuts import render
from . import scrapper
from rest_framework import viewsets
from .serializers import PostsSerializer
from .models import Posts
from django.shortcuts import redirect


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
