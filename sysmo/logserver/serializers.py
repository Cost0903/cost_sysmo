from rest_framework import serializers
from .models import Machine, MachineGroup, Policy, Performance
from django.contrib.auth.models import User
from rest_framework.fields import UUIDField


# class MachineSerializer(serializers.HyperlinkedModelSerializer):
class MachineSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    uuid = UUIDField(required=True)

    # owner = serializers.HyperlinkedRelatedField(view_name='user-detail',
    #                                             lookup_field='pk',
    #                                             read_only=True)

    # group = serializers.ReadOnlyField(source='group.name')

    class Meta:
        model = Machine
        fields = '__all__'
        # fields = [
        #     'url', 'owner', 'ruuid', 'hostname', 'uuid', 'os', 'interface',
        #     'disktable', 'group'
        # ]


# class UserSerializer(serializers.HyperlinkedModelSerializer):
class UserSerializer(serializers.ModelSerializer):
    machines = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Machine.objects.all())

    #     machines = serializers.HyperlinkedRelatedField(
    #         many=True,
    #         view_name='machine-detail',
    #         lookup_field='pk',
    #         queryset=Machine.objects.all())

    class Meta:
        model = User
        # fields = ['__all__', 'machines']
        # fields = ['url', 'id', 'username', 'machines']
        fields = ['id', 'username', 'machines']


# class MachineGroupSerializer(serializers.HyperlinkedModelSerializer):
class MachineGroupSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name='machinegroup-detail')
    # id = serializers.ReadOnlyField(source='machinegroup.id')
    # machine = MachineSerializer()

    # machines = serializers.StringRelatedField(many=True)
    machines = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Machine.objects.all())

    # machines = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     view_name='machine-detail',
    #     queryset=Machine.objects.all(),
    #     lookup_field='pk')

    class Meta:
        model = MachineGroup
        # fields = ['__all__', 'machines']
        # fields = ['url', 'id', 'name', 'policy', 'machines']
        fields = ['id', 'name', 'policy', 'machines']


# class PolicySerializer(serializers.HyperlinkedModelSerializer):
class PolicySerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='policy.id')

    class Meta:
        model = Policy
        fields = '__all__'
        # fields = [
        #     'url', 'id', 'name', 'cpupolicy', 'mempolicy', 'swappolicy',
        #     'diskpolicy'
        # ]


# class PerformanceSerializer(serializers.HyperlinkedModelSerializer):
class PerformanceSerializer(serializers.ModelSerializer):
    # id = serializers.ReadOnlyField(source='performance.id')
    machine = serializers.PrimaryKeyRelatedField(
        queryset=Machine.objects.all())

    # machine = serializers.HyperlinkedRelatedField(
    #     view_name='machine-detail',
    #     queryset=Machine.objects.all(),
    #     lookup_field='pk')

    class Meta:
        model = Performance
        # fields = [
        #     'url', 'id', 'machine', 'cpu_usage', 'mem_usage', 'swap_usage',
        #     'disk_usage', 'datetime'
        # ]
        fields = [
            'id', 'machine', 'cpu_usage', 'mem_usage', 'swap_usage',
            'disk_usage', 'datetime'
        ]
