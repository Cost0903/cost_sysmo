from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"machines", views.MachineViewSet, basename="machine")
router.register(r"users", views.UserViewSet, basename="user")
router.register(r"machinegroups", views.MachineGroupViewSet,
                basename="machinegroup")
router.register(r"policies", views.PolicyViewSet, basename="policy")

urlpatterns = [
    # path("", views.index, name="index"),
    path("", include(router.urls)),
    path('dashboard/', views.dashboard, name='dashboard'),
]