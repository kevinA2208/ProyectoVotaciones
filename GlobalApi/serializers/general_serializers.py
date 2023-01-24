from dataclasses import fields
from rest_framework import serializers
from GlobalApi.models import Lider, Admin, Votantes, PuestoVotacion, Municipios, Departamentos

class LiderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lider
        fields = '__all__'

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = '__all__'

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

