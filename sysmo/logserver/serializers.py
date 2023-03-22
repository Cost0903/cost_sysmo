from rest_framework import serializers
from .models import Machine, MachineGroup, Policy, Performance
from django.contrib.auth.models import User


class MachineSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    group = serializers.ReadOnlyField(source='group.name')

    class Meta:
        model = Machine
        fields = ['url', 'owner', 'ruuid', 'hostname',
                  'uuid', 'os', 'interface', 'disktable', 'group']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    machines = serializers.HyperlinkedRelatedField(
        many=True, view_name='machine-detail', queryset=Machine.objects.all())

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'machines']


class MachineGroupSerializer(serializers.HyperlinkedModelSerializer):
    # id = serializers.ReadOnlyField(source='machinegroup.id')
    # machines = serializers.StringRelatedField(many=True)
    machines = serializers.HyperlinkedRelatedField(
        many=True, view_name='machine-detail', queryset=Machine.objects.all())

    class Meta:
        model = MachineGroup
        fields = ['url', 'id', 'name', 'Gpolicy', 'machines']


class PolicySerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField(source='policy.id')

    class Meta:
        model = Policy
        fields = ['url', 'id', 'name', 'cpupolicy', 'mempolicy', 'swappolicy',
                  'diskpolicy']


class PerformanceSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField(source='performance.id')
    

    class Meta:
        model = Performance
        fields = ['url', 'id', 'machine', 'cpu', 'mem', 'swap', 'disk']
