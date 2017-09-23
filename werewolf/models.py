from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class Village(models.Model):
    name = models.CharField(max_length=200)
    auther = models.ForeignKey(User,default=1,on_delete=models.CASCADE)
    # auther.usernameで取れるので廃止する
    auther_name = models.CharField(default='system',max_length=200)
    charaset = models.CharField(default='rain', max_length=200)
    charaset_name = models.CharField(default='霧雨降る街', max_length=200)
    icon_url = models.CharField(default='A.png',max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    started_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)
    daytime_seconds = models.IntegerField()
    nighttime_seconds = models.IntegerField()
    day = models.IntegerField(default=0)
    nightflag = models.IntegerField(default=0)
    palflag = models.IntegerField(default=0)
    startflag = models.IntegerField(default=0)
    endflag = models.IntegerField(default=0)
    delflag = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Remark(models.Model):
    village = models.ForeignKey(Village, on_delete=models.CASCADE)
    remarker = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    serial_no = models.IntegerField(default=0)
    day = models.IntegerField(default=0)
    nightflag = models.IntegerField(default=0)
    remark_type = models.CharField(default='none',max_length=30)
    # remarker.usernameで取れるので廃止する
    remarker_name = models.CharField(max_length=200)
    character = models.IntegerField(default=1)
    charaset = models.CharField(default='rain', max_length=30)
    icon_url = models.CharField(max_length=100, default="A.png")
    date = models.DateTimeField(default=timezone.now)
    text = models.TextField()
    delflag = models.IntegerField(default=0)

    def __str__(self):
        return self.text

class Resident(models.Model):
    village = models.ForeignKey(Village, on_delete=models.CASCADE)
    resident = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    character = models.IntegerField(default=1)
    charaset = models.CharField(default='rain', max_length=30)
    icon_url = models.CharField(max_length=100, default="A.png")
    job = models.CharField(max_length=100, default='村人')
    deathflag = models.IntegerField(default=0)
    winflag = models.IntegerField(default=0)

    def __str__(self):
        return self.resident.username

class Execute(models.Model):
    village = models.ForeignKey(Village,on_delete=models.CASCADE)
    executer = models.ForeignKey(Resident,on_delete=models.CASCADE,related_name='executer')
    target = models.ForeignKey(Resident,on_delete=models.CASCADE,related_name='target')
    execute_type = models.CharField(default='none',max_length=30)
    day = models.IntegerField(default=0)

def getOpenVillageObjects():
    return Village.objects.filter(palflag=0,endflag=0,delflag=0).order_by('-created_date')
def getPalVillageObjects():
    return Village.objects.filter(palflag=1,endflag=0,delflag=0).order_by('-created_date')
def getEndVillageObjects():
    return Village.objects.filter(endflag=1, delflag=0).order_by('-created_date')
def getResidentObjects(village_id):
    return Resident.objects.filter(village=village_id)
def getAliveResidentObjects(village_id):
    return Resident.objects.filter(village=village_id,deathflag=0)
def getExecuteObjects(village_object):
    return Execute.objects.filter(day=village_object.day)
def getRemarkObjects(village_object):
    return Remark.objects.filter(
        village   = village_object.id,
#        day      = village_object.day,
#        nightflag = village_object.nightflag,
        delflag   = 0,
    ).order_by('-date')

def getVillageObject(village_id):
    return Village.objects.get(id=village_id)

def getThisTurnLength(village_object):
    return village_object.nighttime_seconds if bool(village_object.nightflag) else village_object.daytime_seconds
def calculateUpdateTime(village_object):
    return timezone.timedelta(seconds=getThisTurnLength(village_object)) + village_object.updated_date
