"""BottleShop URL Configuration

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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from userapp import views as userapp_views

urlpatterns = [
    # path('jet/', include('jet.urls', namespace='jet')),
    # path('jet/dashboard/', include('jet.dashboard.urls',namespace='jet-dashboard')),
    path('admin/', admin.site.urls),
    path('', include('main.urls', namespace='main')),
    path('login/', auth_views.LoginView.as_view(template_name='userapp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='userapp/logout.html'), name='logout'),
    path('signup/', userapp_views.signup,name='signup'),
    # path('profile/', userapp_views.profile, name='profile'),
    # path('register_with_email/', userapp_views.register_with_email,name='register_with_email'),
# User Dashboard Section Start
    path('my-dashboard',userapp_views.my_dashboard, name='my_dashboard'),
    path('my-orders',userapp_views.my_orders, name='my_orders'),
    path('my-orders-items/<int:id>',userapp_views.my_order_items, name='my_order_items'),
    path('my-wishlist',userapp_views.my_wishlist, name='my_wishlist'),
    path('delete-from-wishlist/<int:pid>',userapp_views.delete_from_wishlist,name='delete_from_wishlist'),
    path('my-reviews',userapp_views.my_reviews, name='my_reviews'),
# End
# # My AddressBook
    path('my-addressbook',userapp_views.my_addressbook, name='my_addressbook'),
    path('add-address',userapp_views.save_address, name='add_address'),
    path('activate-address',userapp_views.activate_address, name='activate-address'),
    path('update-address/<int:id>',userapp_views.update_address, name='update_address'),
    # path('edit-profile',views.edit_profile, name='edit-profile'),



]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)