from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('',login_required(CreateShop.as_view(), login_url='login' ) , name='create-shop' ),

    path('manage-shop' , login_required(ShopManagement.as_view() , login_url='login') , name='shop-management'),

    path('<str:slug>' , ShopView.as_view() , name='shop-view'  ),

    path('<str:shop>/<str:slug>/<int:id>' , ProductDetail.as_view() , name='prodect-detail' ),

    path('<str:shop>/cart' , CartView.as_view() , name='cart-view' ),

    path('<str:shop>/update_item', updateItem , name='update_item'),
    
    path('<str:shop>/checkout', CheckoutView.as_view() , name='checkout'),

    path('manage-shop/orders-complete',login_required(OrdersComplete.as_view() , login_url='login'), name='orders-copmlete'  ),
    
    path('manage-shop/orders-complete/<int:id>/submit',login_required( SubmitOrder.as_view() , login_url='login' ),name='sumbit_order'),

    path('<str:slug>/all' , AllProduct.as_view() , name='all-product'),

    path('manage-shop/create-page',create_page , name='create-page' ),

    path('<str:shop>/<str:slug>/<int:id>/page' , ViewPages.as_view() , name='view-page'),

    path('manage-shop/<int:id>/edit' ,login_required(ProductEdit.as_view() , login_url='login' ) , name='edit-product' ),

    path('manage-shop/categorie',categorie , name='categorie'),
]