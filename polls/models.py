import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date>=timezone.now()-datetime.timedelta(days=1)

class Choice(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    votes_count = models.IntegerField(default=0)
    groups = models.ManyToManyField('auth.Group', related_name='custom_user_groups', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_user_user_permissions', blank=True)
    
    def __str__(self):
        return self.username
    
class Vote(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='votes')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)  

    class Meta:
        unique_together = ('user', 'question')
# Create your models here.
