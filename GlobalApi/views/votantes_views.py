from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from GlobalApi.models import Votantes
from GlobalApi.serializers.general_serializers import VotantesSerializer

class VotantesViewSet(viewsets.ModelViewSet):
    serializer_class = VotantesSerializer

    def get_queryset(self, pk=None):
        if pk == None:
            return VotantesSerializer.Meta.model.objects.all()
        return Votantes.objects.filter(id_votante = pk).first()

    def create(self, request):
        serializer = VotantesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data' : serializer.data, 'message':'Se ha creado el Votante correctamente'}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        votante = Votantes.objects.filter(id_votante = pk).first()
        serializer = VotantesSerializer(votante, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data' : serializer.data, 'message':'Se ha actualizado el Votante correctamente'}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        votante = Votantes.objects.filter(id_votante = pk).first()
        votante.delete()
        return Response({'message':'Votante eliminado correctamente'}, status= status.HTTP_200_OK)