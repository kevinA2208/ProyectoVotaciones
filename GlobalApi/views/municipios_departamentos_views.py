from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from GlobalApi.models import Municipios, Departamentos, Votantes, User
from GlobalApi.serializers.general_serializers import MunicipiosSerializer, DepartamentosSerializer, MunicipiosListSerializer
from apscheduler.schedulers.background import BackgroundScheduler
from GlobalApi.authentication.authentication_mixins import Authentication

scheduler = BackgroundScheduler({'apscheduler.job_defaults.max_instances': 1})

class MunicipiosViewSet(Authentication, viewsets.ModelViewSet):
    serializer_class = MunicipiosSerializer

    def get_queryset(self, pk=None):
        user_active = self.user
        doc_user_active = user_active.doc
        user = User.objects.filter(doc = doc_user_active).first()
        if user.is_staff:
            if pk == None:
                return MunicipiosSerializer.Meta.model.objects.all()
        else:
            pass
    
    def create(self, request):
        user_active = self.user
        doc_user_active = user_active.doc
        user = User.objects.filter(doc = doc_user_active).first()
        if user.is_staff:
            serializer = MunicipiosSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'data' : serializer.data, 'message':'Se ha creado el Municipio correctamente'}, status= status.HTTP_201_CREATED)
        else:
            return Response({"message":"El usuario no tiene permisos para crear municipios"},status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        user_active = self.user
        doc_user_active = user_active.doc
        user = User.objects.filter(doc = doc_user_active).first()
        if user.is_staff:
            municipio = Municipios.objects.filter(id_municipio = pk).first()
            serializer = MunicipiosSerializer(municipio, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'data' : serializer.data, 'message':'Se ha actualizado el Municipio correctamente'}, status= status.HTTP_201_CREATED)
        else:
            return Response({"message":"El usuario no tiene permisos para actualizar municipios"},status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        user_active = self.user
        doc_user_active = user_active.doc
        user = User.objects.filter(doc = doc_user_active).first()
        if user.is_staff:
            municipio = Municipios.objects.filter(id_municipio = pk).first()
            municipio.delete()
            return Response({'message':'Municipio eliminado correctamente'}, status= status.HTTP_200_OK)
        else:
            return Response({"message":"El usuario no tiene permisos para eliminar municipios"},status=status.HTTP_401_UNAUTHORIZED)

class DepartamentosViewSet(Authentication, viewsets.ModelViewSet):
    serializer_class = DepartamentosSerializer

    def get_queryset(self, pk=None):
        user_active = self.user
        doc_user_active = user_active.doc
        user = User.objects.filter(doc = doc_user_active).first()
        if user.is_staff:
            if pk == None:
                return DepartamentosSerializer.Meta.model.objects.all()
        else:
            pass

    def create(self, request):
        user_active = self.user
        doc_user_active = user_active.doc
        user = User.objects.filter(doc = doc_user_active).first()
        if user.is_staff:
            serializer = DepartamentosSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'data' : serializer.data, 'message':'Se ha creado el Departamento correctamente'}, status= status.HTTP_201_CREATED)
        else:
            return Response({"message":"El usuario no tiene permisos para crear departamentos"},status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk):
        user_active = self.user
        doc_user_active = user_active.doc
        user = User.objects.filter(doc = doc_user_active).first()
        if user.is_staff:
            departamento = Departamentos.objects.filter(id_departamento = pk).first()
            serializer = DepartamentosSerializer(departamento, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'data' : serializer.data, 'message':'Se ha actualizado el Departamento correctamente'}, status= status.HTTP_201_CREATED)
        else:
            return Response({"message":"El usuario no tiene permisos para actualizar departamentos"},status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        user_active = self.user
        doc_user_active = user_active.doc
        user = User.objects.filter(doc = doc_user_active).first()
        if user.is_staff:
            departamento = Departamentos.objects.filter(id_departamento = pk).first()
            departamento.delete()
            return Response({'message':'Departamento eliminado correctamente'}, status= status.HTTP_200_OK)
        else:
            return Response({"message":"El usuario no tiene permisos para eliminar departamentos"},status=status.HTTP_401_UNAUTHORIZED)
        
    
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