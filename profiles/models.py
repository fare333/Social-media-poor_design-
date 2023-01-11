from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    first_name = models.CharField(max_length=225)
    last_name = models.CharField(max_length=225)
    bio = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="post_images",default="avatar.jpg")
    followers = models.ManyToManyField(User,related_name="follower",blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.user.username
    
    
    def get_posts(self):
        return self.post_set.all().count()
    
    def get_followers(self):
        return self.followers.all().count()
    
class Followers(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE,related_name="sender")
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE,related_name="receiver")
    