from django.db import models
# Create your models here.


class Posts(models.Model):
    image = models.TextField(default="")
    title = models.TextField(default="")
    subtitle = models.TextField(default="")
    shared_by = models.TextField(default="")
    content_image = models.TextField(default="")
    content_link = models.TextField(default="")
    content_summary = models.TextField(default="")
    last_update = models.DateTimeField(auto_now=True)
