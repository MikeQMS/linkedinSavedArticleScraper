from django.urls import include, path
from rest_framework import routers
from . import views
from django.views.decorators.csrf import csrf_exempt

router = routers.DefaultRouter()
router.register(r'posts', views.PostsViewSet)

#URL Conf
urlpatterns = [
    path('', views.start_page, name = "home"),
    path('api/', include(router.urls)),
    path('update/', views.get_savedfeed, name="update"),
    path('search', csrf_exempt(views.search), name="search")
]

