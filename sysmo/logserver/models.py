from django.db import models
import uuid

# Create your models here.


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
                              blank=True,
                              null=True,
                              verbose_name=("主機群組"),
                              on_delete=models.SET_NULL,
                              related_name="machines")

    def __str__(self):  # 顯示名稱
        return self.hostname


class MachineGroup(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40, unique=True, verbose_name="群組名稱")
    policy = models.ForeignKey("Policy",
                               blank=True,
                               null=True,
                               verbose_name=("群組策略"),
                               related_name="machinegroups",
                               on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    def getMachine(self, group):
        return Machine.objects.filter(group=group)


class Policy(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40, unique=True, verbose_name="策略名稱")
    description = models.TextField(blank=True, null=True, verbose_name="描述")
    cpu_policy = models.JSONField(default=policy_default, verbose_name="CPU策略")
    mem_policy = models.JSONField(default=policy_default, verbose_name="MEM策略")
    swap_policy = models.JSONField(default=policy_default,
                                   verbose_name="SWAP策略")
    # { MountPoint: "/", value: "90", level: "Critical" }
    disk_policy = models.JSONField(blank=True,
                                   null=True,
                                   verbose_name="Disk策略")

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

    def __str__(self):
        return f"{self.machine.hostname}-{self.datetime}"
