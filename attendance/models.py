from django.db import models
from django.contrib.auth import get_user_model
import datetime

# 出席確認機能

class Uezu_seminar(models.Model):
    student_id = models.CharField(max_length=7)
    attended_day = models.DateField('出席日')
