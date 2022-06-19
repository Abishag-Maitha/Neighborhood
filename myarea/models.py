from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from cloudinary.models import CloudinaryField
import datetime as dt

   
# Create your models here.
class Neighbourhood(models.Model):
    name = models.CharField(max_length = 65)
    location  = models.CharField(max_length=65)
    occupants = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='neighborhood')
    image = CloudinaryField('image')
    description = models.TextField()  
    health = models.IntegerField(null=True, blank=True ,default=0)
    
    class Meta:
        verbose_name_plural = 'Location'

    @classmethod
    def search_hood(cls, search_term):
        hoods = cls.objects.filter(name__icontains=search_term)
        return hoods

    def __str__(self):
        return f"{self.location}"

    def save_hood(self):
        self.save()

    def delete_hood(self):
        self.delete()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture =CloudinaryField('image')
    bio = models.TextField(max_length=800, default="", blank=True)
    location = models.CharField(max_length=60, blank=True)
    neighbourhood = models.ForeignKey(Neighbourhood, on_delete=models.SET_NULL, null=True, related_name='members', blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def save_profile(self):
        self.user

    def delete_profile(self):
        self.delete()

    @classmethod
    def search_profile(cls, name):
        return cls.objects.filter(user__username__icontains=name).all()



class Post(models.Model):
    title = models.CharField(max_length = 65)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hood = models.ForeignKey(Neighbourhood,on_delete=models.CASCADE, blank=True)
    description = models.TextField(max_length=1000)
    
        
    def __str__(self):
        return self.description


class Business(models.Model):
    name = models.CharField(max_length = 200)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    hood = models.ForeignKey(Neighbourhood, on_delete=models.CASCADE, related_name='business')
    business_image=CloudinaryField('image')

    def __str__(self):
        return self.name

    def save_business(self):
        self.save()

    def delete_business(self):
        self.delete()
    @classmethod
    def search_business(cls, name):
        return cls.objects.filter(name__icontains=name).all()

class Join(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    hood_id = models.ForeignKey(Neighbourhood, on_delete=models.CASCADE)

    def __str__(self):
        return self.user_id

