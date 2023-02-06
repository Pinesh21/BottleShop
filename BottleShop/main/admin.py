from django.contrib import admin
from .models import Banner,Category,Brand,Color,Size,Product,ProductAttribute,CartOrder,CartOrderItems,ProductReview,Wishlist,UserAddressBook
# Register your models here.
admin.site.register(Size)

class BannerAdmin (admin.ModelAdmin):
    list_display = ('alt_text','image_tag')#Image_tag is in modely.py, it is to show image in admin page for particular  category

admin.site.register(Banner,BannerAdmin)



class CategoryAdmin (admin.ModelAdmin):
    list_display = ('title','image_tag')#Image_tag is in modely.py, it is to show image in admin page for particular  category

admin.site.register(Category,CategoryAdmin)


class BrandAdmin (admin.ModelAdmin):
    list_display = ('title','image_tag')#Image_tag is in modely.py, it is to show image in admin page for particular  category

admin.site.register(Brand,BrandAdmin)



class ColorAdmin (admin.ModelAdmin):
    list_display = ('title','color_bg')#color_bg is in modely.py, it is to show color_code in admin page for particular  category

admin.site.register(Color,ColorAdmin)

class ProductAdmin (admin.ModelAdmin):
    list_display = ('id','title','brand','category','status','is_featured')
    list_editable = ('brand','category','status','is_featured')

admin.site.register(Product,ProductAdmin)



class ProductAttributeAdmin (admin.ModelAdmin):
    list_display = ('id','product','price','color','size','image_tag')
    list_editable = ('product','price','color','size')
admin.site.register(ProductAttribute,ProductAttributeAdmin)



class CartOrderAdmin (admin.ModelAdmin):
    list_display = ('user','total_amt','paid_status','order_dt','order_status')
admin.site.register(CartOrder,CartOrderAdmin)



class CartOrderItemsAdmin (admin.ModelAdmin):
    list_display = ('order','invoice_no','item','image','qty','price','total')

admin.site.register(CartOrderItems,CartOrderItemsAdmin)


class ProductReviewAdmin (admin.ModelAdmin):
    list_display = ('id','review_text','get_review_rating','product','user')
    list_editable = ('review_text',)
admin.site.register(ProductReview,ProductReviewAdmin)

admin.site.register(Wishlist)


class UserAddressBookAdmin (admin.ModelAdmin):
    list_display = ('user','mobile','address','status')
    list_editable = ('mobile','address','status')
admin.site.register(UserAddressBook,UserAddressBookAdmin)
