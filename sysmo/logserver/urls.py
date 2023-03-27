from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"machines", views.MachineViewSet, basename="machine")
router.register(r"users", views.UserViewSet, basename="user")
router.register(r"machinegroups",
                views.MachineGroupViewSet,
                basename="machinegroup")
router.register(r"policies", views.PolicyViewSet, basename="policy")
router.register(r"performances",
                views.PerformanceViewSet,
                basename="performance")

app_name = "logserver"
urlpatterns = [
    # path("", views.index, name="index"),
    path("", include(router.urls)),
    path("dashboard/", views.dashboard, name='dashboard'),
    path("group/", views.group, name='group'),
    path(r"group/<str:name>", views.group_content, name='group_content'),
    path("policy/", views.policy, name='policy'),
    path(r"policy/<str:name>", views.policy_content, name='policy_content'),
]
