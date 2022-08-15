from django.db import models

from django.db.models.signals import pre_save, post_delete
from django.utils.text import slugify
from django.conf import settings 
from django.dispatch import receiver

# Create your models here.


def upload_loc(instance, filename, **kwargs):
	file_path = 'blogpost/{author_id}/{title}-{filename}'.format(

			author_id  = str(instance.author.id),
			title = str(instance.title),
			filename = filename )
	
	return file_path




class BlogPost(models.Model):
	title = models.CharField(max_length=80, null=False, blank=False)
	body = models.TextField(max_length=6000, null=False, blank=False)
	image = models.ImageField(upload_to = upload_loc, null=False, blank=False)
	date_published = models.DateTimeField(auto_now_add=True, verbose_name="date created")
	date_updated = models.DateTimeField(auto_now=True, verbose_name="date updated")
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	slug = models.SlugField(blank=True, unique=True)
	

	def __str__(self):
		return self.title



'''
Deletes blogpost image that associates with certain blog
'''
@receiver(post_delete, sender=BlogPost,)
def submission_delete(sender, instance, **kwargs):
	instance.image.delete(False)

'''
Intercepts  saving of the blogpost to db before it saved
(creates slug for blogpost before it saved)
'''
def pre_save_blogpost_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = slugify(instance.author.username+'-'+instance.title)

pre_save.connect(pre_save_blogpost_receiver, sender=BlogPost)