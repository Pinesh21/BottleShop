from django.db.models.functions import ExtractMonth
from django.http import JsonResponse,HttpResponse
from django.shortcuts import render, redirect
from .forms import SignupForm,AddressBookForm
from main.models import Product,CartOrder,CartOrderItems,Wishlist,ProductReview,UserAddressBook
from django.contrib import messages
from django.db.models import Max,Min,Count,Avg
from django.db.models.functions import ExtractMonth
# Create your views here.


def signup(request):
    """
    This function is for Form as instance of UserCreationForm with default
    list of fileds
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            mobile = form.cleaned_data.get('mobile')
            address = form.cleaned_data.get('address')
            form.save()
            messages.success(request, f'Account created successfully! Please Log-In')
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'userapp/signup.html', {'form': form})

# User Dashboard
import calendar
def my_dashboard(request):
	orders=CartOrder.objects.annotate(month=ExtractMonth('order_dt')).values('month').annotate(count=Count('id')).values('month','count')
	monthNumber=[]
	totalOrders=[]
	for d in orders:
		monthNumber.append(calendar.month_name[d['month']])
		totalOrders.append(d['count'])
	return render(request, 'userapp/dashboard.html',{'monthNumber':monthNumber,'totalOrders':totalOrders})

# My Orders
def my_orders(request):
	orders=CartOrder.objects.filter(user=request.user).order_by('-id')
	return render(request, 'userapp/orders.html',{'orders':orders})

# Order Detail
def my_order_items(request,id):
	order=CartOrder.objects.get(pk=id)
	orderitems=CartOrderItems.objects.filter(order=order).order_by('-id')
	return render(request, 'userapp/order-items.html',{'orderitems':orderitems})

# My Wishlist
def my_wishlist(request):
	wlist=Wishlist.objects.filter(user=request.user).order_by('-id')
	return render(request, 'userapp/wishlist.html',{'wlist':wlist})

# My Wishlist
def delete_from_wishlist(request,pid):
	product = Product.objects.get(pk=pid)
	wlist_del=Wishlist.objects.filter(user=request.user,product=product)
	wlist_del.delete()
	wlist = Wishlist.objects.filter(user=request.user).order_by('-id')
	return render(request, 'userapp/wishlist.html',{'wlist':wlist})

# My Reviews
def my_reviews(request):
	reviews=ProductReview.objects.filter(user=request.user).order_by('-id')
	return render(request, 'userapp/reviews.html',{'reviews':reviews})

# My AddressBook
def my_addressbook(request):
	msg = None
	addbook=UserAddressBook.objects.filter(user=request.user).order_by('-id')
	return render(request, 'userapp/addressbook.html',{'addbook':addbook})

# Save addressbook
def save_address(request):
	msg=None
	addbook = UserAddressBook.objects.filter(user=request.user).order_by('-id')
	form = AddressBookForm(request.POST or None)
	#Conditional statement to check if form is submitted with POST request, i.e. submit is clicked
	if request.method=='POST':
		form=AddressBookForm(request.POST)
		if form.is_valid():
			saveForm=form.save(commit=False)
			saveForm.user=request.user
			if 'status' in request.POST:
				UserAddressBook.objects.update(status=False)
			saveForm.save()
			msg='Data has been saved'
			# This is to take user to addresbook page after new address is added successfully
			return render(request, 'userapp/addressbook.html', {'addbook': addbook, 'msg': msg})
	#Else is activated when '+' is clicked, i.e. no POST request is made
	else:
		#This is to stay on add address page id form is not valid, i.e. some validation is not passed
		form = AddressBookForm()
		return render(request, 'userapp/add-address.html', {'form': form, 'msg': msg})

def update_address(request,id):
	address=UserAddressBook.objects.get(pk=id)
	addbook = UserAddressBook.objects.filter(user=request.user).order_by('-id')
	form = AddressBookForm(request.POST, instance=address)
	msg=None
	# Conditional statement to check if form is submitted with POST request, i.e. submit is clicked
	if request.method == 'POST':
		form = AddressBookForm(request.POST,instance=address)
		if form.is_valid():
			saveForm = form.save(commit=False)
			saveForm.user = request.user
			if 'status' in request.POST:
				UserAddressBook.objects.update(status=False)
			saveForm.save()
			msg = 'Data has been saved'
			# This is to take user to addresbook page after address is updated successfully
			return render(request, 'userapp/addressbook.html', {'addbook': addbook, 'msg': msg})
	# Else is activated when 'update' is clicked, i.e. no POST request is made
	else:
		# This is to stay on update address page if form is not valid, i.e. some validation is not passed
		form = AddressBookForm(instance=address)
		return render(request, 'userapp/update-address.html', {'form': form, 'msg': msg})

# Activate address
def activate_address(request):
	a_id=str(request.GET['id'])
	UserAddressBook.objects.update(status=False)
	UserAddressBook.objects.filter(id=a_id).update(status=True)
	return JsonResponse({'bool':True})

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
