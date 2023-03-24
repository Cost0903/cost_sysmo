from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, action
from rest_framework.reverse import reverse
from rest_framework.response import Response

from .models import Machine, MachineGroup, Policy, Performance
from .serializers import UserSerializer, MachineSerializer, MachineGroupSerializer, PolicySerializer, PerformanceSerializer
# Create your views here.


def dashboard(request):
    hosts = Machine.objects.all()
    groups = MachineGroup.objects.all()
    host_count = hosts.count()
    normal_count = 1  # hosts.filter(status="normal").count()
    alert_count = 0  # hosts.filter(status="alert").count()
    offline_count = 1  # hosts.filter(status="offline").count()
    return render(
        request, "logserver/dashboard1.html", {
            'hosts': hosts,
            'host_count': host_count,
            'normal_count': normal_count,
            'alert_count': alert_count,
            'offline_count': offline_count,
            'groups': groups
        })


def host(request, pk):
    return render(request, "logserver/host.html")


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users':
        reverse('user-list', request=request, format=format),
        'machines':
        reverse('machine-list', request=request, format=format),
    })


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class MachineGroupViewSet(viewsets.ModelViewSet):
    queryset = MachineGroup.objects.all()
    serializer_class = MachineGroupSerializer

    # @action(detail=True, methods=['get'])
    # def default_group(self, request):
    #     group = self.get_object()
    #     serializer = MachineGroupSerializer(data=request.data)
    #     if serializer.is_valid():
    #         return Response(serializer.data)
    #     else:
    #         try:
    #             group = MachineGroup.objects.all()
    #         except:
    #             MachineGroup.objects.create(name="default")
    #     return Response("OK")


class PolicyViewSet(viewsets.ModelViewSet):
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class MachineViewSet(viewsets.ModelViewSet):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
