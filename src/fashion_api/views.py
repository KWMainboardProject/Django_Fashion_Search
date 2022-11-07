from django.shortcuts import render

def index(request):
    return render(request, 'fashion_api/index.html')

def about(request):
    return render(request,'fashion_api/about.html')


