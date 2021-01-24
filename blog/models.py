from django.db import models
# Create your models here.

#文章信息
class ArticlePost(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=20)
    post_tag = models.CharField(max_length=20) # 文章的tag
    created_time = models.DateField(auto_now_add=True)#创建时间
    updated_time = models.DateField(auto_now=True)#更新时间
    post_view = models.IntegerField(default=0) #浏览量
    content_path = models.CharField(max_length=100) #存放博客内容名称,基于"/static/posted"构建路径
    #一级评论
    comments = models.ForeignKey('Comment',on_delete=models.CASCADE ,blank=True,null=True,default=None)

    def __str__(self):
        return self.title

#评论信息
class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.CharField(max_length=20)#作者
    email = models.EmailField()#邮箱
    content = models.TextField()#内容
    created_time = models.DateField(auto_now_add=True)#创建时间
    #父评论 可以根据一级评论内容,反向查找构建多级评论
    c_parent = models.ForeignKey('self',on_delete=models.CASCADE ,blank=True,null=True,default=None)
