from django.db import models
import uuid

# Create your models here.


def policy_default():
    return {"Pass": "0", "Warning": "75", "Major": "90", "Critical": "98"}


def disk_policy_default():
    return {"Pass": "0", "Warning": "75", "Major": "90", "Critical": "98"}


class Machine(models.Model):
    hostname = models.CharField(max_length=40, verbose_name="主機名稱")
    uuid = models.UUIDField(primary_key=True, unique=True,
                            default=uuid.uuid4, editable=False, verbose_name="UUID")
    ruuid = models.CharField(max_length=40, unique=True, verbose_name="RUUID")
    os = models.CharField(max_length=10, verbose_name="作業系統")
    owner = models.ForeignKey("auth.user", verbose_name=(
        "擁有者"), on_delete=models.CASCADE)
    interface = models.JSONField(blank=True, null=True, verbose_name="網路介面")
    disktable = models.JSONField(blank=True, null=True, verbose_name="磁碟資訊")
    group = models.ForeignKey("MachineGroup", blank=True, null=True, verbose_name=(
        "主機群組"), on_delete=models.SET_NULL)

    def __str__(self):  # 顯示名稱
        return self.hostname


class MachineGroup(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40, unique=True, verbose_name="群組名稱")
    Gpolicy = models.ForeignKey("Policy", blank=True, null=True, verbose_name=(
        "群組策略"), on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class Policy(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40, unique=True, verbose_name="策略名稱")
    cpupolicy = models.JSONField(default=policy_default, verbose_name="CPU策略")
    mempolicy = models.JSONField(default=policy_default, verbose_name="MEM策略")
    swappolicy = models.JSONField(
        default=policy_default, verbose_name="SWAP策略")
    diskpolicy = models.JSONField(blank=True, null=True, verbose_name="Disk策略") # { MountPoint: "/", value: "90", level: "Critical" }

    def __str__(self):
        return self.name


class Performance(models.Model):
    id = models.AutoField(primary_key=True)
    machine = models.ForeignKey("Machine", verbose_name=(
        "主機"), on_delete=models.CASCADE)
    cpu = models.DecimalField(
        verbose_name="CPU", max_digits=5, decimal_places=2)
    mem = models.DecimalField(
        verbose_name="MEM", max_digits=5, decimal_places=2)
    swap = models.DecimalField(
        verbose_name="SWAP", max_digits=5, decimal_places=2)
    disk = models.JSONField(blank=True, null=True, verbose_name="Disk")
    time = models.DateTimeField(auto_now=True, verbose_name="時間")

    def __str__(self):
        return f"{self.machine.hostname}-{self.time}"
