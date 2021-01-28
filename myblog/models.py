from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
# Create your models here.



class PostCategory(models.Model):
    name = models.CharField(max_length=20,verbose_name="文章分类",default='undefined')

    def __str__(self):
        return self.name

def default_category():
    return PostCategory.objects.get_or_create(name="undefined")[0].id

class Mypost(models.Model):
    post_title = models.CharField(max_length=50,verbose_name="文章标题",default="此文章无标题")
    post_text = models.TextField(verbose_name="文章摘要",default="此文章无摘要")
    post_date = models.DateTimeField(auto_now_add=True,verbose_name="发布日期")
    post_update_date = models.DateTimeField(auto_now=True, verbose_name="更新日期")
    post_author = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="作者")
    post_article = models.FileField(upload_to="statics/posted/%Y/%m/", max_length=100,verbose_name="博客文件",default='statics/posted/default/default_posted.md')
    post_category = models.ManyToManyField('PostCategory',verbose_name="文章分类")

#admin 删除记录时删除文件
@receiver(pre_delete, sender=Mypost)
def file_delete(sender, instance, **kwargs):
    if instance.post_article=="statics/posted/default_posted.md":
        return
    instance.post_article.delete(False)
