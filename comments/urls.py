from django.urls import path
from . import views

urlpatterns = [
    #path('',views.home),
    path('add_comments/<int:posted_id>/',views.add_comments,name="add_comments"),
]