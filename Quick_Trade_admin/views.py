from django.shortcuts import get_object_or_404, render,redirect
from Quick_Trade_admin.views import *
from Quick_Trade_Client.views import *
from Quick_Trade_admin.models import *
from Quick_Trade_Client.models import *
from Quick_Trade_admin.forms import *
from Quick_Trade_Client.forms import *
from django.contrib.auth.decorators import login_required ,permission_required,user_passes_test
from django import template

def admin(user):
    return user.is_admin  


def admin_login(request):
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
                    messages.warning("you are not admin")
                    return redirect('/logout/')
    else:
        form = LoginForm()
        
        context={
            'form':form
        }
    return render(request,'admin/login.html',context)
  
# Create your views here.
@login_required(login_url="/login")    
@user_passes_test(admin,login_url="/")
def admin_dash(request):
    return render(request,'admin/index.html')

@login_required(login_url="/login")
@user_passes_test(admin,login_url="/")
def edit_profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = EditProfile(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('admin_dash')  
    else:
        form = EditProfileForm(instance=user)
    return render(request, 'admin/admin_profile_edit.html', {'form': form})



@login_required(login_url="/login")    
@user_passes_test(admin,login_url="/login/")
def category_list(request):
    categories = main_categories.objects.all()
    return render(request,'admin/categories/categories_list.html',{'categories':categories})



@login_required(login_url="/login")    
@user_passes_test(admin,login_url="/login/")
def create_category(request):
    form = Categories(request.POST or None,request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('/admin/categories_list/')

    context={'Title':'Create Category Form',
             'form':form,
             }
    return render(request,'admin/categories/form.html',context)



@login_required(login_url="/login")    
@user_passes_test(admin,login_url="/login/")
def update_category(request,pk):
    category=main_categories.objects.get(id=pk)
    form = Categories(request.POST or None,request.FILES or None,instance=category)
    if form.is_valid():
            form.save()
            print("success")
            return redirect('/admin/categories_list/')
    context={'Title':'Update Category Form',
             'form':form,
             }
    return render(request,'admin/categories/form.html',context)



@login_required(login_url="/login")    
@user_passes_test(admin,login_url="/login/")
def delete_category(request,pk):
    category=main_categories.objects.get(id=pk)
    category.delete()
    print("deleted")
    return redirect('/admin/categories_list/')

        
# #sub Category
# def Sub_category_list(request):
#     Sub_categories = sub_categories.objects.all()
#     return render(request,'admin/categories/sub_categories_list.html',{'sub_categories':Sub_categories})

# def create_Sub_category(request):
#     form = Sub_Categories(request.POST or None,request.FILES or None)
#     if form.is_valid():
#         form.save()
#         return redirect('/quick_trade_admin/sub_categories_list/')

#     context={'Title':'Create Sub_Category Form',
#              'form':form,
#              }
#     return render(request,'admin/categories/form.html',context)

# def update_Sub_category(request,pk):
#     Sub_category=sub_categories.objects.get(id=pk)
#     form = Sub_Categories(request.POST or None,request.FILES or None,instance=Sub_category)
#     if form.is_valid():
#             form.save()
#             print("success")
#             return redirect('/quick_trade_admin/sub_categories_list/')
#     context={'Title':'Update Sub_Category Form',
#              'form':form,
#              }
#     return render(request,'admin/categories/form.html',context)

# def delete_Sub_category(request,pk):
#     category=sub_categories.objects.get(id=pk)
#     category.delete()
#     print("deleted")
#     return redirect('/quick_trade_admin/sub_categories_list/')



@login_required(login_url="/login")    
@user_passes_test(admin,login_url="/login/")
def user_list(request):
    user_list=CustomUser.objects.filter(is_admin=0)
    return render(request,'admin/user_list.html',{'user':user_list})



@login_required(login_url="/login")    
@user_passes_test(admin,login_url="/login/")
def listings(request):
    product=Product.objects.all()
    context = {
        'product':product,
        'status_choices': Product.Ad_Status_Choice
    }
    return render(request,'admin/listings.html',context)



@login_required(login_url="/login")    
@user_passes_test(admin,login_url="/login/")
def update_ad_status(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    new_status = request.POST.get('ad_status')
    if new_status in dict(Product.Ad_Status_Choice):
        product.ad_status = new_status
        product.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))
