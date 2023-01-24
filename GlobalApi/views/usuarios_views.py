from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from GlobalApi.models import Lider, Admin
from GlobalApi.serializers.general_serializers import LiderSerializer, AdminSerializer

class LiderViewSet(viewsets.ModelViewSet):
    serializer_class = LiderSerializer

    def get_queryset(self, pk=None):
        if pk == None:
            return LiderSerializer.Meta.model.objects.all()
        return Lider.objects.filter(id_grado = pk).first()

    def create(self, request):
        serializer = LiderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data' : serializer.data, 'message':'Se ha creado el Lider correctamente'}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        lider = Lider.objects.filter(id_lider = pk).first()
        serializer = LiderSerializer(lider, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data' : serializer.data, 'message':'Se ha actualizado el Lider correctamente'}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        lider = Lider.objects.filter(id_lider = pk).first()
        lider.delete()
        return Response({'message':'Lider eliminado correctamente'}, status= status.HTTP_200_OK)

class AdminViewSet(viewsets.ModelViewSet):
    serializer_class = AdminSerializer

    def get_queryset(self, pk=None):
        if pk == None:
            return AdminSerializer.Meta.model.objects.all()
        return Admin.objects.filter(id_admin = pk).first()

    def create(self, request):
        serializer = AdminSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data' : serializer.data, 'message':'Se ha creado el Admin correctamente'}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        admin = Admin.objects.filter(id_admin = pk).first()
        serializer = AdminSerializer(admin, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data' : serializer.data, 'message':'Se ha actualizado el Admin correctamente'}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        admin = Admin.objects.filter(id_admin = pk).first()
        admin.delete()
        return Response({'message':'Admin eliminado correctamente'}, status= status.HTTP_200_OK)