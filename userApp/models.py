from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
# Data of birth
# Address
# phone number
# bio
# profile picture
# gender
class profile(models.Model):

    gender=[
        ('male','male'),
        ('female','female'),
        ('others','others'),
    ]
    role =[
        ('admin', 'admin'),
        ('staff', 'staff'),
        ('user', 'user')
    ]
    profile_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, null=True, unique=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/',  null=True)
    gender = models.CharField(choices=gender, null=True, max_length=12)
    role = models.CharField(choices=role, max_length=12, default='user')

    def  __str__(self):
        return f'{self.user.username} {self.user.last_name}'
    
    @receiver(post_save, sender=User)
    def create_user_profile(sender,instance,created,  **kwargs):
        if created:
            profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def _post_save_receiver(sender, instance, **kwargs):
        instance.profile.save()
        
    

 

