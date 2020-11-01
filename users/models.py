from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from autoslug import AutoSlugField
from phonenumber_field.modelfields import PhoneNumberField

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	phone = PhoneNumberField(help_text="numero personnel")
	image = models.ImageField(default='default.png', upload_to='profile_pics')
	slug = AutoSlugField(populate_from='user')
	bio = models.TextField(null=True, blank=True)
	friends = models.ManyToManyField("Profile",blank=True)

	def __str__(self):
		return self.user.username

	def get_absolute_url(self):
		return "/users/{}".format(self.slug)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class FriendRequest(models.Model):
	to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='to_user', on_delete=models.CASCADE)
	from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='from_user', on_delete=models.CASCADE)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return "From {}, to {}".format(self.from_user.username, self.to_user.username)



