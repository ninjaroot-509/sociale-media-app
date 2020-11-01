from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("category", kwargs={
            'slug': self.slug
        })

class Post(models.Model):
	user_name = models.ForeignKey(User, on_delete=models.CASCADE)
	title = models.CharField(max_length=200)
	pic = models.ImageField(upload_to='posts/imgs/')
	description = models.TextField()
	tags = models.CharField(max_length=100, null=True, blank=True)
	created_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(auto_now=True)
	is_active = models.BooleanField(default=True)
	
	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk': self.pk})

class Commentposts(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	username = models.ForeignKey(User, on_delete=models.CASCADE)
	comment = models.CharField(max_length=255)
	comment_date = models.DateTimeField(default=timezone.now)
	
class Art(models.Model):
	user_name = models.ForeignKey(User, on_delete=models.CASCADE)
	title = models.CharField(max_length=200)
	pic = models.ImageField(upload_to='arts/imgs/')
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	description = models.TextField()
	tags = models.CharField(max_length=100, null=True, blank=True)
	created_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(auto_now=True)
	is_active = models.BooleanField(default=True)
	
	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('art-detail', kwargs={'pk': self.pk})
 

class Comments(models.Model):
	art = models.ForeignKey(Art, related_name='details', on_delete=models.CASCADE)
	username = models.ForeignKey(User, related_name='details', on_delete=models.CASCADE)
	comment = models.CharField(max_length=255)
	comment_date = models.DateTimeField(default=timezone.now)

class Like(models.Model):
	user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
	art = models.ForeignKey(Art, related_name='likes', on_delete=models.CASCADE)
	