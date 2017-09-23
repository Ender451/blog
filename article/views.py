from django.shortcuts import render,get_object_or_404
from article.models import Article,Category
import markdown
# Create your views here.

from django.http import HttpResponse
import pygments
from comments.forms import CommentForm

def articlelist(request):
    articles = Article.objects.all()[:10]
    context = {'articles':articles}
    return render(request,'article/articlelist.html',context)

def detail(request,id):
    #pk primary_key 主键
    article= get_object_or_404(Article,pk=id)

    article.body = markdown.markdown(article.body,
                                     extensions=[
                                         'markdown.extensions.extra',
                                         'markdown.extensions.codehilite',
                                         'markdown.extensions.toc',
                                               ]
                                    )
    form = CommentForm()
    comment_list = article.comment_set.all()

    context={
             'article':article,
             'form':form,
             'comment_list':comment_list
            }
    return render(request,'article/article.html',context=context)

#归档 视图
def archives(request,year,month):
    print(year,month)
    articles = Article.objects.filter(create_time__year=year,
                                      create_time__month=month
                                   ).order_by('-create_time')
    #print(articles)
    context = {'articles':articles}
    return render(request,'article/articlelist.html',context)

#分类 视图
def category(request,pk):
    cate = get_object_or_404(Category,pk=pk)
    print('-----------------')
    print('cate:',cate)
    articles = Article.objects.filter(category=cate).order_by('-create_time')
    context={'articles':articles,'category':cate}
    return render(request,'article/articletaglist.html',context)

   
