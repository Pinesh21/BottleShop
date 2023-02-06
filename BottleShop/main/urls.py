"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path,include
from . import views
# from userapp import views as userapp_views
from django.contrib.auth import views as auth_views
app_name = 'main'
urlpatterns = [
	#Leave as empty string for base url
	# path('admin/', admin.site.urls),
	path('',views.home,name='home'),
	path('search',views.search,name='search'),
    path('category-list',views.category_list,name='category-list'),
    path('brand-list',views.brand_list,name='brand-list'),
    path('product-list',views.product_list,name='product-list'),
    path('category-product-list/<int:cat_id>',views.category_product_list,name='category-product-list'),
    path('brand-product-list/<int:brand_id>',views.brand_product_list,name='brand-product-list'),
    path('product/<str:slug>/<int:id>',views.product_detail,name='product_detail'),
    path('filter-data',views.filter_data,name='filter_data'),
    path('load-more-data',views.load_more_data,name='load_more_data'),
    path('cat-load-more-data',views.cat_load_more_data,name='cat_load_more_data'),
    path('brand-load-more-data',views.brand_load_more_data,name='brand_load_more_data'),
    path('add-to-cart',views.add_to_cart,name='add_to_cart'),
    path('cart',views.cart_list,name='cart'),
    path('delete-from-cart',views.delete_cart_item,name='delete-from-cart'),
    path('update-cart',views.update_cart_item,name='update-cart'),
    path('checkout',views.checkout,name='checkout'),
    # path('stripe-checkout',views.stripe_checkout,name='strike-checkout'),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('payment-done/', views.payment_done, name='payment_done'),
    path('payment-cancelled/', views.payment_canceled, name='payment_cancelled'),
    path('cancel/', views.CancelledView.as_view(), name='cancel'),
    path('success/', views.SuccessView.as_view(), name='success'),
    path('create-checkout-session/', views.CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('save-review/<int:pid>',views.save_review, name='save-review'),
    # # Wishlist
    path('add-wishlist',views.add_wishlist, name='add_wishlist'),

]