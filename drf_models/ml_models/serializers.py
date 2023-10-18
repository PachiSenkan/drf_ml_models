from rest_framework import serializers

from .models import MlModel, ModelTag
from .services import *


class MLModelResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = MlModel
        fields = ['ml_model']


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = ModelTag
        fields = ['id', 'tag']


class MLModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MlModel
        fields = ['title', 'tags', 'description', 'ml_model', 'inputs']
        extra_kwargs = {'ml_model': {'write_only': True}}
        depth = 0
