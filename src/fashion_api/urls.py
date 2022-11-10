"""fashion_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

# from django.views import index,blog,post
from fashion_api.views import index, about

# from django.views import index,blog,post
from fashion_api.views import index, about, create, login, signup, search_i, overall_list, outer_list, bottom_list, top_list, product_info

urlpatterns = [
    path("",index),
    path("index",index),
    path("about",about),
    path("create",create),
    path("login",login),
    path("signup",signup),
    path("Overall-list",overall_list),
    path("Top-list",top_list),
    path("Bottom-list",bottom_list),
    path("Outer-list",outer_list),  
    path("search_i",search_i),
    path("product-info",product_info),
    path("admin/", admin.site.urls),
    path("api/account/", include('account.urls')),
    path("api/product/", include('product.urls')),
    path("api/image/", include('image.urls')),
    path("api/analysis/", include('analysis.urls')),
    path("api/search/", include('search.urls')),
    path("api/label/", include('label.urls')),
]

# django media
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static

# django media
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
