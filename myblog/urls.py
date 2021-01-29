from django.urls import path
from . import views

urlpatterns = [
    #path('',views.home),
    path('blog-home/',views.HomeView.as_view(),name="blog_home"),
    path('mypost/<int:post_id>/',views.postview,name="post_detail"),
    path('category/',views.CategoryView.as_view(),name="showcategory"),
    path('error/',views.error_handle,name="error"),
]