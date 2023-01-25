from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from GlobalApi.models import Lider, User, Votantes
from GlobalApi.serializers.general_serializers import LiderSerializer, UsuarioSerializer, LiderListSerializer
from datetime import timedelta, date
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler({'apscheduler.job_defaults.max_instances': 1})

class UsuariosViewSet(viewsets.ModelViewSet):
    serializer_class = UsuarioSerializer
    
    def get_queryset(self, pk=None):
        if pk == None:
            return UsuarioSerializer.Meta.model.objects.all()
        return User.objects.filter(doc = pk).first()

    def create(self, request):
        serializer = UsuarioSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data' : serializer.data, 'message':'Se ha agregado el usuario correctamente'}, status= status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        usuario = User.objects.filter(doc = pk).first()
        serializer = UsuarioSerializer(usuario, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data' : serializer.data, 'message':'Usuario actualizado correctamente'}, status= status.HTTP_200_OK)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk):
        usuario = User.objects.filter(doc = pk).first()
        serializer = UsuarioSerializer(usuario, data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'data' : serializer.data, 'message':'Usuario actualizado correctamente'}, status= status.HTTP_200_OK)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        usuario = User.objects.filter(doc = pk).first()
        usuario.delete()
        return Response({'message':'Usuario eliminado correctamente'}, status= status.HTTP_200_OK)


class LiderViewSet(viewsets.ModelViewSet):
    serializer_class = LiderSerializer


    def get_queryset(self, pk=None):
        if pk == None:
            return LiderListSerializer.Meta.model.objects.all()
        return Lider.objects.filter(id_lider = pk).first()

    def create(self, request):
        usuario_serializer = UsuarioSerializer(data=request.data['doc_lider'])

        data_lider = request.data

        data_usuario = request.data['doc_lider']


        data_lider['doc_lider'] = data_usuario['doc']

        lider_serializer = LiderSerializer(data=data_lider)

        if usuario_serializer.is_valid():
            usuario_serializer.save()
            print("Usuario creado correctamente")

        if lider_serializer.is_valid():
            lider_serializer.save()
            return Response({'data' : lider_serializer.data, 'message':'Se ha creado el Lider correctamente'}, status= status.HTTP_201_CREATED)
        return Response(lider_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        lider = Lider.objects.filter(id_lider = pk).first()

        data_lider = request.data
        
        data_usuario = request.data['doc_lider']

        doc_usuario = data_usuario

        usuario = User.objects.filter(doc = doc_usuario).first()

        data_lider['doc_lider'] = doc_usuario

        usuario_serializer = UsuarioSerializer(usuario, data=data_usuario, partial = True)

        lider_serializer = LiderSerializer(lider, data=data_lider)

        if usuario_serializer.is_valid():
            usuario_serializer.save()
            print("Usuario actualizado correctamente")

        if lider_serializer.is_valid():
            lider_serializer.save()
            return Response({'data' : lider_serializer.data, 'message':'Se ha actualizado el Lider correctamente'}, status= status.HTTP_201_CREATED)
        return Response(lider_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        
        lider = Lider.objects.filter(id_lider = pk).first()
        
        doc_lider = lider.doc_lider.doc
        usuario = User.objects.filter(doc = doc_lider).first()

        usuario.delete()
        print("Usuario eliminado correctamente")
        lider.delete()
        return Response({'message':'Lider eliminado correctamente'}, status= status.HTTP_200_OK)


    #Validacion para actualizar el campo cantidad de votantes que tiene cada lider
    @scheduler.scheduled_job('interval', seconds=60)
    def validacion_votantes_lider():
        lideres = Lider.objects.all()
        for lider in lideres:
            votantes = Votantes.objects.filter(lider_id = lider.id_lider)
            cant_votantes = votantes.count()
            if cant_votantes == lider.cantidad_votantes:
                pass
            else:
                lider.cantidad_votantes = cant_votantes
                lider.save()

    scheduler.start()
        