import razorpay
from django.conf import settings
from django.shortcuts import render,get_object_or_404,redirect
from .models import Product
from .models import Cart 
from .models import Order
from django.contrib.auth.decorators import login_required 




def home(request):
    products=Product.objects.all()
    return render(request, 'store/home.html',{'products': products})

def product_detail(request,id):
    product= get_object_or_404(Product, id=id)
    return render(request, 'store/product_detail.html',{'product': product})


def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)
    cart_item, created = Cart.objects.get_or_create(user=request.user,product=product)
    if not created:
        cart_item.quantity += 1
    else:
        cart_item.quantity = 1
    cart_item.save()
    return redirect('cart')

def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'store/cart.html',{'cart_items':cart_items, 'total': total})

def place_order(request):
    user=request.user
    cart_items= Cart.objects.filter(user=user)
    
    total=0
    for item in cart_items:
        total += item.product.price * item.quantity

    order=Order.objects.create(
        user=user,
        total_price=total
    )
    cart_items.delete()
    return redirect('payment', order_id=order.id)
    

def order_success(request):
    order = Order.objects.filter(user=request.user).last()
    return render(request,'store/order_success.html',{'total':order.total_price})

def order_history(request):
    orders=Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/order_history.html',{'orders': orders})

def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
    cart_item.delete()
    return redirect('cart')

def update_cart(request,item_id,action):
    cart_item=Cart.objects.get(id=item_id,user=request.user)

    if action=='plus':
        cart_item.quantity += 1

    elif action == 'minus':
        if cart_item.quantity >1:
            cart_item.quantity -= 1
        
        else:
            cart_item.delete()
            return redirect('cart')
        
    cart_item.save()
    return redirect('cart')

def payment(request,order_id):
    order = Order.objects.get(id=order_id,user=request.user)
    client= razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    razorpay_order= client.order.create({
        'amount': order.total_price * 100,
        'currency': 'INR',
        'payment_capture': '1'
    })
    order.payment_id=razorpay_order['id']
    order.save()
    return render (request,'store/payment.html',{ 
        'razorpay_key_id': settings .RAZORPAY_KEY_ID,
        'order_id': razorpay_order['id'],
        'amount':order.total_price   
    })
        

    






# Create your views here.

