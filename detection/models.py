from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from detection import utils

# Create your models here.
class Picture(models.Model):
    name = models.CharField(max_length=255, blank = True, null = True)
    url = models.ImageField(upload_to='upload/to_recognition/',default = 'upload/to_recognition/none.jpg', blank=True)
    last_modify_date = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

class Recognition(models.Model):
    picture = models.ForeignKey('Picture', on_delete=models.CASCADE,)
    result_json = models.TextField(max_length=255, blank = True, null = True)
    result_url = models.ImageField(upload_to='upload/recognition_result/',default = 'upload/recognition_result/none.jpg', blank=True)
    recognition_time = models.DateTimeField(auto_now_add=True)


# 触发器。图片保存到数据库成功后会触发该函数，然后可以进行物体检测，将检测结果保存到Recognition对象中
@receiver(post_save, sender = Picture)
def object_detection(sender, instance = None, **kwargs):
    # 获取最新上传的图片路径
    pic = Picture.objects.last()
    dict1, list1 = utils.detection_with_single(pic.url)
    str1 = ";".join(list1)
    rec = Recognition(picture = pic, result_json = str1, result_url = dict1['result_url'], recognition_time = dict1['recognition_time'])
    rec.save()

