from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class MyProfile(models.Model):
    # 使用django.contrib.auth.models.User作为Model,额外的属性我们使用MyProfile进行补充

    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)

    phone_num = models.CharField(max_length=20, blank=True)
    mugshot = models.ImageField(upload_to='upload',default = 'upload/none.jpg', blank=True)
    is_developer = models.BooleanField(default=True)    # 开发者
    is_custom_user = models.BooleanField(default=False) # 普通用户

    def __str__(self):
        return self.user.__str__()