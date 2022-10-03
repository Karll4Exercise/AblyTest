from django.conf.urls import url
from django.urls import include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.MobileAuthViews, basename='member')

urlpatterns = [
    url(r'^', include(router.urls)),
]

