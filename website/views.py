from django.http import HttpResponse
from django.shortcuts import render,redirect
import datetime
def home(request):
    page_info = {}
    page_info["info"] = ["hello ","world"]
    page_info["time"]  = datetime.datetime.now()
    return render(request, 'homepage.html', {"page_info":page_info})
