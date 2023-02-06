from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
from .models import Banner,Category,Brand,Product,ProductAttribute,CartOrder,CartOrderItems,ProductReview,Wishlist,UserAddressBook
from django.db.models import Max,Min,Count,Avg
from django.db.models.functions import ExtractMonth
from django.template.loader import render_to_string
from .forms import ReviewAdd
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required
from .forms import CheckoutForm
#paypal
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from django.views.generic import ListView,DetailView,View,FormView,TemplateView
import stripe


# Home Page

def home(request):
    banners=Banner.objects.all().order_by('-id')
    #Follwing is to show only featured product on landing/home screen with filter is_featured which is set in product folder
    data=Product.objects.filter(is_featured =True).order_by('-id')
    # return redirect("main:home", data=data)
    return render(request,'main/index.html',{'data':data,'banners':banners})

# Category
def category_list(request):
    data=Category.objects.all().order_by('-id')
    # return redirect("main:category-list", data=data)
    return render(request,'main/category_list.html',{'data':data})

# Brand
def brand_list(request):
    data=Brand.objects.all().order_by('-id')
    return render(request,'main/brand_list.html',{'data':data})

# Product List
def product_list(request):
    total_data=Product.objects.count()
    data=Product.objects.all().order_by('-id')[:3]
    min_price=ProductAttribute.objects.aggregate(Min('price'))
    max_price=ProductAttribute.objects.aggregate(Max('price'))
    return render(request,'main/product_list.html',
        {
            'data':data,
            'total_data':total_data,
            'min_price':min_price,
            'max_price':max_price,
            'SHOW_CATEGORY_FILTERS_FLAG': True,
            'SHOW_BRAND_FILTERS_FLAG': True
        }
        )

# Product List According to Category
def category_product_list(request,cat_id):
    category=Category.objects.get(id=cat_id)
    total_data = Product.objects.filter(category=category).count()
    data=Product.objects.filter(category=category).order_by('-id')[:3]
    return render(request,'main/category_product_list.html',{
            'data':data,
            'total_data':total_data,
            'category':category,
            'cat_id':cat_id,
            'SHOW_CATEGORY_FILTERS_FLAG':False,
            'SHOW_BRAND_FILTERS_FLAG': True
            })

# Product List According to Brand
def brand_product_list(request,brand_id):
    brand=Brand.objects.get(id=brand_id)
    total_data = Product.objects.filter(brand=brand).count()
    data=Product.objects.filter(brand=brand).order_by('-id')[:3]
    return render(request,'main/brand_product_list.html',{
            'data':data,
            'total_data': total_data,
            'brand': brand,
            'brand_id': brand_id,
            'SHOW_CATEGORY_FILTERS_FLAG': True,
            'SHOW_BRAND_FILTERS_FLAG':False
            })

# Product Detail
def product_detail(request,slug,id):
    pass
    product=Product.objects.get(id=id)
    related_products=Product.objects.filter(category=product.category).exclude(id=id)[:4]
    #Select all color columns for particualr product
    colors=ProductAttribute.objects.filter(product=product).values('color__id','color__title','color__color_code').distinct()
    #Select all size columns for particular product and also pick color id
    sizes=ProductAttribute.objects.filter(product=product).values('size__id','size__title','price','color__id').distinct()
    reviewForm=ReviewAdd()

    # Check
    canAdd=True
    if request.user.is_authenticated:
        reviewCheck = ProductReview.objects.filter(user=request.user, product=product).count()
        if reviewCheck > 0:
           canAdd=False
    # End

    # Fetch reviews
    reviews=ProductReview.objects.filter(product=product)
    # End

    # Fetch avg rating for reviews
    avg_reviews=ProductReview.objects.filter(product=product).aggregate(avg_rating=Avg('review_rating'))
    # End

    return render(request, 'main/product_detail.html',{'data':product,
                                                       'related':related_products,
                                                       'colors':colors,
                                                       'sizes':sizes,
                                                       'reviewForm':reviewForm,
                                                       'canAdd':canAdd,
                                                       'reviews':reviews,
                                                       'avg_reviews':avg_reviews
    })

# Search
def search(request):
    q=request.GET['q']
    data=Product.objects.filter(title__icontains=q).order_by('-id')
    return render(request,'main/search.html',{'data':data})

# Filter Data
def filter_data(request):
    # return JsonResponse({'data':'hello '})
    colors=request.GET.getlist('color[]')
    categories=request.GET.getlist('category[]')
    brands=request.GET.getlist('brand[]')
    sizes=request.GET.getlist('size[]')
    minPrice=request.GET['minPrice']
    maxPrice=request.GET['maxPrice']
    allProducts=Product.objects.all().order_by('-id').distinct()
    allProducts=allProducts.filter(productattribute__price__gte=minPrice)
    allProducts=allProducts.filter(productattribute__price__lte=maxPrice)
    # distinct added below as same bottle could have red and green color
    if len(colors)>0:
        allProducts=allProducts.filter(productattribute__color__id__in=colors).distinct()
    if len(categories)>0:
        allProducts=allProducts.filter(category__id__in=categories).distinct()
    if len(brands)>0:
        allProducts=allProducts.filter(brand__id__in=brands).distinct()
    if len(sizes)>0:
        allProducts=allProducts.filter(productattribute__size__id__in=sizes).distinct()
    t=render_to_string('ajax/product_list.html',{'data':allProducts})
    return JsonResponse({'data':t})

# Load More
def load_more_data(request):
    offset=int(request.GET['offset'])
    limit=int(request.GET['limit'])
    # cat_id = int(request.GET['cat_id'])
    # data = Product.objects.all().order_by('-id')
    # if cat_id is not None:
    #     data = data.filter(category__id__in=cat_id).distinct()[offset:offset+limit]
    # else:
    #     data = Product.objects.all().order_by('-id')[offset:offset + limit]
    data = Product.objects.all().order_by('-id')[offset:offset + limit]
    t=render_to_string('ajax/product_list.html',{'data':data})
    return JsonResponse({'data':t}
)

# Load More within Category
def cat_load_more_data(request):
    offset=int(request.GET['offset'])
    limit=int(request.GET['limit'])
    cat_id = int(request.GET['cat_id'])
    category = Category.objects.get(id=cat_id)
    # total_data = Product.objects.filter(category=category).count()
    data = Product.objects.filter(category=category).order_by('-id')[offset:offset + limit]
    # data = Product.objects.all().order_by('-id')[offset:offset + limit]
    t=render_to_string('ajax/cat_product_list.html',{'data':data})
    return JsonResponse({'data':t}
)

# Load More within Brand
def brand_load_more_data(request):
    offset=int(request.GET['offset'])
    limit=int(request.GET['limit'])
    brand_id = int(request.GET['brand_id'])
    brand = Brand.objects.get(id=brand_id)
    # total_data = Product.objects.filter(category=category).count()
    data = Product.objects.filter(brand=brand).order_by('-id')[offset:offset + limit]
    # data = Product.objects.all().order_by('-id')[offset:offset + limit]
    t=render_to_string('ajax/brand_product_list.html',{'data':data})
    return JsonResponse({'data':t}
)
# Add to cart
def add_to_cart(request):
    # Delete session data at beginning
    # del request.session['cartdata']
    cart_p={}
    cart_p[str(request.GET['id'])]={
        # 'size': request.GET.get('size'),
        # 'color': request.GET.get('color'),
        'image':request.GET.get('image'),
        'title':request.GET.get('title'),
        'qty':request.GET.get('qty'),
        'price':request.GET.get('price'),
    }
    print (cart_p)
    #Check if there is anything in request.sessionm
    if 'cartdata' in request.session:
    # Checking if product exist in request.session, if so,Update product qty with qty added/set by user.
    # If not, add cart_p/current product detail(product chose by user) to request.session via 'cartdata'
        if str(request.GET['id']) in request.session['cartdata']:
            cart_data=request.session['cartdata']
            #Follwing is to replace session qty with user selected current qty,
            # cart_data[str(request.GET['id'])]['qty'] = int(cart_p[str(request.GET['id'])]['qty'])
            # its possible to aggregate qty using increment to session qty with following
            cart_data[str(request.GET['id'])]['qty'] =int(cart_data[str(request.GET['id'])]['qty']) + int(cart_p[str(request.GET['id'])]['qty'])
            #Look at this if you want price to be added based on color/size to cart
            # cart_data[str(request.GET['id'])]['price'] = int(cart_data[str(request.GET['id'])]['price']) + int(
            # 	cart_p[str(request.GET['id'])]['price'])
            cart_data.update(cart_data)
            request.session['cartdata']=cart_data
        else:
            cart_data=request.session['cartdata']
            cart_data.update(cart_p)
            request.session['cartdata']=cart_data
    else:
        request.session['cartdata']=cart_p
    # return JsonResponse({'data':request.session['cartdata']})
    return JsonResponse({'data':request.session['cartdata'],'totalitems':len(request.session['cartdata'])})
    # return JsonResponse({'data':cart_p})





# Cart List Page
def cart_list(request):
    total_amt=0
    if 'cartdata' in request.session:
        for p_id,item in request.session['cartdata'].items():
            total_amt+=int(item['qty'])*float(item['price'])
        return render(request, 'main/cart.html',{'cart_data':request.session['cartdata'],
                                                 'totalitems':len(request.session['cartdata']),
                                                 'total_amt':total_amt
                                                 })
    else:
        return render(request, 'main/cart.html',{'cart_data':'','totalitems':0,'total_amt':0})


# Delete Cart Item
def delete_cart_item(request):
    p_id=str(request.GET['id'])
    if 'cartdata' in request.session:
        if p_id in request.session['cartdata']:
            cart_data=request.session['cartdata']
            del request.session['cartdata'][p_id]
            request.session['cartdata']=cart_data
    total_amt=0
    for p_id,item in request.session['cartdata'].items():
        total_amt+=int(item['qty'])*float(item['price'])
    t=render_to_string('ajax/cart-list.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})
    return JsonResponse({'data':t,'totalitems':len(request.session['cartdata'])})

# Update Cart Item
def update_cart_item(request):
    p_id=str(request.GET['id'])
    p_qty=request.GET['qty']
    if 'cartdata' in request.session:
        if p_id in request.session['cartdata']:
            cart_data=request.session['cartdata']
            cart_data[str(request.GET['id'])]['qty']=p_qty
            request.session['cartdata']=cart_data
    total_amt=0
    for p_id,item in request.session['cartdata'].items():
        total_amt+=int(item['qty'])*float(item['price'])
    t=render_to_string('ajax/cart-list.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})
    return JsonResponse({'data':t,'totalitems':len(request.session['cartdata'])})

# Save Review
def save_review(request,pid):
    product=Product.objects.get(pk=pid)
    user=request.user
    review=ProductReview.objects.create(
		user=user,
		product=product,
		review_text=request.POST['review_text'],
		review_rating=request.POST['review_rating'],
		)
    data={
		'user':user.username,
		'review_text':request.POST['review_text'],
		'review_rating':request.POST['review_rating']
	}
# Fetch avg rating for reviews
    avg_reviews=ProductReview.objects.filter(product=product).aggregate(avg_rating=Avg('review_rating'))
# End
    return JsonResponse({'bool':True,'data':data,'avg_reviews':avg_reviews})



# Checkout
@login_required
def checkout(request):
    total_amt=0
    totalAmt=0
    # Select Order which is not paid for for given user
    order, created = CartOrder.objects.get_or_create(
        user=request.user,
        paid_status=False)

    # Delete all entries from cartorderitems for incomplete order before adding orderitems from session
    if CartOrderItems.objects.filter(order=order).exists():
        orderitem = CartOrderItems.objects.filter(order=order)
        orderitem.delete()
    #End

    if 'cartdata' in request.session:
        #Looping over existing card and adding all cart items price to set order total price
        for p_id,item in request.session['cartdata'].items():
            totalAmt+=int(item['qty'])*float(item['price'])
            total_amt=totalAmt
        #End

        # This will set total amount for order to be existing total in session cart
        order.total_amt=totalAmt
        order.save()

        # OrderItems For all items is session, check if alrady exist in table, if so, update qty to new or add the new record
        #This implementation is to check if order_item exist from before in incomplete order and if so, update the qty and total price
        #This has issue of order items which are there from  before and same is not ordered by user again and this cause stranded record in order items
        # for p_id, item in request.session['cartdata'].items():
        #     if CartOrderItems.objects.filter(item=item['title']).exists():
        #         obj = CartOrderItems.objects.get(item=item['title'])
        #         obj.qty = item['qty']
        #         obj.total = float(item['qty']) * float(item['price'])
        #         obj.save()
        #     else:
        #         items=CartOrderItems.objects.create(
        #             order=order,
        #             invoice_no='INV-'+str(order.id),
        #             item=item['title'],
        #             image=item['image'],
        #             qty=item['qty'],
        #             price=item['price'],
        #             total=float(item['qty'])*float(item['price'])
        #         )
        # End

        #Add to Checkout(table) from session cart to CartOrderItems  table
        for p_id, item in request.session['cartdata'].items():
            items = CartOrderItems.objects.create(
                            order=order,
                            invoice_no='INV-'+str(order.id),
                            item=item['title'],
                            image=item['image'],
                            qty=item['qty'],
                            price=item['price'],
                            total=float(item['qty'])*float(item['price'])
                        )
        #End
        host = request.get_host()

        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': total_amt,
            'item_name': 'OrderNo-' + str(order.id),
            'invoice': 'INV-' + str(order.id),
            'currency_code': 'USD',
            'notify_url': 'http://{}{}'.format(host, reverse('main:paypal-ipn')),
            'return_url': 'http://{}{}'.format(host, reverse('main:payment_done')),
            'cancel_return': 'http://{}{}'.format(host, reverse('main:payment_cancelled')),
        }
        form = PayPalPaymentsForm(initial=paypal_dict)
        checkoutform = CheckoutForm()
        # address=UserAddressBook.objects.filter(user=request.user,status=True).first()
        return render(request, 'main/checkout.html',{'cart_data':request.session['cartdata'],
                                                     'totalitems':len(request.session['cartdata']),
                                                     'total_amt':total_amt,
                                                     'form':form,
                                                     'checkoutform':checkoutform
                                                     # 'address':address
                                                     })


@csrf_exempt
def payment_done(request):
    order = CartOrder.objects.get(user=request.user,paid_status=False)
    order.paid_status=True
    order.save()
    returnData=request.POST
    # Delete session data at beginning
    if 'cartdata' in request.session:
        del request.session['cartdata']
    return render(request, 'main/payment-success.html',{'data':returnData,'order':order})


@csrf_exempt
def payment_canceled(request):
    return render(request, 'main/payment-fail.html')



stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def stripe_config(request):
     if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)

class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        total_amt = 0
        totalAmt = 0
        #Select Order which is not paid for for given user
        order, created = CartOrder.objects.get_or_create(
            user=request.user,
            paid_status=False)

        # Delete all entries from cartorderitems for incomplete order before adding orderitems from session
        if CartOrderItems.objects.filter(order=order).exists():
            orderitem = CartOrderItems.objects.filter(order=order)
            orderitem.delete()
        # End

        if 'cartdata' in request.session:
            # Looping over existing card and adding all cart items price to set order total price
            for p_id, item in request.session['cartdata'].items():
                totalAmt += int(item['qty']) * float(item['price'])
                total_amt = totalAmt
            #End

            #This will set total amount for order to be existing total in session cart
            order.total_amt = totalAmt
            order.save()
            # End

            #Add to Checkout(table) from session cart to CartOrderItems table
            for p_id, item in request.session['cartdata'].items():
                items = CartOrderItems.objects.create(
                    order=order,
                    invoice_no='INV-' + str(order.id),
                    item=item['title'],
                    image=item['image'],
                    qty=item['qty'],
                    price=item['price'],
                    total=float(item['qty']) * float(item['price'])
                )
            # End

        YOUR_DOMAIN = "http://127.0.0.1:8000"  # change in production
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                    {
                        'name': items.invoice_no,
                        'amount': int(total_amt*100),
                        'quantity': 1,
                        'currency': 'usd',
                    },
                ],
                mode='payment',
                success_url=YOUR_DOMAIN + '/success/',
                cancel_url=YOUR_DOMAIN + '/cancel/',
            )
        return redirect(checkout_session.url)

class SuccessView(TemplateView):
    template_name = 'main/success.html'

class CancelledView(TemplateView):
    template_name = 'main/cancel.html'


# Wishlist
def add_wishlist(request):
	pid=request.GET['product']
	product=Product.objects.get(pk=pid)
	data={}
	checkw=Wishlist.objects.filter(product=product,user=request.user).count()
	if checkw > 0:
		data={
			'bool':False
		}
	else:
		wishlist=Wishlist.objects.create(
			product=product,
			user=request.user
		)
		data={
			'bool':True
		}
	return JsonResponse(data)




# # Edit Profile
# def edit_profile(request):
# 	msg=None
# 	if request.method=='POST':
# 		form=ProfileForm(request.POST,instance=request.user)
# 		if form.is_valid():
# 			form.save()
# 			msg='Data has been saved'
# 	form=ProfileForm(instance=request.user)
# 	return render(request, 'user/edit-profile.html',{'form':form,'msg':msg})





#################################Credit Card

# stripe.api_key = settings.STRIPE_SECRET_KEY
#
#
# @csrf_exempt
# def stripe_config(request):
#      if request.method == 'GET':
#         stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
#         return JsonResponse(stripe_config, safe=False)
#
#
# # payments/views.py
#
# @csrf_exempt
# def create_checkout_session(request):
# 	if request.method == 'GET':
# 		total_amt = 0
# 		totalAmt = 0
# 		domain_url = 'http://127.0.0.1:8000/'
# 		stripe.api_key = settings.STRIPE_SECRET_KEY
# 		if 'cartdata' in request.session:
# 			for p_id, item in request.session['cartdata'].items():
# 				totalAmt += int(item['qty']) * float(item['price'])
# 				total_amt = totalAmt
# 			# Order
# 			order, created = CartOrder.objects.get_or_create(user=request.user,paid_status=False)
# 			order.total_amt = totalAmt
# 			order.save()
# 			# OrderItems
# 			items = CartOrderItems.objects.create(
# 				order=order,
# 				invoice_no='INV-' + str(order.id),
# 				item=item['title'],
# 				image=item['image'],
# 				qty=item['qty'],
# 				price=item['price'],
# 				total=float(item['qty']) * float(item['price']))
#
# 		try:
# 			checkout_session = stripe.checkout.Session.create(
#                 success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
#                 cancel_url=domain_url + 'cancelled/',
#                 payment_method_types=['card'],
#                 mode='payment',
#                 line_items=[
#                     {
#                         'name': 'T-shirt',
#                         'quantity': 1,
#                         'currency': 'usd',
#                         'amount': total_amt,
#                     }
# 				]
# 			)
#             return JsonResponse({'sessionId': checkout_session['id']})
# 		except Exception as e:
# 			return JsonResponse({'error': str(e)})
#
# class SuccessView(TemplateView):
# 	template_name = 'main/payment-success.html'
#
# class CancelledView(TemplateView):
#     template_name = 'main/payment-fail.html'

# @csrf_exempt
# def stripe_webhook(request):
#     stripe.api_key = settings.STRIPE_SECRET_KEY
#     endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
#     payload = request.body
#     sig_header = request.META['HTTP_STRIPE_SIGNATURE']
#     event = None
#
#     # Stripe CLI setup + login
#     # The easiest way to test our webhook is to download Stripe CLI (https://stripe.com/docs/stripe-cli)
#     # After downloading it we need to login by running 'stripe login' in Terminal, this command will generate
#     # a pairing code for us an open our web browser.
#     #
#     # ---------------------------------------------------------------
#     # Your pairing code is: word1-word2-word3-word4
#     # This pairing code verifies your authentication with Stripe.
#     # Press Enter to open the browser (^C to quit)
#     # ---------------------------------------------------------------
#     #
#     # By pressing enter CLI opens our browser and asks us if we want to allow Stripe CLI to access our account
#     # information. We can allow it by clicking 'Allow access' button and confirming the action with our password.
#     #
#     # If everything goes well Stripe CLI will display the following message:
#     #
#     # ---------------------------------------------------------------
#     # > Done! The Stripe CLI is configured for {ACCOUNT_NAME} with account id acct_{ACCOUNT_ID}
#     # Please note: this key will expire after 90 days, at which point you'll need to re-authenticate.
#     # ---------------------------------------------------------------
#     #
#     # Webhook setup
#     # Once we successfully logged in we can start listening to Stripe events and forward them to our webhook using
#     # the following command:
#     #
#     # stripe listen --forward-to localhost:8000/webhook/
#     #
#     # This will generate a webhook signing secret that we should save in our settings.py. After that we will
#     # need to pass it when constructing a Webhook event.
#     try:
#         event = stripe.Webhook.construct_event(
#             payload, sig_header, endpoint_secret
#         )
#     except ValueError as e:
#         # Invalid payload
#         return HttpResponse(status=400)
#     except stripe.error.SignatureVerificationError as e:
#         # Invalid signature
#         return HttpResponse(status=400)
#
#     # Handle the checkout.session.completed event
#     if event['type'] == 'checkout.session.completed':
#         session = event['data']['object']
#
#         # This method will be called when user successfully purchases something.
#         handle_checkout_session(session)
#
#     return HttpResponse(status=200)
#
#
# def handle_checkout_session(session):
#     # client_reference_id = user's id
#     client_reference_id = session.get("client_reference_id")
#     payment_intent = session.get("payment_intent")
#
#     if client_reference_id is None:
#         # Customer wasn't logged in when purchasing
#         return
#
#     # Customer was logged in we can now fetch the Django user and make changes to our models
#     try:
#         user = User.objects.get(id=client_reference_id)
#         print(user.username, "just purchased something.")
#
#         # TODO: make changes to our models.
#
#     except User.DoesNotExist:
#         pass



# @csrf_exempt
# def stripe_webhook(request):
#     stripe.api_key = settings.STRIPE_SECRET_KEY
#     endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
#     payload = request.body
#     sig_header = request.META['HTTP_STRIPE_SIGNATURE']
#     event = None
#
#     try:
#         event = stripe.Webhook.construct_event(
#             payload, sig_header, endpoint_secret
#         )
#     except ValueError as e:
#         # Invalid payload
#         return HttpResponse(status=400)
#     except stripe.error.SignatureVerificationError as e:
#         # Invalid signature
#         return HttpResponse(status=400)
#
#     # Handle the checkout.session.completed event
#     if event['type'] == 'checkout.session.completed':
#         print("Payment was successful.")
#         # TODO: run some custom code here
#
#     return HttpResponse(status=200)

