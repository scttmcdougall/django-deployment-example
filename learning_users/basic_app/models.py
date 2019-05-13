from django.db import models
from django.contrib.auth.models import User

class UserProfileInfo(models.Model):
    #add more attributes to user
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    #additional classes
    #blank true = not compulsory field
    portfolio_site = models.URLField(blank=True)
    profile_pic = models.ImageField(upload_to = 'profile_pics',blank=True)
    #method to print up user details. username is default of user
    def __str__(self):
        return self.user.username
        
