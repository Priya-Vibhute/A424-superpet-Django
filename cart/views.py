from django.shortcuts import render,HttpResponseRedirect
from .models import Cart,CartItem
from product.models import Product

# Create your views here.

def cart(request):
    current_user=request.user
    cart,created=Cart.objects.get_or_create(user=current_user)
    cartitems=cart.cartitem_set.all()
    return render(request,"cart.html",{"cartitems":cartitems})


def add_to_cart(request,productId):
    current_user=request.user
    cart,created=Cart.objects.get_or_create(user=current_user)
    cartitem,cartitem_created=CartItem.objects.get_or_create(cart=cart,products=Product.objects.get(id=productId))
    
    quantity=int(request.GET.get('quantity'))

    if cartitem_created:
        cartitem.quantity=quantity
    else:
        cartitem.quantity=cartitem.quantity+quantity
    
    cartitem.save()
    
    print(request.META.get("HTTP_REFERER"))
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def delete_cart_item(request):
    pass

def update_cart_item(request):
    pass




