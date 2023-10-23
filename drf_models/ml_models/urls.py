from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import MLModelViewSet, TagAPICreate, TagAPIList, UserList, UserDetail

router = DefaultRouter()
router.register(r'models', MLModelViewSet, basename='models')


urlpatterns = [
    path('models/tags/<int:pk>', TagAPICreate.as_view()),
    path('models/tags/', TagAPIList.as_view()),
    path('users/', UserList.as_view()),
    path('users/<int:pk>/', UserDetail.as_view()),
]

urlpatterns += router.urls
