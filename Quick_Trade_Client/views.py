from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, LoginForm
from django.contrib import messages
from django.shortcuts import render
from django.db.models import Q, Count
from django.utils import timezone

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
                # Keep the session only for the browser session unless "Remember me" is selected.
                if request.POST.get('rememberMe'):
                    request.session.set_expiry(1209600)  # 14 days
                else:
                    request.session.set_expiry(0)

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
    product = get_object_or_404(Product, id=product_id, seller=request.user)
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

def product_detail(request, product_id):
    product = get_object_or_404(
        Product.objects.select_related('seller', 'main_category'),
        id=product_id,
    )
    related_products = Product.objects.filter(
        ad_status='Active',
        main_category=product.main_category,
    ).exclude(id=product.id).select_related('seller', 'main_category').order_by('-created_at')[:8]
    seller_listing_count = Product.objects.filter(
        seller=product.seller,
        ad_status='Active',
    ).count()

    context = {
        'prod': [product],
        'related_products': related_products,
        'seller_listing_count': seller_listing_count,
        'categories': main_categories.objects.all(),
    }
    return render(request, 'user/product_detail.html', context)


# def search_product_category(request):
#     return render(request,'user/product_list_by_category.html')
def _listing_page(request, category_id=None):
    categories = main_categories.objects.all()
    form = ProductSearchForm(request.GET or None)
    products = Product.objects.filter(ad_status='Active').select_related('seller', 'main_category')
    selected_conditions = request.GET.getlist('condition')
    price_min = None
    price_max = None
    sort_by = 'newest'
    search_query = ''
    selected_category = None
    category_object = None

    if category_id is not None:
        category_object = get_object_or_404(main_categories, id=category_id)
        products = products.filter(main_category=category_object)
        selected_category = category_object.id

    if form.is_valid():
        category = form.cleaned_data.get('category')
        search_query = (form.cleaned_data.get('search') or '').strip()
        sort_by = form.cleaned_data.get('sort_by') or 'newest'
        price_min = form.cleaned_data.get('price_min')
        price_max = form.cleaned_data.get('price_max')

        if category and category_id is None:
            products = products.filter(main_category=category)
            selected_category = category.id
            category_object = category
        if search_query:
            products = products.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))
        if selected_conditions:
            products = products.filter(condition__in=selected_conditions)
        if price_min is not None:
            products = products.filter(price__gte=price_min)
        if price_max is not None:
            products = products.filter(price__lte=price_max)

    if price_min is not None and price_max is not None and price_min > price_max:
        form.add_error('price_max', 'Maximum price must be greater than or equal to minimum price.')
        products = Product.objects.none()

    if sort_by == 'price_low':
        products = products.order_by('price', '-created_at')
    elif sort_by == 'price_high':
        products = products.order_by('-price', '-created_at')
    else:
        products = products.order_by('-created_at')

    from django.core.paginator import Paginator
    paginator = Paginator(products, 9)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'products': page_obj.object_list,
        'page_obj': page_obj,
        'paginator': paginator,
        'categories': categories,
        'form': form,
        'price_mx': price_max,
        'price_mn': price_min,
        'selected_conditions': selected_conditions,
        'selected_category': selected_category,
        'category_object': category_object,
        'search_query': search_query,
        'sort_by': sort_by,
        'total_results': paginator.count,
    }
    template = 'user/product_list_by_category.html' if category_id is not None else (
        'user/product_list_by_category.html' if category_object else 'user/product_list.html'
    )
    return render(request, template, context)


def product_list(request):
    return _listing_page(request)


def product_list_by_category(request, category_id):
    return _listing_page(request, category_id=category_id)

@login_required(login_url='/login')
def Delete_listing(request, product_id):
    product = get_object_or_404(Product, id=product_id, seller=request.user)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Listing removed successfully.')
    else:
        messages.error(request, 'Please use the listing form to confirm deletion.')
    return redirect('profile')

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