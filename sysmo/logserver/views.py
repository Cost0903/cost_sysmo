from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, action
from rest_framework.reverse import reverse
from rest_framework.response import Response

from .models import Machine, MachineGroup, Policy, Performance
from .serializers import UserSerializer, MachineSerializer, MachineGroupSerializer, PolicySerializer, PerformanceSerializer
# Create your views here.
import logging, json


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


# LOG_PATH = "/var/log/sysmo-agent/agent.log"


# @login_required
def dashboard(request):
    hosts = Machine.objects.all()
    groups = MachineGroup.objects.all()
    host_count = hosts.count()
    performances = []
    for host in hosts:
        performances.append(Performance.objects.filter(machine=host).last)
    # dashboard_value = {}
    normal_count = 1  # hosts.filter(status="normal").count()
    alert_count = 0  # hosts.filter(status="alert").count()
    offline_count = 1  # hosts.filter(status="offline").count()
    context = {
        'hosts': hosts,
        'host_count': host_count,
        'normal_count': normal_count,
        'alert_count': alert_count,
        'offline_count': offline_count,
        'groups': groups,
        'performances': performances,
    }
    return render(request, "logserver/dashboard.html", context=context)


def group(request):
    groups = MachineGroup.objects.all()
    # host_count = MachineGroup.
    context = {'groups': groups}
    return render(request, "logserver/group.html", context=context)


def group_content(request, name):
    machines = Machine.objects.filter(group__name=name)
    group = None
    try:
        group = Group.objects.filter(name=name)
    except:
        group = None
    finally:
        group = None if group is None else group
    context = {'group': group, 'machines': machines}
    return render(request, "logserver/group_content.html", context=context)


def policy(request):
    policies = Policy.objects.all()
    context = {'policies': policies}
    return render(request, "logserver/policy.html", context=context)


def policy_content(request, name):
    policy = Policy.objects.filter(name=name)
    groups = None
    try:
        groups = MachineGroup.objects.filter(policy=policy[0].id)
    except:
        logging.info("The Policy is not apply to any groups.")
    logging.info(f"Group = {groups}")
    context = {'policy': policy[0], 'groups': groups}
    return render(request, 'logserver/policy_content.html', context=context)


def host(request, name):
    host = Machine.objects.filter(hostname=name)
    context = {'host': host[0]}
    return render(request, "logserver/host.html", context=context)


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users':
        reverse('user-list', request=request, format=format),
        'machines':
        reverse('machine-list', request=request, format=format),
        'machinegroups':
        reverse('machinegroup-list', request=request, format=format),
        'policies':
        reverse('policy-list', request=request, format=format),
        'performances':
        reverse('performance-list', request=request, format=format),
    })


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'


class MachineGroupViewSet(viewsets.ModelViewSet):
    queryset = MachineGroup.objects.all()
    serializer_class = MachineGroupSerializer

    # lookup_field = 'name'

    # def list(self, request, *args, **kwargs):
    #     logging.info("MachineGroup List Method")
    #     logging.info(request.data)
    #     if MachineGroup.objects.all().count() == 0:
    #         try:
    #             policy = Policy.objects.get(name="default")
    #         except:
    #             policy = Policy.objects.create(
    #                 name="default",
    #                 cpu_policy=policy_default(),
    #                 mem_policy=policy_default(),
    #                 swap_policy=policy_default(),
    #                 disk_policy=disk_policy_default())
    #         MachineGroup.objects.create(name="default", policy=policy)
    #     return super().list(request, *args, **kwargs)


class PolicyViewSet(viewsets.ModelViewSet):
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'name'

    # def create(self, request, *args, **kwargs):
    #     return super().create(request, *args, **kwargs)

    # def list(self, request):
    #     logging.info("Policy List Method")
    #     logging.info(request.data)
    #     if Policy.objects.all().count() == 0:
    #         Policy.objects.create(name="default",
    #                               cpu_policy=policy_default(),
    #                               mem_policy=policy_default(),
    #                               swap_policy=policy_default(),
    #                               disk_policy=disk_policy_default())
    #     return super().list(request)


class MachineViewSet(viewsets.ModelViewSet):
    logging.info("MachineViewSet")
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False)
    def search_by_group(self, request):
        logging.info("Machine Search Method")
        logging.info(request.query_params)
        group_name = request.query_params.get('group')
        queryset = Machine.objects.filter(
            group__name=group_name).only("hostname")
        logging.info(f"type: {type(queryset)}")
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False)
    def get_last(self, request, *args, **kwargs):
        logging.info("Performance List Method")
        logging.info(request.query_params)
        hosts = []
        if request.query_params.get('group'):
            hosts = [
                m.uuid for m in Machine.objects.filter(
                    group__name=request.query_params.get('group')).only('uuid')
            ]
            logging.info(f"if  host_list: {hosts}")
        else:
            hosts = [m.uuid for m in Machine.objects.only('uuid')]
            logging.info(f"else  host_list: {hosts}")
        queryset = [
            Performance.objects.filter(machine=host).last() for host in hosts
            if Performance.objects.filter(machine=host)
        ]

        logging.info(f"queryset: {queryset}")
        logging.info(f"type: {type(queryset)}")
        # logging.info(queryset[0].machine.hostname)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
