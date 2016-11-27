from django.shortcuts import render
from .forms import ProductForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from .models import Product, Category, UserProfile
import django.forms
import json
from django.views.generic import ListView, UpdateView


@login_required
def like(request):
    prod_id = request.GET['like_info']
    product = Product.objects.get(id=prod_id)
    product.like += 1
    product.save()
    return HttpResponse(product.like)

@login_required
def delete_product(request):
    prod_id = request.GET['delete_info']
    product = Product.objects.get(id=prod_id)
    product.delete()
    return HttpResponse()


@login_required
def edit_product(request, edit_info):
    context = RequestContext(request)
    edited_product = False
    if request.method == 'POST':
        instance = Product.objects.get(id=edit_info)
        form = ProductForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            if 'product_logo' in request.FILES:
                form.product_logo = request.FILES['product_logo']
            else:
                print('not in')
            form.save()
            edited_product = True
            return render(request, 'rango/edit_product.html', {'edited_product': edited_product}, context)
        else:
            print(form.errors)
    else:
        product = Product.objects.get(id=edit_info)
        d = product.__dict__
        d['category'] = product.category.id
        d['product-logo'] = '../'+product.product_logo.url
        pform = ProductForm(initial=d)
        return render(request, 'rango/edit_product.html', {'form': pform, 'edited_product': edited_product,
                                                           'product': product}, context)


def test(request):
    context = RequestContext(request)
    product = Product.objects.get(id=12)

    pform = ProductForm(initial=product.__dict__)
    return render(request, 'rango/test.html', {'form': pform}, context)


def general(request):
    context = RequestContext(request)
    categories = Category.objects.all()
    context_dict = {'boldmessage': 'I am a bald message', 'categories': categories}
    return render(request, 'rango/general.html', context_dict, context)


def my_account(request):
    context = RequestContext(request)
    context_dict = dict()
    return render(request, 'rango/my_account.html', context_dict, context)


def show_category(request, category_name):
    context = RequestContext(request)
    context_dict = dict()
    print(category_name)
    context_dict['products_all'] = Product.objects.filter(category='Watches')
    return render(request, 'rango/list_view_category.html', context_dict, context)


def search(request):
    context = RequestContext(request)
    search_info = request.POST['search_info']
    listfilter= Product.objects.filter(name__icontains=search_info).order_by('price', 'name').reverse()
    return render(request, 'rango/search.html', {'products_filter': listfilter}, context)


def list_view(request):
        context = RequestContext(request)
        context_dict = dict()
        context_dict['products_all'] = Product.objects.all().order_by('price', 'name').reverse()
        return render(request, 'rango/list_view.html', context_dict, context)


def grid_view(request):
    context = RequestContext(request)
    l = Product.objects.all().order_by('price')
    context_dict = dict()
    l2 = []
    k1 = 0
    k2 = 1
    for x in l:
        try:
            l2[k1].append(x)
        except IndexError:
            l2.append([x])
        if k2 % 3 == 0:
            k1 += 1
        k2 += 1
    context_dict['products_all'] = l2 # l2 is list of lists  [ [], [], [] ]
    return render(request, 'rango/grid_view.html', context_dict, context)


def index(request):
    context = RequestContext(request)
    categories = Category.objects.all()
    context_dict = {'boldmessage': 'I am a bald message', 'categories': categories}
    return render(request, 'rango/index.html', context_dict, context)


def product_details(request, product_id):
    context = RequestContext(request)
    categories = Category.objects.all()
    product = Product.objects.get(id=product_id)
    context_dict = {'product': product, 'categories': categories}
    return render(request, 'rango/product_details.html', context_dict, context)

@login_required
def about(request):
    string = "rango this is about page <br><a href='/rango/user_logout'>Logout press hehe</a>  "
    use = UserProfile()
    print(dir(use))
    return HttpResponse(string)

@login_required
def add_product(request):
    context = RequestContext(request)
    createdProduct = False
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            if 'product_logo' in request.FILES:
                form.product_logo = request.FILES['product_logo']
            else:
                print('not in')
            form.save()
            createdProduct = True
            return render(request, 'rango/add_product.html', {'createdProduct': createdProduct}, context)
        else:
            print(form.errors)
    else:
        form = ProductForm()
    return render(request, 'rango/add_product.html', {'form': form, 'createdProduct': createdProduct}, context)


def register(request):
    context = RequestContext(request)
    createdUser = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'user_logo' in request.FILES:
                profile.user_logo = request.FILES['user_logo']
                profile.save()
                createdUser = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request, 'rango/register.html', {'user_form': user_form, 'profile_form': profile_form,
                                                   'createdUser': createdUser}, context)


def user_login(request):
    context = RequestContext(request)
    categories = Category.objects.all()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'rango/my_account.html', {'categories': categories}, context)
            else:
                return render(request, 'rango/register.html', {'categories': categories}, context)
        else:
            print("Invalid login details: {}, {}".format(username, password))
            return render(request, 'rango/register.html', {'categories': categories})
    else:
        return render(request, 'rango/register.html', {'categories': categories}, context)


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/rango/index')

