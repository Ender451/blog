#coding:utf-8
from django.shortcuts import render

# Create your views here.
from article.models import Article,Tag,Category
from home.models import Visitors
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import time

def index(request):
    #return HttpResponse("时空构建中")
    #context ={'title':'川陀图书馆','text':'时空构建中' }
    #return render(request,'home/index.html',context)

    articles = Article.objects.all().order_by('-create_time')[:10]

    context = {'articles':articles}
    return render(request,'home/index.html',context)

#基于类 的通用视图
class IndexView(ListView):
    model= Article
    template_name = 'home/index.html'
    context_object_name = 'articles'
 
    #分页功能
    paginate_by = 7
    
    def get_context_data(self,**kwargs):
        context =super().get_context_data(**kwargs)
        
        #访客人数统计 +1
        day = str(time.strftime('%Y-%m-%d',time.localtime(time.time())))
        print(day)
        #access = Visitors.objects.filter(Visit_day=day)
        access = get_object_or_404(Visitors,Visit_day=day)
        if access:
            access.increase_Visitors_number()
        else:
            access = Visitors.objects.create(Visit_day=day,Visitors_number=0)                                       

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
