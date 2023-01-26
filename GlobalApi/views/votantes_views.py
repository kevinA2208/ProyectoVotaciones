from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from GlobalApi.models import Votantes, User, Lider
from GlobalApi.serializers.general_serializers import VotantesSerializer, VotantesListSerializer
from GlobalApi.authentication.authentication_mixins import Authentication

class VotantesViewSet(Authentication, viewsets.ModelViewSet):
    serializer_class = VotantesSerializer

    def get_queryset(self, pk=None):
        if pk == None:
            user_active = self.user
            doc_user_active = user_active.doc
            user = User.objects.filter(doc = doc_user_active).first()
            if user.is_staff:
                return VotantesSerializer.Meta.model.objects.all()
            else:
                lider = Lider.objects.filter(doc_lider = doc_user_active).first()
                votantes_lider = Votantes.objects.filter(lider_id = lider.id_lider)
                return votantes_lider

    def create(self, request):
        user_active = self.user
        doc_user_active = user_active.doc
        user = User.objects.filter(doc = doc_user_active).first()
        if user.is_staff:
            serializer = VotantesSerializer(data=request.data)
            if serializer.is_valid():
                #Validacion de que no exista un votante con el mismo documento al crear un votante
                documento_votante = serializer.validated_data['doc_votante']
                if documento_votante:
                    votante = Votantes.objects.filter(doc_votante = documento_votante).first()
                    if votante:
                        return Response({'message':'Ya existe un votante con el documento ' + documento_votante}, status= status.HTTP_400_BAD_REQUEST)
                    else:
                        serializer.save()
                        return Response({'data' : serializer.data, 'message':'Se ha creado el Votante correctamente'}, status= status.HTTP_201_CREATED) 
        else:
            lider = Lider.objects.filter(doc_lider = doc_user_active).first()
            #Si el usuario logueado es un lider, el id del lider del votante se pone automaticamente como el del usuario activo
            id_lider = lider.id_lider
            request.data['lider_id'] = id_lider
            
            serializer = VotantesSerializer(data=request.data)
            if serializer.is_valid():
                #Validacion de que no exista un votante con el mismo documento al crear un votante
                documento_votante = serializer.validated_data['doc_votante']
                if documento_votante:
                    votante = Votantes.objects.filter(doc_votante = documento_votante).first()
                    if votante:
                        return Response({'message':'Ya existe un votante con el documento ' + documento_votante}, status= status.HTTP_400_BAD_REQUEST)
                    else:
                        serializer.save()
                        return Response({'data' : serializer.data, 'message':'Se ha creado el Votante correctamente'}, status= status.HTTP_201_CREATED) 

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        user_activo = self.user
        doc_user_activo = user_activo.doc
        user = User.objects.filter(doc = doc_user_activo).first()
        if user.is_staff:
            votante = Votantes.objects.filter(id_votante = pk).first()
            serializer = VotantesSerializer(votante, data=request.data)
            if serializer.is_valid():
                #Validacion de que no exista un votante con el mismo documento al actualizar un votante
                documento_votante = serializer.validated_data['doc_votante']
                if documento_votante == votante.doc_votante:
                    serializer.save()
                    return Response({'data' : serializer.data, 'message':'Se ha actualizado el Votante correctamente'}, status= status.HTTP_201_CREATED)
                if documento_votante:
                    votante = Votantes.objects.filter(doc_votante = documento_votante).first()
                    if votante:
                        return Response({'message':'Ya existe un votante con el documento ' + documento_votante}, status= status.HTTP_400_BAD_REQUEST)
                    else:
                        serializer.save()
                        return Response({'data' : serializer.data, 'message':'Se ha actualizado el Votante correctamente'}, status= status.HTTP_201_CREATED)
        else:
            lider_activo = Lider.objects.filter(doc_lider = doc_user_activo).first()
            votante = Votantes.objects.filter(id_votante = pk).first()

            #Validación para que no se le pueda cambiar el id del lider al votante
            primer_lider_id = votante.lider_id
            request.data['lider_id'] = primer_lider_id.id_lider

            serializer = VotantesSerializer(votante, data=request.data)

            if serializer.is_valid():
                #validacion para que el lider logueado solo pueda actualizar sus votantes
                votante_lider = serializer.validated_data['lider_id']
                if votante_lider == lider_activo:
                    #Validacion de que no exista un votante con el mismo documento al crear un votante
                    documento_votante = serializer.validated_data['doc_votante']

                    #Si al actualizar tiene su mismo documento, que lo actualice correctamente
                    if documento_votante == votante.doc_votante:
                        serializer.save()
                        return Response({'data' : serializer.data, 'message':'Se ha actualizado el Votante correctamente'}, status= status.HTTP_201_CREATED)

                    if documento_votante:
                        votante = Votantes.objects.filter(doc_votante = documento_votante).first()
                        #Si al actualizar tiene el documento de otro votante, no le permita actualizar
                        if votante:
                            return Response({'message':'Ya existe un votante con el documento ' + documento_votante}, status= status.HTTP_400_BAD_REQUEST)

                        else:
                            serializer.save()
                            return Response({'data' : serializer.data, 'message':'Se ha actualizado el Votante correctamente'}, status= status.HTTP_201_CREATED)   
                                     
                else:
                    return Response({'message':'No tiene permiso para actualizar este Votante'}, status= status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        user_active = self.user
        doc_user_active = user_active.doc
        user = User.objects.filter(doc = doc_user_active).first()
        if user.is_staff:
            votante = Votantes.objects.filter(id_votante = pk).first()
            votante.delete()
            return Response({'message':'Votante eliminado correctamente'}, status= status.HTTP_200_OK)
        else:
            lider_activo = Lider.objects.filter(doc_lider = doc_user_active).first()
            votante = Votantes.objects.filter(id_votante = pk).first()
            if votante.lider_id == lider_activo:
                votante.delete()
                return Response({'message':'Votante eliminado correctamente'}, status= status.HTTP_200_OK)
            else:
                return Response({"message":"El usuario no tiene permisos para eliminar votantes"},status=status.HTTP_401_UNAUTHORIZED)

class TotalVotantesViewSet(Authentication ,viewsets.GenericViewSet):

    def list(self, request):
        user_active = self.user
        doc_user_active = user_active.doc
        user = User.objects.filter(doc = doc_user_active).first()
        if user.is_staff:
            votantes = Votantes.objects.all()
            if votantes:
                cantidad_votantes = str(votantes.count())
                print(cantidad_votantes)
                return Response({'message':'Hay un total de ' + cantidad_votantes + " votantes en el sistema!"}, status= status.HTTP_200_OK)
            else:
                return Response({'message':'No hay votantes en el sistema'}, status= status.HTTP_200_OK)
        else:
            return Response({"message":"El usuario no tiene permisos para ver el total de votantes en el sistema"},status=status.HTTP_401_UNAUTHORIZED)


        
        

        
