from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from GlobalApi.models import Municipios, Departamentos, Votantes
from GlobalApi.serializers.general_serializers import MunicipiosSerializer, DepartamentosSerializer, MunicipiosListSerializer
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler({'apscheduler.job_defaults.max_instances': 1})

class MunicipiosViewSet(viewsets.ModelViewSet):
    serializer_class = MunicipiosListSerializer

    def get_queryset(self, pk=None):
        if pk == None:
            return MunicipiosSerializer.Meta.model.objects.all()
        return Municipios.objects.filter(id_municipio = pk).first()
    
    def create(self, request):
        serializer = MunicipiosSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data' : serializer.data, 'message':'Se ha creado el Municipio correctamente'}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        municipio = Municipios.objects.filter(id_municipio = pk).first()
        serializer = MunicipiosSerializer(municipio, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data' : serializer.data, 'message':'Se ha actualizado el Municipio correctamente'}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        municipio = Municipios.objects.filter(id_municipio = pk).first()
        municipio.delete()
        return Response({'message':'Municipio eliminado correctamente'}, status= status.HTTP_200_OK)

class DepartamentosViewSet(viewsets.ModelViewSet):
    serializer_class = DepartamentosSerializer

    def get_queryset(self, pk=None):
        if pk == None:
            return DepartamentosSerializer.Meta.model.objects.all()
        return Departamentos.objects.filter(id_departamento = pk).first()

    def create(self, request):
        serializer = DepartamentosSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data' : serializer.data, 'message':'Se ha creado el Departamento correctamente'}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk):
        departamento = Departamentos.objects.filter(id_departamento = pk).first()
        serializer = DepartamentosSerializer(departamento, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data' : serializer.data, 'message':'Se ha actualizado el Departamento correctamente'}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        departamento = Departamentos.objects.filter(id_departamento = pk).first()
        departamento.delete()
        return Response({'message':'Departamento eliminado correctamente'}, status= status.HTTP_200_OK)
        

    
    #Validacion para actualizar el campo cantidad de votantes que tiene cada municipio
    @scheduler.scheduled_job('interval', seconds=60)
    def validacion_votantes_municipio():
        municipios = Municipios.objects.all()
        for municipio in municipios:
            votantes = Votantes.objects.filter(municipio_votante = municipio.id_municipio)
            cant_votantes = votantes.count()
            if cant_votantes == municipio.cantidad_votantes:
                pass
            else:
                municipio.cantidad_votantes = cant_votantes
                municipio.save()

    scheduler.start()