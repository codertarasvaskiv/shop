from django.shortcuts import render
from .forms import ProductForm, CategoryForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import logging
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views import View
from django.views.generic import DetailView
from django.template import RequestContext
from django.shortcuts import render_to_response
from .models import Product, Category, UserProfile
from django.views.generic import ListView, UpdateView, DeleteView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import urllib.request
import lxml.html as lh
import requests
from bs4 import BeautifulSoup



logger_ = logging.getLogger('root')

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
    return HttpResponse('Product was deleted')


class ProductUpdateView(UpdateView):  # update product based on ClassBasedViews
    model = Product
    template_name = 'edit_product.html'
    fields = [x for x in Product().__dict__.keys() if not x.startswith('_')]  # exclude fields i dont need
    for x in range(len(fields)):
        if fields[x].__contains__('_'):
            fields[x] = fields[x][:fields[x].find('_')] # convert category_id to category
    success_url = '../index'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_details.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['related_products'] = Product.objects.filter(category=context['product'].category)
        context['categories'] = Category.objects.all()
        return context


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('index')


class ProductListView(ListView):
    model = Product
    template_name = 'list_view.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def get_queryset(self):
        queryset = super(ProductListView, self).get_queryset()

        if 'category' in self.kwargs:
            cat = Category.objects.filter(name=self.kwargs['category'])
            queryset = queryset.filter(category=cat)

        if 'order_by' not in self.kwargs:
            queryset = queryset.order_by('price')
        else:
            queryset = queryset.order_by(self.kwargs['order_by'])



        return queryset




def general(request):
    context = RequestContext(request)
    categories = Category.objects.all()
    context_dict = {'boldmessage': 'I am a bald message', 'categories': categories}
    return render(request, 'general.html', context_dict, context)


def my_account(request):
    context = RequestContext(request)
    categories = Category.objects.all()
    context_dict = {'categories': categories}
    return render(request, 'my_account.html', context_dict, context)


class ProductGridView(View):

    def get(self, request):
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
        return render(request, 'grid_view.html', context_dict)



def index(request):
    logger_.debug('dedug')
    context = RequestContext(request)
    categories = Category.objects.all()
    context_dict = {'boldmessage': 'I am a bald message', 'categories': categories}
    return render(request, 'index.html', context_dict, context)


@login_required
def about(request):
    string = "app this is about page <br><a href='/app/user_logout'>Logout press hehe</a>  "
    use = UserProfile()
    print(dir(use))
    return HttpResponse(string)

@login_required
def add_product(request):
    context = RequestContext(request)
    createdProduct = False
    categories = Category.objects.all()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            if 'product_logo' in request.FILES:
                form.product_logo = request.FILES['product_logo']
            else:
                print('not in')
            form.save()
            createdProduct = True
            return render(request, 'add_product.html', {'createdProduct': createdProduct, 'categories': categories}, context)
        else:
            print(form.errors)
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form, 'createdProduct': createdProduct, 'categories': categories}, context)


@login_required
def add_category(request):
    context = RequestContext(request)
    createdCategory= False
    categories = Category.objects.all()
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            if 'category_logo' in request.FILES:
                form.product_logo = request.FILES['category_logo']
            else:
                print('not in')
            form.save()
            createdCategory = True
            return render(request, 'add_category.html', {'createdCategory': createdCategory, 'categories': categories}, context)
        else:
            print(form.errors)
    else:
        form = CategoryForm()
    return render(request, 'add_category.html', {'form': form, 'createdCategory': createdCategory, 'categories': categories}, context)


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
    return render(request, 'register.html', {'user_form': user_form, 'profile_form': profile_form,
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
                return render(request, 'my_account.html', {'categories': categories}, context)
            else:
                return render(request, 'register.html', {'categories': categories}, context)
        else:
            print("Invalid login details: {}, {}".format(username, password))
            return render(request, 'register.html', {'categories': categories})
    else:
        return render(request, 'register.html', {'categories': categories}, context)


@login_required
def user_logout(request):
    context = RequestContext(request)
    logout(request)
    return render(request, 'index.html', {}, context)
