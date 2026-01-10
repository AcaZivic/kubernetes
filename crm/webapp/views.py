from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm, CreateCustomerForm, UpdateCustomerForm
from django.db.models import Q 

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate

from django.contrib.auth.decorators import login_required

from .models import Customer

from django.contrib import messages



# - Homepage 

def home(request):
    if(request.user.is_authenticated):
        return dashboard(request)
    else:
        return render(request, 'webapp/index.html')


# - Register a user

def register(request):

    form = CreateUserForm()

    if request.method == "POST":

        form = CreateUserForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(request, "Account created successfully!")

            return redirect("my-login")

    context = {'form':form}

    return render(request, 'webapp/register.html', context=context)


# - Login a user

def my_login(request):

    form = LoginForm()

    if request.method == "POST":

        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:

                auth.login(request, user)

                return redirect("dashboard")

    context = {'form':form}

    return render(request, 'webapp/my-login.html', context=context)


# - Dashboard

@login_required(login_url='my-login')
def dashboard(request):

    # my_customers = Customer.objects.all()

    # context = {'customers': my_customers}

    # return render(request, 'webapp/dashboard.html', context=context)
    search_query = request.GET.get('q')

    if search_query:
        # Ako postoji upit za pretragu, filtriramo kupce.
        # Q objekti nam omogućavaju da koristimo logičko "ILI" (OR) u upitu.
        # __icontains traži podstring bez obzira na velika/mala slova.
        customers = Customer.objects.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(city__icontains=search_query) |
            Q(country__icontains=search_query) |
            Q(postal_code__icontains=search_query)
        )
    else:
        # Ako nema upita za pretragu, prikaži sve kupce.
        customers = Customer.objects.all()

    # Prosleđujemo listu kupaca i upit za pretragu u templejt
    context = {
        'customers': customers,
        'search_query': search_query,
    }

    return render(request, 'webapp/dashboard.html', context)


# - Create a customer 

@login_required(login_url='my-login')
def create_customer(request):

    form = CreateCustomerForm()

    if request.method == "POST":

        form = CreateCustomerForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(request, "Your customer was created!")

            return redirect("dashboard")

    context = {'form': form}

    return render(request, 'webapp/create-customer.html', context=context)


# - Update a customer 

@login_required(login_url='my-login')
def update_customer(request, pk):

    customer = Customer.objects.get(id=pk)

    form = UpdateCustomerForm(instance=customer)

    if request.method == 'POST':

        form = UpdateCustomerForm(request.POST, instance=customer)

        if form.is_valid():

            form.save()

            messages.success(request, "Your customer was updated!")

            return redirect("dashboard")
        
    context = {'form':form}

    return render(request, 'webapp/update-customer.html', context=context)


# - Read / View a singular customer

@login_required(login_url='my-login')
def singular_customer(request, pk):

    all_customers = Customer.objects.get(id=pk)

    context = {'customer':all_customers}

    return render(request, 'webapp/view-customer.html', context=context)


# - Delete a customer

@login_required(login_url='my-login')
def delete_customer(request, pk):

    customer = Customer.objects.get(id=pk)

    customer.delete()

    messages.success(request, "Your customer was deleted!")

    return redirect("dashboard")



# - User logout

def user_logout(request):

    auth.logout(request)

    messages.success(request, "Logout success!")

    return redirect("my-login")





