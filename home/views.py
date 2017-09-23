#coding:utf-8
from django.shortcuts import render

# Create your views here.
from article.models import Article,Tag,Category
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

def index(request):
    #return HttpResponse("时空构建中")
    #context ={'title':'川陀图书馆','text':'时空构建中' }
    #return render(request,'home/index.html',context)

    articles = Article.objects.all().order_by('-create_time')[:10]

    context = {'articles':articles}
    return render(request,'home/index.html',context)

