from django.shortcuts import render,HttpResponseRedirect
from .models import Cart,CartItem,Order,OrderItem
from product.models import Product
from .forms import OrderForm
import uuid
import razorpay
from superpet.settings import RAZORPAY_ID,RAZORPAY_SECRET
from django.views.decorators.csrf import csrf_exempt

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
    if request.method=="GET":
        form=OrderForm()
        return render(request,"checkout.html",{'form':form})
    elif request.method=="POST":
        form=OrderForm(request.POST)
      
        if form.is_valid():
           print(form.cleaned_data)

           order=Order.objects.create(
               order_id=str(uuid.uuid4())[:11],
               user=request.user,
               address_line_1=form.cleaned_data['address_line_1'],
               address_line_2=form.cleaned_data['address_line_1'],
               city=form.cleaned_data['city'],
               state=form.cleaned_data['state'],
               pincode=form.cleaned_data['pincode'],
               phoneno=form.cleaned_data['phoneno'],    
           )

           cart=Cart.objects.get(id=request.session.get('cart_id'))
           for cartitem in cart.cartitem_set.all():
               OrderItem.objects.create(
                   
                   order=order,
                   products=cartitem.products,
                   quantity=cartitem.quantity
                   
               )
               
                 
        return HttpResponseRedirect('/cart/payment/'+order.order_id)
    

def payment(request,order_id):
    order=Order.objects.get(order_id=order_id)
    orderitems=order.orderitem_set.all()

    total=0
    for orderitem in orderitems:
        total+=orderitem.quantity*orderitem.products.product_price


    client=razorpay.Client(auth=(RAZORPAY_ID, RAZORPAY_SECRET))
    data = { "amount": total*100, "currency": "INR", "receipt": order_id }
    payment_details=client.order.create(data=data)
    print(payment_details)

    

    return render(request,"payment.html",{'total':total,'order':order,'razorpayid':RAZORPAY_ID,'payment':payment_details})


@csrf_exempt
def payment_success(request,order_id):
    razorpay_payment_id=request.POST.get('razorpay_payment_id')
    razorpay_order_id=request.POST.get('razorpay_order_id')
    razorpay_signature=request.POST.get('razorpay_signature')

    client=razorpay.Client(auth=(RAZORPAY_ID, RAZORPAY_SECRET))

    client.utility.verify_payment_signature({
        'razorpay_order_id': razorpay_order_id,
       'razorpay_payment_id': razorpay_payment_id,
       'razorpay_signature': razorpay_signature
    })

    return render(request,"success.html")
         



