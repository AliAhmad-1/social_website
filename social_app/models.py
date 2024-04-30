from django.db import models
from social_website import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
class Post(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,related_name='posts_created',on_delete=models.CASCADE)
    content=models.TextField(max_length=500)
    image=models.ImageField(upload_to="images/%Y/%m/%d/",blank=True,null=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    saves=models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name="user_saves")
    likes=models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name='user_likes')
    class Meta:
        ordering=['-created']
        indexes=[models.Index(fields=['-created']),]
    def __str__(self):
        return self.content


class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='post_comments')
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="user_comments")
    content=models.TextField(max_length=150,blank=False)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'" {self.content} "  on  " {self.post.content} "'
    class Meta:
        ordering=['-created']
        indexes=[models.Index(fields=['-created'])]



class Action(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,related_name='user_action',on_delete=models.CASCADE)
    verb=models.CharField(max_length=255)
    created=models.DateTimeField(auto_now_add=True)
    target_ct=models.ForeignKey(ContentType,blank=True,null=True,related_name='target_obj',on_delete=models.CASCADE)
    target_id=models.PositiveIntegerField(null=True,blank=True)
    target=GenericForeignKey('target_ct','target_id')

    class Meta:
        ordering=['-created']
        indexes=[
        models.Index(fields=['-created']),
        models.Index(fields=['target_ct', 'target_id']),
        ]