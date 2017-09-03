import datetime
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
    auther = models.CharField('作成者', max_length=200)
    character = models.CharField('キャラセット', max_length=200)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class Remark(models.Model):
    village = models.ForeignKey(Village, on_delete=models.CASCADE)
    serial_no = models.IntegerField(defalult=0)
    days = models.IntegerField(default=1)
    types = models.IntegerField(default=1)
    user = models.CharField('ユーザ名', max_length=200)
    date = models.DateTimeField(default=timezone.now)
    text = models.TextField('本文')

    def __str__(self):
        return self.text
