# coding:utf-8
from django.shortcuts import render,get_object_or_404,redirect
from article.models import Article
from independentarticle.models import Independentarticle

from .models import Comment
from .forms import CommentForm

# Create your views here.


#一般文章的评论提交
def article_comment(request,article_pk):
    article = get_object_or_404(Article,pk=article_pk)
    print('article:',article)
    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article     
            
            comment.save()

            return redirect(article)

        else:
            comment_list = article.comment_set.all()
            context ={
                     'article':article,
                     'form':form,
                     'comment_list':comment_list
                     }        
            return render(request,'article/article.html',context=context)
     
    return redirect(article)


#独立文章的评论提交
def independentarticle_comment(request,article_pk):
    article = get_object_or_404(Independentarticle,pk=article_pk)
    print('in-article:',article)
    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.independentarticle = article  #comment.independentarticle 外键

            comment.save()

            return redirect(article)

        else:
            comment_list = article.comment_set.all()
            context ={
                     'article':article,
                     'form':form,
                     'comment_list':comment_list
                     }
            return render(request,'independentarticle/independentarticle.html',context=context)

    return redirect(article)
