from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from GlobalApi.models import Votantes
from GlobalApi.serializers.general_serializers import VotantesSerializer, LiderSerializer

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

class TotalVotantesViewSet(viewsets.GenericViewSet):

    def list(self, request):
        votantes = Votantes.objects.all()
        if votantes:
            cantidad_votantes = str(votantes.count())
            print(cantidad_votantes)
            return Response({'message':'Hay un total de ' + cantidad_votantes + " votantes en el sistema!"}, status= status.HTTP_200_OK)


""" class TotalVotantesPorLider(viewsets.ModelViewSet):
    serializer_class = LiderSerializer

    def get_queryset(self, pk=None):
        if pk == None:
            return LiderSerializer.Meta.model.objects.all()
        return LiderSerializer.Meta.model.objects.filter(doc_lider = pk).first()

    def list(self, request, pk=None):
        if(pk == None):
            return Response({'message':'Ingrese el documento del lider que desea consultar sus votantes en la url'}, status= status.HTTP_404_NOT_FOUND)
        else:
            lider = LiderSerializer.Meta.model.objects.filter(doc_lider = pk).first()
            if lider:
                votantes = Votantes.objects.filter(lider_votante = lider)
                cantidad_votantes = str(votantes.count())
                return Response({'message':'El lider ' + lider.nombres_lider + " tiene un total de " + cantidad_votantes + " votantes!"}, status= status.HTTP_200_OK)
            else:
                return Response({'message':'No se ha encontrado el lider'}, status= status.HTTP_404_NOT_FOUND) """

        
        

        
