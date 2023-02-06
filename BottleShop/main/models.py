from django.db import models
from django.utils.html import mark_safe
# from django_countries.fields import CountryField
from PIL import Image
from django.contrib.auth.models import User

# Create your models here.

class Banner(models.Model):
    img=models.ImageField(upload_to="banner_imgs/",null=True)
    alt_text=models.CharField(max_length=300)

    class Meta:
        verbose_name_plural='1. Banners'

    def image_tag(self):
        return mark_safe('<img src="%s" width="100" />' % (self.img.url))

    def __str__(self):
        return self.alt_text

    @property
    def imageURL(self):
        '''

        :return: url as '' if no image is found for product in db, other option, you could set to default image while
        creating db model
        '''
        try:
            url = self.img.url
        except:
            url = ''
        return url


class Category(models.Model):
    title =models.CharField(max_length=100)
    image =models.ImageField(upload_to="cat_imgs/",null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural='2. Category'


    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    @property
    def imageURL(self):
        '''

        :return: url as '' if no image is found for product in db, other option, you could set to default image while
        creating db model
        '''
        try:
            url = self.image.url
        except:
            url = ''
        return url

        # Override save method to resize profile pic


class Brand(models.Model):
    title =models.CharField(max_length=100)
    image =models.ImageField(upload_to="brand_imgs/",null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural='3. Brand'

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    @property
    def imageURL(self):
        '''

        :return: url as '' if no image is found for product in db, other option, you could set to default image while
        creating db model
        '''
        try:
            url = self.image.url
        except:
            url = ''
        return url

        # Override save method to resize profile pic


class Color(models.Model):
    title =models.CharField(max_length=100)
    color_code = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural='4. Color'

    def color_bg(self):
        return mark_safe('<div style="width:30px; height:30px; background-color:%s"></div>' % (self.color_code))

class Size(models.Model):
    title =models.CharField(max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural='5. Size'

class Product(models.Model):
    title =models.CharField(max_length=200)
    slug =models.SlugField(max_length=400)
    detail =models.TextField()
    specs=models.TextField()
    # price = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
    # color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True)
    # size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True)
    status = models.BooleanField(default=True)
    is_featured= models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural='6. Product'




# Product Attribute
class ProductAttribute(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    color=models.ForeignKey(Color,on_delete=models.CASCADE)
    size=models.ForeignKey(Size,on_delete=models.CASCADE)
    price=models.PositiveIntegerField(default=0)
    image=models.ImageField(upload_to="product_imgs/",null=True)

    class Meta:
        verbose_name_plural='7. ProductAttributes'

    def __str__(self):
        return self.product.title

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    @property
    def imageURL(self):
        '''

        :return: url as '' if no image is found for product in db, other option, you could set to default image while
        creating db model
        '''
        try:
            url = self.image.url
        except:
            url = ''
        return url

        # Override save method to resize profile pic
    def save(self):
        super().save()

        img = Image.open(self.image.path)
        if img.height> 300 or img.width> 300:
            output_size =(300, 300)
            img.thumbnail (output_size)
            img.save(self.image.path)


# Order
status_choice=(
        ('process','In Process'),
        ('shipped','Shipped'),
        ('delivered','Delivered'),
    )




class CartOrder(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    total_amt=models.FloatField(null=True)
    paid_status=models.BooleanField(default=False)
    order_dt=models.DateTimeField(auto_now_add=True)
    order_status=models.CharField(choices=status_choice,default='process',max_length=150)
    # coupon = models.ForeignKey(
    #     Coupon, on_delete=models.SET_NULL, blank=True, null=True)
    # ordered_date = models.DateTimeField()
    # ordered = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.user.username}'s order"


    class Meta:
        verbose_name_plural='8. Orders'

# OrderItems
class CartOrderItems(models.Model):
    order=models.ForeignKey(CartOrder,on_delete=models.CASCADE)
    invoice_no=models.CharField(max_length=150)
    item=models.CharField(max_length=150)
    image=models.CharField(max_length=200)
    qty=models.IntegerField()
    price=models.FloatField()
    total=models.FloatField()

    class Meta:
        verbose_name_plural='9. Order Items'

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    # @property
    # def imageURL(self):
    #     '''
    #
    #     :return: url as '' if no image is found for product in db, other option, you could set to default image while
    #     creating db model
    #     '''
    #     try:
    #         url = self.image.url
    #     except:
    #         url = ''
    #     return url

# Product Review
RATING=(
    (1,'1'),
    (2,'2'),
    (3,'3'),
    (4,'4'),
    (5,'5'),
)
class ProductReview(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    review_text=models.TextField()
    review_rating=models.CharField(choices=RATING,max_length=150)

    class Meta:
        verbose_name_plural='10. Reviews'

    def get_review_rating(self):
        return self.review_rating

# WishList
class Wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural='Wishlist'

# AddressBook
class UserAddressBook(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    mobile=models.CharField(max_length=50,null=True)
    address=models.TextField()
    status=models.BooleanField(default=False)

    class Meta:
        verbose_name_plural='AddressBook'


