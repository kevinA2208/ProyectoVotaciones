from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from GlobalApi.models import Lider, User, Votantes
from GlobalApi.serializers.general_serializers import LiderSerializer, UsuarioSerializer, LiderListSerializer
from datetime import timedelta, date
from apscheduler.schedulers.background import BackgroundScheduler
from GlobalApi.authentication.authentication_mixins import Authentication

scheduler = BackgroundScheduler({'apscheduler.job_defaults.max_instances': 1})

#El viewset de los usuarios solo conecta los usuarios lideres con la autenticación, al momento de crear un lider, se crea el usuario
#y con los datos del usuario se hace el proceso de autenticacion, que viene conectado con un lider
#el super user no pasa por esto, ya que se crea por consola
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

#Viewset para gestionar un lider, con validaciones, si se crea un lider, se crea el usuario del lider, este usuario no es staff
class LiderViewSet(Authentication, viewsets.ModelViewSet):
    serializer_class = LiderSerializer

    def get_queryset(self, pk=None):
        if pk == None:
            #Validacion para que los usuarios lideres no tengan acceso a la base de datos de lideres ni la puedan modificar
            user_active = self.user
            doc_user_active = user_active.doc
            user = User.objects.filter(doc = doc_user_active).first()
            if user.is_staff:
                return LiderListSerializer.Meta.model.objects.all()
            else:
                pass
          

    def create(self, request):
        #Validacion para que los usuarios lideres no tengan acceso a la base de datos de lideres ni la puedan modificar
        user_active = self.user
        doc_user_active = user_active.doc
        user = User.objects.filter(doc = doc_user_active).first()
        if user.is_staff:
            usuario_serializer = UsuarioSerializer(data=request.data['doc_lider'])

            data_lider = request.data

            data_usuario = request.data['doc_lider']

            #Validación si existe un usuario con ese documento
            if usuario_serializer.is_valid():
                user_doc_validated = usuario_serializer.validated_data['doc']
                user_existente = User.objects.filter(doc = user_doc_validated).first()
                if user_existente:
                    pass
                else:
                    usuario_serializer.save()
                    

            data_lider['doc_lider'] = data_usuario['doc']

            lider_serializer = LiderSerializer(data=data_lider)

            #Validacion para que los lideres no tengan el mismo documento
            if lider_serializer.is_valid():
                user_lider_documento = lider_serializer.validated_data['doc_lider']
                user_doc = user_lider_documento.doc
                lider_existente = Lider.objects.filter(doc_lider = user_doc).first()
                if lider_existente:
                    return Response({'message':'Ya existe un lider con el documento ' + user_doc}, status= status.HTTP_400_BAD_REQUEST)
                else:
                    lider_serializer.save()
                    return Response({'data' : lider_serializer.data, 'message':'Se ha creado el Lider correctamente'}, status= status.HTTP_201_CREATED)
        else:
            return Response({"message":"El usuario no tiene permisos para crear lideres"},status=status.HTTP_401_UNAUTHORIZED)
        return Response(lider_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        user_active = self.user
        doc_user_active = user_active.doc
        user = User.objects.filter(doc = doc_user_active).first()
        if user.is_staff:
            lider = Lider.objects.filter(id_lider = pk).first()

            primer_documento = lider.doc_lider.doc
            print(primer_documento)
            request.data['doc_lider'] = primer_documento

            data_lider = request.data
            
            data_usuario = request.data['doc_lider']

            doc_usuario = data_usuario

            usuario = User.objects.filter(doc = doc_usuario).first()

            data_lider['doc_lider'] = doc_usuario





            usuario_serializer = UsuarioSerializer(usuario, data=data_usuario, partial = True)

            lider_serializer = LiderSerializer(lider, data=data_lider)
            

            if usuario_serializer.is_valid():
                usuario_serializer.save()
            

            if lider_serializer.is_valid():
                lider_serializer.save()
                return Response({'data' : lider_serializer.data, 'message':'Se ha actualizado el Lider correctamente'}, status= status.HTTP_201_CREATED)
        else:
            return Response({"message":"El usuario no tiene permisos para actualizar lideres"},status=status.HTTP_401_UNAUTHORIZED)
        return Response(lider_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        user_active = self.user
        doc_user_active = user_active.doc
        user = User.objects.filter(doc = doc_user_active).first()
        if user.is_staff:
            lider = Lider.objects.filter(id_lider = pk).first()
            
            doc_lider = lider.doc_lider.doc
            usuario = User.objects.filter(doc = doc_lider).first()

            usuario.delete()
            
            lider.delete()
            return Response({'message':'Lider eliminado correctamente'}, status= status.HTTP_200_OK)
        else:
            return Response({"message":"El usuario no tiene permisos para actualizar lideres"},status=status.HTTP_401_UNAUTHORIZED)


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
        