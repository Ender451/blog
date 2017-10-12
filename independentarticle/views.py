from django.shortcuts import render,get_object_or_404
from independentarticle.models import Independentarticle
import markdown
# Create your views here.

from django.http import HttpResponse
import pygments
from comments.forms import CommentForm

from django.views.generic import DetailView



def detail(request,id):
    #pk primary_key 主键
    article= get_object_or_404(Independentarticle,pk=id)

    #阅读量+1
    article.increase_views()

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
    return render(request,'independentarticle/independentarticle.html',context=context)

#temp
#文章 基于类
class IndependentarticleDetailView(DetailView):
    model= Independentarticle
    template_name = 'independentarticle/independentarticle.html'
    context_object_name = 'article'

    def get(self,request,*args,**kwargs):
        response= super(IndependentarticleDetailView,self).get(request,*args,**kwargs)
        self.object.increase_view()
        return response

    def get_object(self,queryset=None):
        article = super(IndependentarticleDetailView,self).get_object(queryset=None)
        article.body = markdown.markdown(
                                        article.body,
                                        extensions=[
                                            'markdown.extensions.extra',
                                            'markdown.extensions.codehilite',
                                            'markdown.extensions.toc',
                                                   ]
                                        )       
        return article

    def get_context_data(self,**kwargs):
        context = super(IndependentarticleDetailView,self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
                      'form':form,
                      'comment_list':comment_list
                      })
        return context

