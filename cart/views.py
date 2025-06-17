from django.shortcuts import render,HttpResponseRedirect
from .models import Cart,CartItem
from product.models import Product
from .forms import OrderForm

# Create your views here.

def cart(request):
    current_user=request.user
    cart,created=Cart.objects.get_or_create(user=current_user)
    request.session['cart_id']=cart.id
    cartitems=cart.cartitem_set.all()
    total=0
    for cartitem in cartitems:
        total+=cartitem.quantity*cartitem.products.product_price

    return render(request,"cart.html",{"cartitems":cartitems,"total":total})


def add_to_cart(request,productId):
    current_user=request.user
    cart,created=Cart.objects.get_or_create(user=current_user)
    request.session['cart_id']=cart.id
    cartitem,cartitem_created=CartItem.objects.get_or_create(cart=cart,products=Product.objects.get(id=productId))
    
    quantity=int(request.GET.get('quantity'))

    if cartitem_created:
        cartitem.quantity=quantity
    else:
        cartitem.quantity=cartitem.quantity+quantity
    
    cartitem.save()
    
    print(request.META.get("HTTP_REFERER"))
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def delete_cart_item(request,cartitem_id):
    cartitem=CartItem.objects.get(id=cartitem_id)
    cartitem.delete()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def update_cart_item(request,cartitem_id):
    cartitem=CartItem.objects.get(id=cartitem_id)
    quantity= request.GET.get("quantity")
    cartitem.quantity=quantity
    cartitem.save()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def checkout(request):
    form=OrderForm()
    return render(request,"checkout.html",{'form':form})


