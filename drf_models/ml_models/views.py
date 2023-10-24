from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework import generics, viewsets,status
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response


from .models import MlModel, ModelTag
from .serializers import MLModelSerializer, TagSerializer, UserSerializer
from .ml_models_utils import calculate_diagnose_disease

order_dict = {'desc': '-',
              'asc': ''}


class MLModelList(generics.ListCreateAPIView):
    serializer_class = MLModelSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        print(data)
        print(self.request.user)
        new_model = MlModel.objects.create(title=data['title'],
                                           description=data['description'],
                                           inputs=data['inputs'],
                                           owner=self.request.user)
        new_model.save()
        for tag in data['tags']:
            tag_obj = ModelTag.objects.get(name=tag['name'])
            new_model.tags.add(tag_obj)

        serializer = MLModelSerializer(new_model)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        if 'sort_by' in self.request.query_params:
            order = self.request.query_params['sort_order']
            order_field = f'{order_dict[order]}{self.request.query_params["sort_by"]}'
            query = MlModel.objects.order_by(order_field)
            return query

        return MlModel.objects.all()


class MLModelDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MlModel.objects.all()
    serializer_class = MLModelSerializer


class MLModelViewSet(viewsets.ModelViewSet):
    """
    Вывести все, одну, удалить, обновить модели
    """
    serializer_class = MLModelSerializer
    queryset = MlModel.objects.all()

    def perform_create(self, serializer):
        print(f'PERFORM CREATE{self.request.user}')
        serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        data = request.data
        print(data)
        print(self.request.user)
        new_model = MlModel.objects.create(title=data['title'],
                                           description=data['description'],
                                           inputs=data['inputs'])
        new_model.save()
        for tag in data['tags']:
            tag_obj = ModelTag.objects.get(tag=tag['tag'])
            new_model.tags.add(tag_obj)

        serializer = MLModelSerializer(new_model)
        serializer.save(owner=self.request.user)
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


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
