from django.db import models
from myblog.models import Mypost
# Create your models here.
class Comment(models.Model):
    comm_name = models.CharField(max_length=30)
    comm_email = models.EmailField()
    comm_content = models.TextField()
    comm_created_time = models.DateTimeField(auto_now_add=True)
    comm_posted = models.ForeignKey(Mypost,on_delete=models.CASCADE)

    def __str__(self):
        return self.comm_content[:20]