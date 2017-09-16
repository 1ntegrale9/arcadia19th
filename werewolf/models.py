import datetime
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class Question(models.Model):
    question_text = models.CharField('質問', max_length=200)
    pub_date = models.DateTimeField('公開日時')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = '最近公開された'

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

class Village(models.Model):
    name = models.CharField('村名', max_length=200)
    auther = models.CharField('村主', max_length=200)
    character = models.CharField('キャラセット', max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    endflag = models.IntegerField(default=0)
    delflag = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Remark(models.Model):
    village = models.ForeignKey(Village, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, default=0, on_delete=models.CASCADE)
    serial_no = models.IntegerField(default=0)
    days = models.IntegerField(default=1)
    types = models.IntegerField(default=1)
    user = models.CharField('ユーザ名', max_length=200)
    character = models.IntegerField(default=1)
    character_img_url = models.CharField(max_length=100, default="rain/01.png")
    date = models.DateTimeField(default=timezone.now)
    text = models.TextField('発言')

    def __str__(self):
        return self.text

class Resident(models.Model):
    village = models.ForeignKey(Village, on_delete=models.CASCADE)
    resident = models.ForeignKey(User, default='system', on_delete=models.CASCADE)
    character = models.IntegerField(default=1)
    character_img_url = models.CharField(max_length=100, default="rain/01.png")
    position = models.CharField('役職', max_length=100, default='村人')
    death_flag = models.IntegerField(default=0)

    def __str__(self):
        return self.resident.username
