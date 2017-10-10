from django.shortcuts import render,get_object_or_404
from article.models import Article,Category,Tag
import markdown
# Create your views here.

from django.http import HttpResponse
import pygments
from comments.forms import CommentForm

from django.views.generic import ListView,DetailView

def articlelist(request):
    articles = Article.objects.all()[:10]
    context = {'articles':articles}
    return render(request,'article/articlelist.html',context)

#与首页 文章list 代码一致 可以精简
class ArticlelistView(ListView):
    model= Article
    template_name = 'article/articlelist.html'
    context_object_name = 'articles'

    #分页功能(重复代码)
    paginate_by = 7

    def get_context_data(self,**kwargs):
        context =super().get_context_data(**kwargs)

        paginator= context.get('paginator')
        page = context.get('page_obj')
        is_paginated= context.get('is_paginated')
        #print(paginator,page,is_paginated)
        pagination_data = self.pagination_data(paginator,page,is_paginated)

        #print(pagination_data)
        context.update(pagination_data)

        return context

    def pagination_data(self,paginator,page,is_paginated):
        if not is_paginated:

             return {}

        left = []
        right = []
        left_has_more = False
        right_has_more = False
        first = False
        last = False

        page_number = page.number
        total_pages = paginator.num_pages

        page_range = paginator.page_range

        if page_number == 1 :
            right = page_range[page_number:page_number +2 ]
            if right[-1] < total_pages - 1:
                right_has_more = True

            if right[-1] < total_pages:
                last = True

        elif page_number == total_pages:
            left = page_range[(page_number -3 ) if (page_number -3) > 0 else 0:page_number - 1]

            if left[0] > 2:
                left_has_more = True

            if left[0] > 1:
                first = True

        else:
            left = page_range[(page_number - 3) if (page_number -3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]

            if right[-1] < total_pages - 1:
               right_has_more = True
            if right[-1] < total_pages:
               last = True

            if left[0] > 2:
               left_has_more = True
            if left[0] > 1:
               first = True

        data = {
            'left':left,
            'right': right,
            'left_has_more':left_has_more,
            'right_has_more':right_has_more,
            'first':first,
            'last':last,
             }
        print(data)
        return data

def detail(request,id):
    #pk primary_key 主键
    article= get_object_or_404(Article,pk=id)

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
    return render(request,'article/article.html',context=context)

#文章 基于类
class ArticleDetailView(DetailView):
    model= Article
    template_name = 'article/article.html'
    context_object_name = 'article'

    def get(self,request,*args,**kwargs):
        response= super(ArticleDetailView,self).get(request,*args,**kwargs)
        self.object.increase_view()
        return response

    def get_object(self,queryset=None):
        article = super(ArticleDetailView,self).get_object(queryset=None)
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
        context = super(ArticleDetailView,self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
                      'form':form,
                      'comment_list':comment_list
                      })
        return context



#归档 视图
def archives(request,year,month):
    print(year,month)
    articles = Article.objects.filter(create_time__year=year,
                                      create_time__month=month
                                   ).order_by('-create_time')
    #print(articles)
    context = {'articles':articles}
    return render(request,'article/articlelist.html',context)

#归档 基于类
class Archivesview(ListView):
    model = Article
    template_name = 'article/article_archives_list.html'
    context_object_name = 'articles'

    #分页功能(重复代码)
    paginate_by = 7

    #重写父类的 get_queryset() 方法
    #因为父类的方法是获取整个 model 对象列表，需要修改为获取指定对象列表
    #在此就是 指定归档时间 的文章列表
    def get_queryset(self):
        
        year=self.kwargs.get('year')
        month=self.kwargs.get('month')

        print('get_queryset ok')
        return super(Archivesview,self).get_queryset().filter(create_time__year=year,
                                                              create_time__month=month)

    
    def get_context_data(self,**kwargs):
        context =super().get_context_data(**kwargs)

        paginator= context.get('paginator')
        page = context.get('page_obj')
        is_paginated= context.get('is_paginated')
        print(paginator,page,is_paginated)
        pagination_data = self.pagination_data(paginator,page,is_paginated)

        print('归档',pagination_data)
        context.update(pagination_data)

        #将 归档 年月传给 templates模板
        year=self.kwargs.get('year')
        month=self.kwargs.get('month')
        context['year']=year
        context['month']=month
        print('context:',context)
        return context

    def pagination_data(self,paginator,page,is_paginated):
        if not is_paginated:

             return {}

        left = []
        right = []
        left_has_more = False
        right_has_more = False
        first = False
        last = False

        page_number = page.number
        total_pages = paginator.num_pages

        page_range = paginator.page_range

        if page_number == 1 :
            right = page_range[page_number:page_number +2 ]
            if right[-1] < total_pages - 1:
                right_has_more = True

            if right[-1] < total_pages:
                last = True

        elif page_number == total_pages:
            left = page_range[(page_number -3 ) if (page_number -3) > 0 else 0:page_number - 1]

            if left[0] > 2:
                left_has_more = True

            if left[0] > 1:
                first = True

        else:
            left = page_range[(page_number - 3) if (page_number -3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]

            if right[-1] < total_pages - 1:
               right_has_more = True
            if right[-1] < total_pages:
               last = True

            if left[0] > 2:
               left_has_more = True
            if left[0] > 1:
               first = True

        data = {
            'left':left,
            'right': right,
            'left_has_more':left_has_more,
            'right_has_more':right_has_more,
            'first':first,
            'last':last,
             }
        print(data)
        return data
        


#分类 视图
def category(request,pk):
    cate = get_object_or_404(Category,pk=pk)
    articles = Article.objects.filter(category=cate).order_by('-create_time')
    context={'articles':articles,'category':cate}
    return render(request,'article/article_category_list.html',context)

#分类 基于类
class CategoryView(ListView):
    model = Article
    template_name = 'article/article_category_list.html'
    context_object_name = 'articles'

    paginate_by = 5
   
    #重写父类的 get_queryset() 方法
    def get_queryset(self):
        cate = get_object_or_404(Category,pk=self.kwargs.get('pk'))
        #print('cate',cate)
        return super(CategoryView,self).get_queryset().filter(category=cate)


    def get_context_data(self,**kwargs):
        context =super().get_context_data(**kwargs)

        paginator= context.get('paginator')
        page = context.get('page_obj')
        is_paginated= context.get('is_paginated')
        pagination_data = self.pagination_data(paginator,page,is_paginated)

        print('分类',pagination_data)
        context.update(pagination_data)
        name= get_object_or_404(Category,pk=self.kwargs.get('pk'))
        #print('name:',name)
        context['categoryname'] = name
        print('context',context)
        return context

    #分页功能（重复代码）
    def pagination_data(self,paginator,page,is_paginated):
        if not is_paginated:

             return {}

        left = []
        right = []
        left_has_more = False
        right_has_more = False
        first = False
        last = False

        page_number = page.number
        total_pages = paginator.num_pages

        page_range = paginator.page_range

        if page_number == 1 :
            right = page_range[page_number:page_number +2 ]
            if right[-1] < total_pages - 1:
                right_has_more = True

            if right[-1] < total_pages:
                last = True

        elif page_number == total_pages:
            left = page_range[(page_number -3 ) if (page_number -3) > 0 else 0:page_number - 1]

            if left[0] > 2:
                left_has_more = True

            if left[0] > 1:
                first = True

        else:
            left = page_range[(page_number - 3) if (page_number -3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]

            if right[-1] < total_pages - 1:
               right_has_more = True
            if right[-1] < total_pages:
               last = True

            if left[0] > 2:
               left_has_more = True
            if left[0] > 1:
               first = True

        data = {
            'left':left,
            'right': right,
            'left_has_more':left_has_more,
            'right_has_more':right_has_more,
            'first':first,
            'last':last,
             }
        return data

#标签 基于类
class TagView(ListView):
    model = Article
    template_name = 'article/article_tag_list.html'
    context_object_name = 'articles'
    paginate_by = 5

    #重写父类的 get_queryset() 方法
    def get_queryset(self):
        cate = get_object_or_404(Tag,pk=self.kwargs.get('pk'))
        print('tag',cate)
        return super(TagView,self).get_queryset().filter(tags=cate)


    def get_context_data(self,**kwargs):
        context =super().get_context_data(**kwargs)

        paginator= context.get('paginator')
        page = context.get('page_obj')
        is_paginated= context.get('is_paginated')
        pagination_data = self.pagination_data(paginator,page,is_paginated)

        context.update(pagination_data)
        name= get_object_or_404(Tag,pk=self.kwargs.get('pk'))
        print('tagname:',name)
        context['tagname'] = name

        return context

    #分页功能（重复代码）
    def pagination_data(self,paginator,page,is_paginated):
        if not is_paginated:

             return {}

        left = []
        right = []
        left_has_more = False
        right_has_more = False
        first = False
        last = False

        page_number = page.number
        total_pages = paginator.num_pages

        page_range = paginator.page_range

        if page_number == 1 :
            right = page_range[page_number:page_number +2 ]
            if right[-1] < total_pages - 1:
                right_has_more = True

            if right[-1] < total_pages:
                last = True

        elif page_number == total_pages:
            left = page_range[(page_number -3 ) if (page_number -3) > 0 else 0:page_number - 1]

            if left[0] > 2:
                left_has_more = True

            if left[0] > 1:
                first = True

        else:
            left = page_range[(page_number - 3) if (page_number -3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]

            if right[-1] < total_pages - 1:
               right_has_more = True
            if right[-1] < total_pages:
               last = True

            if left[0] > 2:
               left_has_more = True
            if left[0] > 1:
               first = True

        data = {
            'left':left,
            'right': right,
            'left_has_more':left_has_more,
            'right_has_more':right_has_more,
            'first':first,
            'last':last,
             }
        return data
