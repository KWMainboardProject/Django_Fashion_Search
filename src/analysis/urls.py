"""carom_api URL Configuration

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
from .views import AnalysisStateSViewSet, ImageAttributesSViewSet

#define ViewSet
AnalysisState_list = AnalysisStateSViewSet.as_view({
    'get' : 'list',
})
AnalysisState_detail = AnalysisStateSViewSet.as_view({
    'get' : 'retrieve',
    'delete' : 'destroy'
})
ImageAttributes_list = ImageAttributesSViewSet.as_view({
    'get' : 'list',
})
ImageAttributes_detail = ImageAttributesSViewSet.as_view({
    'get' : 'retrieve',
    'delete' : 'destroy'
})
#define url pattern
urlpatterns = [
    # path("fashion/<int:carom_id>/<str:usr>/", DetectRequestAPIView.as_view()),
    path("state/", AnalysisState_list),
    path("state/<int:id>/", AnalysisState_detail),
    path("attributes/class/", ImageAttributes_list),
    path("attributes/class/<int:id>/", ImageAttributes_detail),
]