# serializers.py
from rest_framework import serializers
from .models import Posts


class PostsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Posts
        fields = ('image', 'title', 'subtitle', 'shared_by', 'content_image', 'content_summary', 'content_link', 'last_update')
