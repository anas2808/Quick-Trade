from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, LoginForm
from django.contrib import messages
from django.shortcuts import render
from django.db.models import Q, Count

from .models import *
from .forms import *
# Create your views here.

def listing_expiry_time():
    product=Product.objects.all()
    for i in product:  
        if i.expiry_date <= timezone.now():
            i.ad_status = 'Expired'
            i.save()
        else:
            pass
            

listing_expiry_time()
    
    
    

def index(request):
    listing_expiry_time()
    category = main_categories.objects.all()
    product=Product.objects.filter(ad_status='Active')
    context={
        'categories':category,
        'product':product,
    }
    return render(request,'user/index.html',context)


def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST or None,request.FILES or None)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Registration successful.")
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


@login_required(login_url="/login")
def edit_profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')  # Replace 'profile' with your actual profile page URL name
    else:
        form = EditProfileForm(instance=user)
    return render(request, 'user/edit_profile.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                if user.is_admin:
                    return redirect('admin_dash')
                else:
                    return redirect('/')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


@login_required(login_url="/login") 
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url="/login") 
def profile(request):
    product=Product.objects.filter(seller=request.user).order_by('-created_at')
    # Count unread messages
    unread_count = Message.objects.filter(receiver=request.user, is_read=False).count()
    context={
        'product':product,
        'unread_count':unread_count,
        }
    return render(request,'user/profile.html',context)


@login_required(login_url="/login") 
def sell(request):
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            # Create product but don't save to database yet
            product = form.save(commit=False)
            product.seller = request.user
            product.created_at = timezone.now()
            
            
            product.save()
            messages.success(request, 'Your product has been listed successfully!')
            return redirect('product_detail', product_id=product.id)
    else:
        form = ProductForm()
    
    context = {
        'form': form,
        'categories': main_categories.objects.all(),
    }
    
    return render(request, 'user/sell.html', context)

@login_required(login_url="/login") 
def Update_product(request,product_id):
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES, instance=product)
        if form.is_valid():
            # Create product but don't save to database yet
            product1 = form.save() 
            product1.save()
            messages.success(request, 'Your product has been listed successfully!')
            return redirect('product_detail', product_id)
    else:
        form = ProductForm( instance=product)
    
    context = {
        'form': form,
        'categories': main_categories.objects.all(),
    }
    
    return render(request,'user/update_product.html', context)

def product_detail(request,product_id):
    product = Product.objects.filter(id=product_id)
    context={
        'prod': product,        
        }
    return render(request, 'user/product_detail.html', context)


# def search_product_category(request):
#     return render(request,'user/product_list_by_category.html')
def product_list(request):
    categories = main_categories.objects.all()

    form = ProductSearchForm(request.GET)
    
    # Base query
    products = Product.objects.filter(ad_status='Active').order_by('-created_at')
    selected_conditions = request.GET.getlist('condition')
    # Apply filters if form is valid
    if form.is_valid():
        # Filter by category
        if form.cleaned_data.get('category'):
            products = Product.objects.filter(ad_status='Active',main_category=form.cleaned_data['category'])
        
        # Filter by search term
        if form.cleaned_data.get('search'):
            search_query = form.cleaned_data['search']
            products = products.filter(
                Q(name__icontains=search_query) | 
                Q(description__icontains=search_query)
            )
        
      
        if selected_conditions:
            products = Product.objects.filter(ad_status='Active',condition__in=selected_conditions)
        
        sort_by = form.cleaned_data.get('sort_by')
        if sort_by == 'price_low':
            products = products.order_by('price')
        elif sort_by == 'price_high':
            products = products.order_by('-price')
            
        price_min=form.cleaned_data['price_min']
        price_max=form.cleaned_data['price_max']
        # Price range filtering
        if form.cleaned_data.get('price_min'):
            products = Product.objectsfilter(ad_status='Active',price__gte=price_min)
        
        if form.cleaned_data.get('price_max'):
            products = Product.objects.filter(ad_status='Active',price__lte=price_max)
    context = {
        'products': products,
        'categories': categories,
        'form': form,
        'price_mx':price_max,
        'price_mn':price_min,
        'selected_conditions': selected_conditions,
        'selected_category': form.cleaned_data.get('category').id if form.is_valid() and form.cleaned_data.get('category') else None,
        'search_query': form.cleaned_data.get('search') if form.is_valid() else '',
        'sort_by': form.cleaned_data.get('sort_by') if form.is_valid() and form.cleaned_data.get('sort_by') else 'newest'
    }
    return render(request, 'user/product_list.html', context)

def Delete_listing(request,product_id):
    product=Product.objects.get(id=product_id)
    product.delete()
    messages.warning(request,'Listing Removed succesfully')
    return redirect('/profile/')

def user_listing(request,username):
    user = get_object_or_404(CustomUser, username=username)
    products = Product.objects.filter(ad_status='Active',seller=user).order_by('-created_at')
    
    context = {
        'profile_user': user,
        'products': products
    }
    return render(request,'user/user_listing.html',context)

@login_required
def send_message(request, receiver_id, product_id=None):
    receiver = get_object_or_404(CustomUser, email=receiver_id)
    product = get_object_or_404(Product, id=product_id) if product_id else None
    
    if receiver == request.user:
        messages.error(request, "You cannot send messages to yourself.")
        return redirect('index')
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = receiver
            message.product = product
            message.created_at = timezone.now()
            message.save()
            
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('message_list')
    else:
        initial_data = {}
        if product:
            initial_data['subject'] = f"Inquiry about: {product.name}"
        form = MessageForm(initial=initial_data)
    
    context = {
        'form': form,
        'receiver': receiver,
        'product': product
    }
    
    return render(request, 'user/send_message.html', context)


@login_required
def message_detail(request, message_id):
    """View for showing details of a specific message."""
    message = get_object_or_404(Message, id=message_id)
    
    if request.user != message.sender and request.user != message.receiver:
        messages.error(request, "You don't have permission to view this message.")
        return redirect('message_list')
    
    if request.user == message.receiver and not message.is_read:
        message.is_read = True
        message.save()
    
    context = {
        'message': message
    }
    
    return render(request, 'user/message_detail.html', context)


@login_required
def message_list(request):
    received_messages = Message.objects.filter(receiver=request.user).order_by('-created_at')
    sent_messages = Message.objects.filter(sender=request.user).order_by('-created_at')
    
    context = {
        'received_messages': received_messages,
        'sent_messages': sent_messages
    }
    
    return render(request, 'user/message_list.html', context)