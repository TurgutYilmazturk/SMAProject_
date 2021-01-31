
from django.db import models
from django.contrib.auth import get_user_model
import requests
from django.utils.text import slugify
import misaka
from django import template


# Create your models here.

register=template.Library()
User=get_user_model()


class Analysis(models.Model):
    user=models.ForeignKey(User,related_name='analysis',on_delete=models.CASCADE)
    topic=models.TextField()
    analysis_positive=models.IntegerField(blank=False, null=False)
    analysis_negative=models.IntegerField(blank=False,null=False)
    analysis_neutral=models.IntegerField(blank=False,null=False)
    created_at=models.DateTimeField(auto_now=True)
