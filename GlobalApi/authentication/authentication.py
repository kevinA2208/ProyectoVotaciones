from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from datetime import timedelta
from django.utils import timezone
from django.conf import settings


class ExpiringTokenAuthentication(TokenAuthentication):
    expired = False
    #Esta funcion calcula el tiempo de expiracion
    def expires_in(self, token):
        time_elapsed = timezone.now() - token.created
        #El tiempo de expiracion se encuentra en el archivo settings.py
        left_time = timedelta(seconds = settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed
        return left_time

    #Esta funcion verifica si el token esta expirado
    def is_token_expired(self, token):
        return self.expires_in(token) < timedelta(seconds = 0)


    #Esta funcion llama la funcion para verificar si el token esta expirado, si lo está, lo borra y crea uno nuevo
    def token_expire_handler(self, token):
        is_expired = self.is_token_expired(token)
        if is_expired:
            self.expired = True
            #Si el tiempo del token ha expirado, se guarda el usuario de ese token en una variable, se borra el token, y se crea uno nuevo con el mismo usuario
            user = token.user
            token.delete()
            token = self.get_model().objects.create(user=token.user)
        return is_expired,token
        


    def authenticate_credentials(self, key):
        message,token,user = None,None,None
        try:
            token = self.get_model().objects.select_related('user').get(key=key)
            user = token.user
        #Validación por si se envia un token invalido no existente
        except self.get_model().DoesNotExist:
            message = "Token Invalido"
            self.expired = True
            
        if token is not None:
            if not token.user.is_active:
                message = "Usuario no activo o eliminado"
            
        if token is not None:
            is_expired = self.token_expire_handler(token)
            if is_expired:
                message = "El token ha expirado"
           
            
        return (user,token,message,self.expired)


