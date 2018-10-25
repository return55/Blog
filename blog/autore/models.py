from django.db import models
from django.contrib.auth.models import User

import datetime


class Autore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #nick = models.CharField(max_length=15, unique=True, help_text='Max 15 caratteri') #unico
    data_registrazione = models.DateField(default=datetime.date.today, editable=False)
    bio = models.TextField(blank=True)

    class Meta:
        get_latest_by  = ['-(User.objects.get(pk=self.user)).first_name', '-(User.objects.get(pk=self.user)).last_name']

     def __str__(self):
        return (User.objects.get(pk=self.user)).first_name + " " + (User.objects.get(pk=self.user)).last_name + ", " + (User.objects.get(pk=self.user)).username

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save() 

