from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _ 
from django.db.models.deletion import CASCADE 
# Create your models here.
from .managers import CustomUserManager



class CustomUser(AbstractUser):
  name = models.CharField(max_length=200, null= True)
  email = models.EmailField(unique = True)
  bio = models.TextField()
  
  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = []
  objects = CustomUserManager()
  
  def __str__(self):
    return str(self.name)


class TopicModel(models.Model):
  name = models.CharField(max_length=200)
  def __str__(self):
      return self.name
  




class RoomModel(models.Model):
  host = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
  topic = models.ForeignKey('TopicModel', on_delete=models.SET_NULL, null=True)
  name = models.CharField(max_length=200)
  description = models.TextField(null=True, blank=True)
  participants = models.ManyToManyField(CustomUser, related_name='participants', blank=True)
  updated = models.DateTimeField(auto_now=True)
  created = models.DateTimeField(auto_now_add=True)
  
  class Meta:
    ordering = ['-updated','-created']
  def __str__(self):
      return self.name


class MassageModel(models.Model):
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  room = models.ForeignKey("RoomModel", on_delete=models.CASCADE)
  body = models.TextField()
  updated = models.DateTimeField(auto_now=True, null=True, blank=True)
  created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
  
  def __str__(self):
      return self.body[0:20]
  