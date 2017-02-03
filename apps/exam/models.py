from __future__ import unicode_literals

from django.db import models

from ..LogReg.models import User

# Create your models here.

class Quotes(models.Model):
    quote = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    poster = models.ForeignKey("LogReg.User")
    created_at = models.DateTimeField(auto_now_add=True)

class Favorites(models.Model):
    favorite = models.ForeignKey('Quotes', related_name="favorite")
    favorited_by = models.ForeignKey('LogReg.User', related_name="favorited_by")
    created_at = models.DateTimeField(auto_now_add=True)
