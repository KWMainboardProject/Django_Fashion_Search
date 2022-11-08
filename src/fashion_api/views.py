from django.shortcuts import render

def index(request):
    return render(request, 'fashion_api/index.html')

def about(request):
    return render(request,'fashion_api/about.html')

def create(request):
    return render(request, 'fashion_api/create.html')

def login(request):
    return render(request, 'fashion_api/login.html')

def signup(request):
    return render(request, 'fashion_api/signup.html')

def search_i(request):
    return render(request, 'fashion_api/search_i.html')

def outer_list(request):
    return render(request, 'fashion_api/outer_list.html')

def overall_list(request):
    return render(request, 'fashion_api/overall_list.html')

def bottom_list(request):
    return render(request, 'fashion_api/bottom_list.html')

def top_list(request):
    return render(request, 'fashion_api/top_list.html')

def product_info(request):
    return render(request, 'fashion_api/product-info.html')