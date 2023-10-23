from rest_framework import serializers
from django.contrib.auth.models import User

from .models import MlModel, ModelTag
from .services import *


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = ModelTag
        fields = ['id', 'tag']


class MLModelSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.username')
    uploaded = serializers.DateTimeField(format='%d/%m/%Y %H:%M:%S')

    class Meta:
        model = MlModel
        fields = ['title', 'tags', 'description', 'owner', 'uploaded', 'ml_model', 'inputs']
        extra_kwargs = {'ml_model': {'write_only': True}}
        depth = 1


class UserSerializer(serializers.ModelSerializer):
    ml_models = serializers.PrimaryKeyRelatedField(many=True, queryset=MlModel.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'ml_models']