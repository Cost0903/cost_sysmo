from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import MachineGroup, Policy
from sysmo.settings import logging, CPU_POLICY, MEM_POLICY, SWAP_POLICY, DISK_POLICY


@receiver(post_migrate)
def create_default_groups_and_policies(sender, **kwargs):
    """Create Default Group and Policy,
    Admin User can change it later, include the name and value.
    """
    logging.info("Create Default Group and Policy")

    # 檢查 Default Policy 是否已存在
    if not Policy.objects.exists():
        # 建立預設的 Policy
        default_policy = Policy.objects.create(name='Default')
        default_policy.cpu_policy = CPU_POLICY
        default_policy.mem_policy = MEM_POLICY
        default_policy.swap_policy = SWAP_POLICY
        default_policy.disk_policy = DISK_POLICY
        default_policy.save()

    if not MachineGroup.objects.exists():
        # 建立預設的 Machine Group
        default_group = MachineGroup.objects.create(name='Default')
        # 設定 Default Policy 套用在 Default Machine Group 上
        default_group.policy = Policy.objects.get(name='Default')
        default_group.save()
