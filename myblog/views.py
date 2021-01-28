from django.shortcuts import render,redirect,reverse,HttpResponse
import datetime
from django.views.generic import ListView,DetailView
from comments.models import Comment
from .models import Mypost,PostCategory
# Create your views here.

def error_handle(request):
    return render(request,"error.html")


def feedContent(filepath):
    posted = filepath.path
    with open(posted,"r") as fp:
        return fp.read()

#使用ListView显示博客列表页
class HomeView(ListView):
    model = Mypost
    template_name = "myblog/index.html"
    context_object_name = "post_list"
    ordering = ['-post_update_date']
    paginate_by = 5

    #添加附加信息
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_list = PostCategory.objects.exclude(name="undefined")
        context["category_list"] = category_list
        return context

def postview(request,post_id):
    posted = Mypost.objects.get(pk=post_id)
    if posted.post_article=="":
        #博客文章不存在  重定向至错误页面
        return redirect(reverse("blog:error"))
    else:
        post_info = {}
        post_info["posted_id"] = post_id
        post_info["post_title"] = posted.post_title
        post_info["post_author"] = posted.post_author
        post_info["post_date"] = posted.post_date
        post_info["post_update_date"] = posted.post_update_date
        post_info["post_content"] = feedContent(posted.post_article)

        # 评论
        comment_obj = Comment.objects.filter(comm_posted=posted).order_by("comm_created_time")

        #分类
        category_list = PostCategory.objects.exclude(name="undefined")

        context = {
            "post_info":post_info,
            "comment_info":comment_obj,
            "category_list":category_list,
        }
        return render(request,"myblog/blog-post.html",context)


class CategoryView(ListView):
    model = Mypost
    template_name = "myblog/index.html"
    context_object_name = "post_list"
    ordering = ['-post_update_date']
    paginate_by = 5


    #与home相同，但要筛选出需要的
    def get_queryset(self):
        ca_name = self.request.GET.get('name', None)
        pkid = PostCategory.objects.get(name=ca_name)
        return Mypost.objects.filter(post_category=pkid).order_by('-post_update_date')

    #添加附加信息
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_list = PostCategory.objects.exclude(name="undefined")
        context["category_list"] = category_list
        return context
# class PostView(DetailView):
#     model = Mypost
#     template_name = "myblog/blog-post.html"
#     context_object_name = "post_info"