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
    #model_result = serializers.SerializerMethodField('count')
    #model_input_data = serializers.SerializerMethodField('get_input_data')
    #
    #def count(self, obj):
    #    return count(obj.ml_model)
    #
    #def get_input_data(self, obj):
    #    return get_input_data(obj.ml_model)
    #
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = MlModel
        fields = ['title', 'tags', 'description', 'ml_model', 'inputs']
        extra_kwargs = {'ml_model': {'write_only': True}}
        depth = 0


