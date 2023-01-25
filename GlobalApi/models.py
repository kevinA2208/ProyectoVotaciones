from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class UserManager(BaseUserManager):
    def create_user(self, doc, username, password=None):
        if not doc:
            raise ValueError('El usuario debe tener un numero de documento')

        user = self.model(
            doc = doc,
            username = username,
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, doc, username,password):
        user = self.create_user(
            doc = doc,
            username = username,
            password=password,
        )
        user.is_staff = True
        user.save()
        return user

class User(AbstractBaseUser):
    doc = models.CharField('Numero de documento', unique=True, max_length=20, primary_key=True)
    username = models.CharField('Nombre de usuario', max_length=50, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    
    objects = UserManager()
    USERNAME_FIELD = 'doc'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f'{self.username},  doc: {self.doc}'

    def has_perm(self,perm,obj = None):
        return True

    def has_module_perms(self, app_label):
        return True



class Lider(models.Model):
    id_lider = models.AutoField(primary_key=True)
    doc_lider = models.ForeignKey('User', on_delete=models.CASCADE, db_column='doc' )
    nombres_lider = models.CharField(max_length = 50)
    apellidos_lider = models.CharField(max_length = 100)
    direccion_lider = models.CharField(max_length = 100)
    ciudad_lider = models.CharField(max_length = 50)
    foto_lider = models.ImageField(upload_to='lideres', null=True, blank=True)
    email_lider = models.EmailField(null = False)
    cantidad_votantes = models.IntegerField(default=0)


class Votantes(models.Model):
    id_votante = models.AutoField(primary_key=True)
    doc_votante = models.CharField(max_length = 50)
    nombres_votante = models.CharField(max_length = 50)
    apellidos_votante = models.CharField(max_length = 100)
    direccion_votante = models.CharField(max_length = 100)
    municipio_votante = models.ForeignKey('Municipios', on_delete=models.CASCADE, db_column='id_municipio')
    puesto_votacion = models.ForeignKey('PuestoVotacion', on_delete=models.CASCADE, db_column='id_puesto_votacion')
    lider_id = models.ForeignKey('Lider', on_delete=models.CASCADE, db_column='id_lider')
    

class PuestoVotacion(models.Model):
    id_puesto_votacion = models.AutoField(primary_key=True)
    nombre_puesto_votacion = models.CharField(max_length = 50)
    direccion_puesto_votacion = models.CharField(max_length = 100)
    municipio_puesto_votacion = models.ForeignKey('Municipios', on_delete=models.CASCADE, db_column='id_municipio')
    cantidad_votantes = models.IntegerField(default=0)
    
    
class Municipios(models.Model):
    id_municipio = models.AutoField(primary_key=True)
    nombre_municipio = models.CharField(max_length = 50)
    departamento_municipio = models.ForeignKey('Departamentos', on_delete=models.CASCADE, db_column='id_departamento')
    cantidad_votantes = models.IntegerField(default=0)
    

class Departamentos(models.Model):
    id_departamento = models.AutoField(primary_key=True)
    nombre_departamento = models.CharField(max_length = 50)
    