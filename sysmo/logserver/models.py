from datetime import datetime, timedelta
from django.db import models
import uuid
from sysmo.settings import CPU_POLICY, MEM_POLICY, SWAP_POLICY, DISK_POLICY, logging


class Machine(models.Model):
    hostname = models.CharField(max_length=40, verbose_name="主機名稱")
    description = models.TextField(blank=True, null=True, verbose_name="描述")
    uuid = models.UUIDField(primary_key=True,
                            unique=True,
                            default=uuid.uuid4,
                            editable=False,
                            verbose_name="UUID")
    ruuid = models.PositiveBigIntegerField(unique=True, verbose_name="RUUID")
    network_info = models.JSONField(verbose_name="網路資訊")
    disk_info = models.JSONField(verbose_name="硬碟資訊")
    cpu_info = models.JSONField(verbose_name="CPU資訊", null=True, blank=True)
    mem_info = models.JSONField(verbose_name="記憶體資訊", null=True, blank=True)
    os_info = models.JSONField(verbose_name="作業系統資訊", null=True, blank=True)
    owner = models.ForeignKey("auth.user",
                              verbose_name=("擁有者"),
                              on_delete=models.CASCADE,
                              related_name="machines")
    group = models.ForeignKey("MachineGroup",
                              default=1,
                              verbose_name=("主機群組"),
                              on_delete=models.DO_NOTHING,
                              related_name="machines")

    def __str__(self):  # 顯示名稱
        return self.hostname


class MachineGroup(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40, unique=True, verbose_name="群組名稱")
    policy = models.ForeignKey("Policy",
                               blank=True,
                               null=True,
                               default=1,
                               verbose_name=("群組策略"),
                               related_name="machinegroups",
                               on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name_plural = "Machine Groups"

    def __str__(self):
        return self.name


class Policy(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40, unique=True, verbose_name="策略名稱")
    description = models.TextField(blank=True, null=True, verbose_name="描述")
    cpu_policy = models.JSONField(default=CPU_POLICY, verbose_name="CPU策略")
    mem_policy = models.JSONField(default=MEM_POLICY, verbose_name="MEM策略")
    swap_policy = models.JSONField(default=SWAP_POLICY, verbose_name="SWAP策略")
    # { MountPoint: "/", value: "90", level: "Critical" }
    disk_policy = models.JSONField(default=DISK_POLICY, verbose_name="Disk策略")

    class Meta:
        verbose_name_plural = "Policies"

    def __str__(self):
        return self.name


class Performance(models.Model):
    id = models.AutoField(primary_key=True)
    machine = models.ForeignKey("Machine",
                                verbose_name=("主機"),
                                on_delete=models.CASCADE,
                                related_name="performances")
    # CPU 3 digits , 1 decimal_places # 99.1
    cpu_usage = models.DecimalField(verbose_name="CPU",
                                    max_digits=5,
                                    decimal_places=2)
    mem_usage = models.DecimalField(verbose_name="MEM",
                                    max_digits=5,
                                    decimal_places=2)
    swap_usage = models.DecimalField(verbose_name="SWAP",
                                     max_digits=5,
                                     decimal_places=2)
    disk_usage = models.JSONField(blank=True, null=True, verbose_name="Disk")
    datetime = models.DateTimeField(auto_now_add=True, verbose_name="時間")

    class Meta:
        verbose_name_plural = "Performances"

    def __str__(self):
        return f"{self.machine.hostname}-{self.datetime}"

    def status(self):
        # Green : OK
        # Yellow : Warning
        # Orange : Major
        # Red : Critical
        # Grey : Offline
        cpu_policy = self.machine.group.policy.cpu_policy
        mem_policy = self.machine.group.policy.mem_policy
        swap_policy = self.machine.group.policy.swap_policy
        disk_policy = self.machine.group.policy.disk_policy
        offline_status = "Offline" if datetime.now(
        ) - self.datetime > timedelta(minutes=10) else "OK"

        if cpu_policy['Pass'] == 1 or self.cpu_usage < cpu_policy['Warning']:
            cpu_status = "OK"
        elif self.cpu_usage >= cpu_policy[
                'Warning'] and self.cpu_usage < cpu_policy['Major']:
            cpu_status = "Warning"
        elif self.cpu_usage >= cpu_policy[
                'Major'] and self.cpu_usage < cpu_policy['Critical']:
            cpu_status = "Major"
        elif self.cpu_usage >= cpu_policy['Critical']:
            cpu_status = "Critical"

        if mem_policy['Pass'] == 1 or self.mem_usage < mem_policy['Warning']:
            mem_status = "OK"
        elif self.mem_usage >= mem_policy[
                'Warning'] and self.mem_usage < mem_policy['Major']:
            mem_status = "Warning"
        elif self.mem_usage >= mem_policy[
                'Major'] and self.mem_usage < mem_policy['Critical']:
            mem_status = "Major"
        elif self.mem_usage >= mem_policy['Critical']:
            mem_status = "Critical"

        if swap_policy['Pass'] == 1 or self.swap_usage < swap_policy['Warning']:
            mem_status = "OK"
        elif self.swap_usage >= swap_policy[
                'Warning'] and self.swap_usage < swap_policy['Major']:
            mem_status = "Warning"
        elif self.swap_usage >= swap_policy[
                'Major'] and self.swap_usage < swap_policy['Critical']:
            mem_status = "Major"
        elif self.swap_usage >= swap_policy['Critical']:
            mem_status = "Critical"

        for mp, val in self.disk_usage.items():
            try:
                if disk_policy[mp][
                        'Pass'] == 1 or val < disk_policy[mp]['Warning']:
                    disk_status = "OK"
                elif disk_policy[mp]['Warning'] <= val < disk_policy[mp][
                        'Major']:
                    disk_status = "Warning"
                elif disk_policy[mp]['Major'] <= val < disk_policy[mp][
                        'Critical']:
                    disk_status = "Major"
                elif disk_policy[mp]['Critical'] <= val:
                    disk_status = "Critical"
            except:
                logging.info("No Disk Policy")
