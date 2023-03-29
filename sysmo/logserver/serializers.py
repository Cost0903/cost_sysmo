from rest_framework import serializers
from .models import Machine, MachineGroup, Policy, Performance
from django.contrib.auth.models import User


class MachineSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.HyperlinkedRelatedField(view_name='user-detail',
                                                lookup_field='pk',
                                                read_only=True)

    # group = serializers.ReadOnlyField(source='group.name')

    class Meta:
        model = Machine
        fields = '__all__'
        # fields = [
        #     'url', 'owner', 'ruuid', 'hostname', 'uuid', 'os', 'interface',
        #     'disktable', 'group'
        # ]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    machines = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='machine-detail',
        lookup_field='pk',
        queryset=Machine.objects.all())

    class Meta:
        model = User
        # fields = ['__all__', 'machines']
        fields = ['url', 'id', 'username', 'machines']


class MachineGroupSerializer(serializers.HyperlinkedModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name='machinegroup-detail')
    # id = serializers.ReadOnlyField(source='machinegroup.id')
    # machine = MachineSerializer()

    # machines = serializers.StringRelatedField(many=True)

    machines = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='machine-detail',
        queryset=Machine.objects.all(),
        lookup_field='pk')

    class Meta:
        model = MachineGroup
        # fields = ['__all__', 'machines']
        fields = ['url', 'id', 'name', 'policy', 'machines']


class PolicySerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField(source='policy.id')

    class Meta:
        model = Policy
        fields = '__all__'
        # fields = [
        #     'url', 'id', 'name', 'cpupolicy', 'mempolicy', 'swappolicy',
        #     'diskpolicy'
        # ]


class PerformanceSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField(source='performance.id')

    class Meta:
        model = Performance
        fields = ['url', 'id', 'machine', 'cpu', 'mem', 'swap', 'disk']
