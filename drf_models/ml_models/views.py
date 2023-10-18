from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets,status
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import MlModel, ModelTag
from .serializers import MLModelSerializer, TagSerializer, MLModelResultSerializer
from .ml_models_utils import calculate_diagnose_disease


class MLModelViewSet(viewsets.ModelViewSet):
    """
    Вывести все, одну, удалить, обновить модели
    """
    serializer_class = MLModelSerializer
    queryset = MlModel.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data
        new_model = MlModel.objects.create(title=data['title'],
                                           description=data['description'],
                                           inputs=data['inputs'])
        new_model.save()

        for tag in data['tags']:
            tag_obj = ModelTag.objects.get(tag=tag['tag'])
            new_model.tags.add(tag_obj)

        serializer = MLModelSerializer(new_model)
        return Response(serializer.data)

    @action(detail=True,
            methods=['put'])
    def calculate(self, request, *args, **kwargs):
        ml_model = self.get_object()
        print(ml_model.ml_model)
        inputs = request.data['model_inputs']
        result = calculate_diagnose_disease(ml_model, inputs)
        if result.any():
            return Response({'Results': result})
        else:
            return Response({'Error': 'Мало вводных'})


class TagAPIList(generics.ListCreateAPIView):
    serializer_class = TagSerializer
    queryset = ModelTag.objects.all()


class TagAPICreate(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TagSerializer
    queryset = ModelTag.objects.all()


class MLModelResults(APIView):
    """
    Получить результаты конкретной модели МО
    """
    def get_object(self, pk):
        return get_object_or_404(MlModel, pk=pk)

    def post(self, request, pk):
        ml_model = self.get_object(pk)
        serializer = MLModelResultSerializer(ml_model, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)