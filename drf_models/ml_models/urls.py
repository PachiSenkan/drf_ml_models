from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import MLModelViewSet, MLModelResults, TagAPICreate, TagAPIList

router = DefaultRouter()
router.register(r'models', MLModelViewSet, basename='models')


urlpatterns = [
    path('models/tags/<int:pk>', TagAPICreate.as_view()),
    path('models/tags/', TagAPIList.as_view()),
    path('models/results/<int:pk>', MLModelResults.as_view())
]

urlpatterns += router.urls
