from .models import Banner,Category,Brand,Product,ProductAttribute
from django.db.models import Min,Max

def get_filters(request):
    colors = ProductAttribute.objects.distinct().values('color__title', 'color__id', 'color__color_code')
    cats = Product.objects.distinct().values('category__title', 'category__id')
    brands = Product.objects.distinct().values('brand__title', 'brand__id')
    sizes = ProductAttribute.objects.distinct().values('size__title', 'size__id')
    minMaxPrice = ProductAttribute.objects.aggregate(Min('price'),Max('price'))
    data={'colors':colors,
			'cats': cats,
			'brands': brands,
			'sizes': sizes,
            'minMaxPrice':minMaxPrice
          }
    return data