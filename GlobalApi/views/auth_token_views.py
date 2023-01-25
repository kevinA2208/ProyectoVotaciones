from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from GlobalApi.serializers.general_serializers import UserTokenSerializer
from django.contrib.sessions.models import Session
from datetime import datetime
from rest_framework.views import APIView

class Login(ObtainAuthToken):


    def post(self, request, *args, **kwargs):
        login_serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        
        if login_serializer.is_valid():
            user = login_serializer.validated_data['user']
            #Trae el token del usuario si existe, si no, lo crea
            #Esta variable devuelve la instancia del token, y un booleano si es true si se ha creado el token o false si no
            token,created = Token.objects.get_or_create(user=user)
            user_serializer = UserTokenSerializer(user)
            if created:
                return Response({
                    'token': token.key,
                    'user': user_serializer.data,
                    'message': "Inicio de sesión exitoso"
                }, status = status.HTTP_201_CREATED)
            else:
                all_sessions = Session.objects.filter(expire_date__gte=datetime.now())
                if all_sessions.exists():
                    for session in all_sessions:
                        session_data = session.get_decoded()
                        if user.id == session_data.get('_auth_user_id'):
                            session.delete()
                    
                token.delete()
                token = Token.objects.create(user = user)
                return Response({
                    'token': token.key,
                    'user': user_serializer.data,
                    'message': "Inicio de sesión exitoso"
                }, status = status.HTTP_201_CREATED)
                    
        else:
            return Response({'mensaje': 'Nombre de usuario o contraseña incorrectas'}, status= status.HTTP_400_BAD_REQUEST)
        return Response({'mensaje': 'holaa desde response'}, status= status.HTTP_200_OK)

class Logout(APIView):
    
    def get(self, request, *args, **kwargs):
        try:
            token = request.GET.get('token')
            token = Token.objects.filter(key = token).first()
            if token:
                user = token.user

                all_sessions = Session.objects.filter(expire_date__gte=datetime.now())
                if all_sessions.exists():
                    for session in all_sessions:
                        session_data = session.get_decoded()
                        if user.id == session_data.get('_auth_user_id'):
                            session.delete()

                token.delete()
                return Response({'message': 'Sesiones y token eliminados correctamente'}, status= status.HTTP_200_OK)
            return Response({'error': 'No se ha encontrado un usuario con estas credenciales'}, status= status.HTTP_400_BAD_REQUEST)

        except:
            return Response({'error': 'No se ha encontrado token en la petición'}, status= status.HTTP_409_CONFLICT)


