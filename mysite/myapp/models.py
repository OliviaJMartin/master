from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class MachineInfo(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    name = models.CharField(max_length=50, default='')
    serialNum = models.CharField(max_length=50)
    swVersion = models.CharField(max_length=50)

    class Meta:
        db_table = 'MachineInfo'

    def __str__(self):
        return self.name


class MachineStatus(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    machineID = models.ForeignKey(MachineInfo, on_delete=models.CASCADE,)
    Status = models.CharField(max_length=50)
    startUserID = models.ForeignKey(User, on_delete=models.CASCADE, default=-1)
    startTime = models.CharField(max_length=50, default='01-01-1900 00:00:00')
    description = models.CharField(max_length=100)
    comments = models.CharField(max_length=255)

    class Meta:
        db_table = 'MachineStatus'

    def __int__(self):
        return self.id


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'

