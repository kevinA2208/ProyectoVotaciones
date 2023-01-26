from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from GlobalApi.models import PuestoVotacion, Votantes, User
from GlobalApi.serializers.general_serializers import PuestoVotacionSerializer, PuestoVotacionListSerializer
from apscheduler.schedulers.background import BackgroundScheduler
from GlobalApi.authentication.authentication_mixins import Authentication


scheduler = BackgroundScheduler({'apscheduler.job_defaults.max_instances': 1})



class PuestoVotacionViewSet(Authentication, viewsets.ModelViewSet):
    serializer_class = PuestoVotacionSerializer

    def get_queryset(self, pk=None):
        if pk == None:
            user_active = self.user
            doc_user_active = user_active.doc
            user = User.objects.filter(doc = doc_user_active).first()
            if user.is_staff:
                return PuestoVotacionSerializer.Meta.model.objects.all()
            else:
                pass

    def create(self, request):
        user_active = self.user
        doc_user_active = user_active.doc
        user = User.objects.filter(doc = doc_user_active).first()
        if user.is_staff:
            serializer = PuestoVotacionSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'data' : serializer.data, 'message':'Se ha creado el Puesto de Votacion correctamente'}, status= status.HTTP_201_CREATED)
        else:
            return Response({"message":"El usuario no tiene permisos para crear puestos de votación"},status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        user_active = self.user
        doc_user_active = user_active.doc
        user = User.objects.filter(doc = doc_user_active).first()
        if user.is_staff:
            puesto_votacion = PuestoVotacion.objects.filter(id_puesto_votacion = pk).first()
            serializer = PuestoVotacionSerializer(puesto_votacion, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'data' : serializer.data, 'message':'Se ha actualizado el Puesto de Votacion correctamente'}, status= status.HTTP_201_CREATED)
        else:
            return Response({"message":"El usuario no tiene permisos para actualizar puestos de votación"},status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        user_active = self.user
        doc_user_active = user_active.doc
        user = User.objects.filter(doc = doc_user_active).first()
        if user.is_staff:
            puesto_votacion = PuestoVotacion.objects.filter(id_puesto_votacion = pk).first()
            puesto_votacion.delete()
            return Response({'message':'Puesto de Votacion eliminado correctamente'}, status= status.HTTP_200_OK)
        else:
            return Response({"message":"El usuario no tiene permisos para eliminar puestos de votación"},status=status.HTTP_401_UNAUTHORIZED)


    #Validacion para actualizar el campo cantidad de votantes que tiene cada puesto de votacion
    @scheduler.scheduled_job('interval', seconds=60)
    def validacion_votantes_lider():
        puestos_votacion = PuestoVotacion.objects.all()
        for puesto in puestos_votacion:
            votantes = Votantes.objects.filter(puesto_votacion = puesto.id_puesto_votacion)
            cant_votantes = votantes.count()
            if cant_votantes == puesto.cantidad_votantes:
                pass
            else:
                puesto.cantidad_votantes = cant_votantes
                puesto.save()
                
    
    scheduler.start()