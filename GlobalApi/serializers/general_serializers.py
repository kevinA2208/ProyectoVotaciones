from rest_framework import serializers
from GlobalApi.models import User, Votantes, PuestoVotacion, Municipios, Departamentos, Lider


class VotantesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Votantes
        fields = '__all__'

class PuestoVotacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PuestoVotacion
        fields = '__all__'

class MunicipiosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipios
        fields = '__all__'


class DepartamentosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamentos
        fields = '__all__'

class MunicipiosListSerializer(serializers.ModelSerializer):

    departamento_municipio = DepartamentosSerializer()

    class Meta:
        model = Municipios
        fields = ('id_municipio', 'nombre_municipio', 'departamento_municipio', 'cantidad_votantes')

class MunicipiosSinCantSerializer(serializers.ModelSerializer):

    departamento_municipio = DepartamentosSerializer()

    class Meta:
        model = Municipios
        fields = ('id_municipio', 'nombre_municipio', 'departamento_municipio')


class PuestoVotacionListSerializer(serializers.ModelSerializer):
    
        municipio_puesto_votacion = MunicipiosSinCantSerializer()
    
        class Meta:
            model = PuestoVotacion
            fields = ('id_puesto_votacion', 'nombre_puesto_votacion', 'direccion_puesto_votacion', 'municipio_puesto_votacion', 'cantidad_votantes')

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UsuariosListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)


class LiderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lider
        fields = '__all__'

class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('doc', 'username')

class LiderListSerializer(serializers.ModelSerializer):

    doc_lider = UsuariosListSerializer()

    class Meta:
        model = Lider
        fields = ('id_lider', 'doc_lider', 'nombres_lider', 'apellidos_lider', 'direccion_lider', 'ciudad_lider', 'foto_lider', 'email_lider')



