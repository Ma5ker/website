from django.contrib import admin
from myblog import models


class PostAdmin(admin.ModelAdmin):
    list_display = ('id','post_title','post_author', 'post_date','post_update_date')
class ShowCategory(admin.ModelAdmin):
    list_display = ('id','name')
# Register your models here.
admin.site.register(models.Mypost,PostAdmin)
admin.site.register(models.PostCategory,ShowCategory)