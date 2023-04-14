from rest_framework import serializers
from .models import Machine, MachineGroup, Policy, Performance
from django.contrib.auth.models import User
from rest_framework.fields import UUIDField
import logging


def policy_default():
    return {"Pass": "0", "Warning": "75", "Major": "90", "Critical": "98"}


def disk_policy_default():
    return {
        "/": {
            "Pass": "0",
            "Warning": "75",
            "Major": "90",
            "Critical": "98"
        }
    }


# class MachineSerializer(serializers.HyperlinkedModelSerializer):
class MachineSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    def create(self, validated_data):
        logging.info("MachineSerializer.create")
        logging.info(validated_data)
        if validated_data['group'] is None:
            try:
                group = MachineGroup.objects.get(name="default")
            except:
                group = MachineGroup.objects.create(name="default")
            validated_data['group'] = group
        logging.info(validated_data)

        return super().create(validated_data)

    class Meta:
        model = Machine
        fields = '__all__'


# class UserSerializer(serializers.HyperlinkedModelSerializer):
class UserSerializer(serializers.ModelSerializer):
    machines = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Machine.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'machines']


# class MachineGroupSerializer(serializers.HyperlinkedModelSerializer):
class MachineGroupSerializer(serializers.ModelSerializer):
    machines = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Machine.objects.all())

    class Meta:
        model = MachineGroup
        fields = ['id', 'name', 'policy', 'machines']

    def create(self, validated_data):
        logging.info("MachineGroupSerializer.create")
        logging.info(validated_data)
        if validated_data['policy'] is None:
            try:
                policy = Policy.objects.get(name="default")
            except:
                policy = Policy.objects.create(
                    name="default",
                    cpu_policy=policy_default(),
                    mem_policy=policy_default(),
                    swap_policy=policy_default(),
                    disk_policy=disk_policy_default())
            validated_data['policy'] = policy
        return super().create(validated_data)


# class PolicySerializer(serializers.HyperlinkedModelSerializer):
class PolicySerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='policy.id')

    class Meta:
        model = Policy
        fields = [
            'id', 'name', 'description', 'cpu_policy', 'mem_policy',
            'swap_policy', 'disk_policy'
        ]


# class PerformanceSerializer(serializers.HyperlinkedModelSerializer):
class PerformanceSerializer(serializers.ModelSerializer):
    machine = serializers.PrimaryKeyRelatedField(
        queryset=Machine.objects.all())
    hostname = serializers.ReadOnlyField(source='machine.hostname')
    group = serializers.ReadOnlyField(source='machine.group.name')
    owner = serializers.ReadOnlyField(source='machine.owner.username')
    policy = serializers.ReadOnlyField(source='machine.group.policy.name')

    class Meta:
        model = Performance
        fields = [
            'id',
            'machine',
            'hostname',
            'group',
            'policy',
            'owner',
            'cpu_usage',
            'mem_usage',
            'swap_usage',
            'disk_usage',
            'datetime',
        ]
