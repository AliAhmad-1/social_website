from django.db import models
from django.contrib.auth.models import AbstractUser

class MyUser(AbstractUser):
    image_profile=models.ImageField(upload_to='users_photo/',blank=True,null=True)
    cover_profile=models.ImageField(upload_to='users_photo/',blank=True,null=True)
    bio=models.TextField(max_length=160,blank=True,null=True)
    follow=models.ManyToManyField('self',through='Contact',related_name='followers',symmetrical=False)

class Contact(models.Model):
    user_to=models.ForeignKey(MyUser,on_delete=models.CASCADE,related_name='follow_to')
    user_from=models.ForeignKey(MyUser,on_delete=models.CASCADE,related_name='follow_from')
    created=models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering=['-created']
        indexes=[
        models.Index(fields=['-created'])
        ]
        unique_together=('user_to','user_from')
        
    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'
