from django.shortcuts import render

# Create your views here.


from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from . import models


def index(request):
	context={'messages' : 'It is working'}
	return render(request, 'online/index.html', context)

