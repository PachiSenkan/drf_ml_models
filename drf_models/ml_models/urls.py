from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(r'api/v1/models', MLModelViewSet, basename='models')


urlpatterns = [
    path('models/', MLModelList.as_view()),
    path('models/tags/<int:pk>', TagAPICreate.as_view()),
    path('models/tags/', TagAPIList.as_view()),
    path('users/', UserList.as_view()),
    path('users/<int:pk>/', UserDetail.as_view()),
]

urlpatterns += router.urls
