from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class Village(models.Model):
    name = models.CharField('村名', max_length=200)
    auther = models.CharField('村主', max_length=200)
    character = models.CharField('キャラセット', default='rain', max_length=200)
    character_name = models.CharField(default='霧雨降る街', max_length=200)
    character_img_url = models.CharField(default='rain/01.png',max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    started_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)
    daytime_length = models.IntegerField()
    nighttime_length = models.IntegerField()
    days = models.IntegerField('何日目', default=0)
    nightflag = models.IntegerField(default=0)
    palflag = models.IntegerField(default=0)
    startflag = models.IntegerField(default=0)
    endflag = models.IntegerField(default=0)
    delflag = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Remark(models.Model):
    village = models.ForeignKey(Village, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    serial_no = models.IntegerField(default=0)
    days = models.IntegerField(default=0)
    nightflag = models.IntegerField(default=0)
    types = models.IntegerField(default=1)
    user = models.CharField('ユーザ名', max_length=200)
    character = models.IntegerField(default=1)
    charaset = models.CharField('キャラセット', default='rain', max_length=30)
    character_img_url = models.CharField(max_length=100, default="rain/01.png")
    date = models.DateTimeField(default=timezone.now)
    text = models.TextField('発言')
    delflag = models.IntegerField(default=0)

    def __str__(self):
        return self.text

class Resident(models.Model):
    village = models.ForeignKey(Village, on_delete=models.CASCADE)
    resident = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    character = models.IntegerField(default=1)
    charaset = models.CharField('キャラセット', default='rain', max_length=30)
    character_img_url = models.CharField(max_length=100, default="rain/01.png")
    job = models.CharField('役職', max_length=100, default='村人')
    types = models.IntegerField(default=1)
    deathflag = models.IntegerField(default=0)
    winflag = models.IntegerField(default=0)

    def __str__(self):
        return self.resident.username
