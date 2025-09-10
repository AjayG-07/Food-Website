from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from app1.models import Food,FoodCart
from app1.forms import FoodForm,SignUpForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from django.contrib.admin.views.decorators import staff_member_required




def home_view(request):
   
    food_data = Food.objects.all().order_by('-id')  # Show latest first
    latest_foods = food_data[:4]  # Show latest 4 items separately

    paginator = Paginator(food_data, 4)  # Show 4 items per slide
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'app1/home.html', {
        'page_obj': page_obj,
        'latest_foods': latest_foods
    })


@login_required(login_url='/login/')
def food_view(request):
    form = FoodForm()
    if request.method == 'POST':
        form = FoodForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/list')
   

    return render(request, 'app1/food.html', {'form': form}) 


@login_required(login_url='/login/')
def food_list(request):
    food_data = Food.objects.all()
    return render(request, 'app1/food_list.html', {'food_data': food_data})


def user_food_list(request):
    food_data = Food.objects.all()
    return render(request, 'app1/user_food_list.html', {'food_data': food_data})

@login_required(login_url='/login/')
def food_details(request,id):
    data= get_object_or_404(Food,id=id)

    return render(request  , 'app1/food_details.html',{'data':data})

@login_required(login_url='/login/')
def food_update(request,id):
    data =get_object_or_404(Food, id=id)
    if request.method == "POST":
        form = FoodForm(request.POST,request.FILES, instance=data)
        if form.is_valid():
            form.save()
            return redirect('list')
    else:
        form = FoodForm(instance=data)
    return render(request, 'app1/food_update.html', {'form': form}) 

@login_required(login_url='/login/')
def food_delete(request, id):
    data = get_object_or_404(Food, id=id)
    if request.method == "POST":
        data.delete()
        return redirect('list')
    return render(request, 'app1/food_delete.html', {'data': data})


# this is cart page
@login_required
def food_add_cart(request, id):
    if request.method == "POST":
            quantity = int(request.POST.get('quantity', 1))
 

    # here check cart is empty or not 
            if 'cart' not in request.session or not isinstance(request.session['cart'], dict):
                request.session['cart']={}   # here cart store empty dic

            cart=request.session['cart']  # here fetch data 

            # this is check id prsent or not present then inceremenr otherwise default one
            id = str(id)

            if str(id) in cart:
                cart[id] += quantity
            else:
                cart[id] = quantity


            request.session['cart']=cart      # this is save session
            request.session.modified = True  
            return redirect('food_cart_view')
    return redirect('home')




@login_required
def food_cart_view(request):

    cart= request.session.get('cart',{})
    cart_data=[]
    total_foodprice=0

    for id,quantity in cart.items():
        food=Food.objects.get(id=int(id))
        total_price = food.prize * quantity 
        cart_data.append({'food':food,'quantity':quantity,'total_price': total_price})
        total_foodprice += total_price

    return render(request, 'app1/foodcart.html', {
        'cart_data': cart_data,
        'total_foodprice': total_foodprice
    })




def increase_quantity(request, food_id):
    if 'cart' in request.session:
        cart = request.session['cart']
        if str(food_id) in cart:
            cart[str(food_id)] += 1  # Increase quantity
            request.session['cart'] = cart  # Save session
    return redirect('food_cart_view')

def decrease_quantity(request, food_id):
    if 'cart' in request.session:
        cart = request.session['cart']
        if str(food_id) in cart:
            if cart[str(food_id)] > 1:
                cart[str(food_id)] -= 1  # Decrease quantity
            else:
                del cart[str(food_id)]  # Remove item if quantity is 1
            request.session['cart'] = cart  # Save session
    return redirect('food_cart_view')


@login_required
def food_remove_view(request, id):
    cart= request.session.get('cart',{})

    if str(id) in cart:
            del cart[str(id)]

    request.session['key']=cart
    return redirect('food_cart_view')



@login_required
def food_clear_view(request):
    request.session['cart']={}
    return redirect('food_cart_view')


#  this is authentication page

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user =form.save()
            login(request,user)

            if user.is_staff:
                return redirect('food_dashboard')
            else:
                return redirect('/')
    else:
        form = SignUpForm()

    return render(request, 'setup/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user =form.get_user()
            login(request,user)
            if user.is_staff:
                return redirect('food_dashboard')
            else:
                return redirect('/')
    else:
        form = AuthenticationForm()

    return render(request, 'setup/login.html', {'form': form})


def admin_sign_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user =form.save()
            user.is_staff=True
            user.save()
            login(request,user)

            return redirect('food_dashboard')
                
    else:
        form = SignUpForm()

    return render(request, 'setup/adminsignup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect(reverse('login'))


@staff_member_required(login_url='/login/')
def food_dashboard_view(request):
    
    return render(request,'app1/admin_dashboard.html')
