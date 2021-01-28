from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from myblog.models import Mypost
from comments.models import Comment
# Create your views here.
def add_comments(request,posted_id):
    #获得了文章的id
    if request.method=="GET":
        return render(request,"error.html")
    else:

        #获取关联博客对象
        posted = Mypost.objects.get(pk=posted_id)
        #插入comments表中
        username = request.POST.get("username")
        email = request.POST.get("email")
        #同用户名 邮箱 对同一篇文章只能评论最多三次
        comm_num = Comment.objects.filter(comm_posted=posted,comm_name=username,comm_email=email).count()
        if comm_num==1:
            response = {"state":False,"msg":"评论次数过多","err_enum":1}
            return JsonResponse(response)
        

        content = request.POST.get("content")
        comm_obj = Comment.objects.create(comm_name=username,comm_email=email,comm_content=content,comm_posted=posted)

        response = {}
        response["state"] = True
        response["created_time"] = comm_obj.comm_created_time.strftime("%Y-%m-%d %H:%M")
        response["username"] = username
        response["content"] = content
        response["floor"] = Comment.objects.filter(comm_posted = posted).count()
        return JsonResponse(response)
