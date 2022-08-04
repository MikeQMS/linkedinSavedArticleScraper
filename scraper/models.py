from django.db import models
from django import forms


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


class LoginForm(forms.Form):
    your_name = forms.CharField(label='Login Name', max_length=100)
    your_password = forms.CharField(label='Password', max_length=256, widget=forms.PasswordInput(render_value=True))
