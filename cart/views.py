from django.shortcuts import render
from .models import Cart

# Create your views here.

def cart(request):
    current_user=request.user
    cart,created=Cart.objects.get_or_create(user=current_user)
    print("================================================")
    print(cart)
    print(created)
    print("================================================")
    return render(request,"cart.html")


def add_to_cart(request,productId):
    return render(request,"cart.html")


def delete_cart_item(request):
    pass

def update_cart_item(request):
    pass




