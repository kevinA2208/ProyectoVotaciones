from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class UserManager(BaseUserManager):
    def create_user(self, email, doc, name,password=None):
        if not doc:
            raise ValueError('The user must have a document')

        user = self.model(
            doc = doc,
            email = self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, doc, name, password):
        user = self.create_user(
            email,
            doc = doc,
            name=name,
            password=password,
        )
        user.user_type = 'A'
        user.save()
        return user

class User(AbstractBaseUser):
    doc = models.CharField('Numero de documento', unique=True, max_length=20, primary_key=True)
    name = models.CharField('Nombre de usuario', max_length=50, blank=True, null=True)
    user_type = models.CharField('Tipo usuario', max_length=1)
    email = models.EmailField('Correo electronico', max_length=100, unique=True)
    #[A (Admin) L (Lider)]
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['doc', 'name']

    def __str__(self):
        return f'{self.name},  doc: {self.doc}'

    def has_perm(self,perm,obj = None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.user_type == 'A'


class Lider(models.Model):
    id_lider = models.AutoField(primary_key=True)
    doc_lider = models.ForeignKey('User', on_delete=models.CASCADE, db_column='doc' )
    nombres_lider = models.CharField(max_length = 50)
    apellidos_lider = models.CharField(max_length = 100)
    direccion_lider = models.EmailField(null = False)
    ciudad_lider = models.CharField(max_length = 50)
    foto_lider = models.ImageField(upload_to='lideres', null=True, blank=True)
    email_lider = models.EmailField(null = False)


class Admin(models.Model):
    id_admin = models.AutoField(primary_key=True)
    doc_admin = models.ForeignKey('User', on_delete=models.CASCADE, db_column='doc' )
    name_admin = models.CharField(max_length = 50)
    last_name_admin = models.CharField(max_length = 100)
    email = models.EmailField(null = False)


class Votantes(models.Model):
    id_votante = models.AutoField(primary_key=True)
    doc_votante = models.CharField(max_length = 50)
    nombres_votante = models.CharField(max_length = 50)
    apellidos_votante = models.CharField(max_length = 100)
    direccion_votante = models.CharField(max_length = 100)
    ciudad_votante = models.CharField(max_length = 50)
    puesto_votacion = models.ForeignKey('PuestoVotacion', on_delete=models.CASCADE, db_column='id_puesto_votacion')
    lider_id = models.ForeignKey('Lider', on_delete=models.CASCADE, db_column='id_lider')
    

class PuestoVotacion(models.Model):
    id_puesto_votacion = models.AutoField(primary_key=True)
    nombre_puesto_votacion = models.CharField(max_length = 50)
    direccion_puesto_votacion = models.CharField(max_length = 100)
    municipio_puesto_votacion = models.ForeignKey('Municipios', on_delete=models.CASCADE, db_column='id_municipio')
    
    
class Municipios(models.Model):
    id_municipio = models.AutoField(primary_key=True)
    nombre_municipio = models.CharField(max_length = 50)
    departamento_municipio = models.ForeignKey('Departamentos', on_delete=models.CASCADE, db_column='id_departamento')
    

class Departamentos(models.Model):
    id_departamento = models.AutoField(primary_key=True)
    nombre_departamento = models.CharField(max_length = 50)
    