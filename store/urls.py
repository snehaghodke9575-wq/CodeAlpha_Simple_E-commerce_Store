
from django.urls import path
from . import views

urlpatterns=[
    path('', views.home,name='home'),
    path('product/<int:id>/',views.product_detail,name='product_detail'),
    path('add-to-cart/<int:id>/',views.add_to_cart,name='add_to_cart'),
    path('cart/',views.cart,name='cart'),
    path('order/',views.place_order,name='place_order'),
    path('order-success/',views.order_success,name='order_success'),
    path('orders/',views.order_history,name='order_history'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart/<int:item_id>/<str:action>/',views.update_cart,name='update_cart'),
    path('payment/<int:order_id>/',views.payment,name='payment'),


    
    
]
