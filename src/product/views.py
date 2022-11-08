from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product, Description, Image
from account.models import User

# Create your views here.

#이미지 검사는 따로 -> search에서 진행

def productRegister(request):
    if request.method == 'GET':
        return render(request, 'product_register.html')
    elif request.method == 'POST':
        productName = request.POST['productName']
        productMemo = request.POST['productMemo']
        price = request.POST['price']

        if not(productName and price):
            return render(request, 'product_register.html')
        else:
            #기본 정보 저장
            description = Description(
                productName = productName,
                productMemo = productMemo,
                price = price,
            )
            description.save()
            product = Product(
                description = description,
                #판매자 정보 세션 정보 불러와서 저장
            )
            product.save()
            #썸네일 이미지 저장
            thumbnail = Image(
                image = request.POST['thumbnail'],
                isThumbnail = True,
            )
            thumbnail.save()
            #상세 이미지들 저장
            for img in request.POST['images']:
                image = Image(
                    image = img,
                )
                image.save()
            return redirect('home')

def myProductList(request):
    if request.method == 'GET':
        return render(request, 'my_product_list.html')
    elif request.method == 'POST':
        #세션정보 받아와서 해당 userid에 해당하는 모든 product 받아오기
        productList = Product.objects.filter()
        