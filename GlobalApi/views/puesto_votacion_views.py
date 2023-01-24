from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from GlobalApi.models import PuestoVotacion
from GlobalApi.serializers.general_serializers import PuestoVotacionSerializer


class PuestoVotacionViewSet(viewsets.ModelViewSet):
    serializer_class = PuestoVotacionSerializer

    def get_queryset(self, pk=None):
        if pk == None:
            return PuestoVotacionSerializer.Meta.model.objects.all()
        return PuestoVotacion.objects.filter(id_puesto_votacion = pk).first()

    def create(self, request):
        serializer = PuestoVotacionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data' : serializer.data, 'message':'Se ha creado el Puesto de Votacion correctamente'}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        puesto_votacion = PuestoVotacion.objects.filter(id_puesto_votacion = pk).first()
        serializer = PuestoVotacionSerializer(puesto_votacion, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data' : serializer.data, 'message':'Se ha actualizado el Puesto de Votacion correctamente'}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        puesto_votacion = PuestoVotacion.objects.filter(id_puesto_votacion = pk).first()
        puesto_votacion.delete()
        return Response({'message':'Puesto de Votacion eliminado correctamente'}, status= status.HTTP_200_OK)

