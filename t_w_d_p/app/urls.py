from django.conf.urls import url
from . import views
from .views import ProductGridView, ProductDetailView, ProductDeleteView, ProductListView

urlpatterns = [
    url(r'^$', views.index, name='start'),
    url(r'^like/$', views.like, name='like'),
    url(r'^index/', views.index, name='index'),
    url(r'^my_account/', views.my_account, name='my_account'),
    url(r'^register/', views.register, name='register'),
    url(r'^user_login/', views.user_login, name='user_login'),
    url(r'^user_logout/', views.user_logout, name='user_logout'),
    url(r'^about/', views.about, name='about'),
    url(r'^add_product/', views.add_product, name='add_product'),
    url(r'^add_category/', views.add_category, name='add_category'),
    # url(r'^delete_product/', views.delete_product, name='delete_product'),
    url(r'^delete_product/', ProductDeleteView.as_view(), name='delete_product'),
    url(r'^edit_product/(?P<pk>[0-9]+)$', views.ProductUpdateView.as_view(), name='edit_product'),
    url(r'^general/', views.general, name='general'),

    url(r'^list_view/$', ProductListView.as_view(), name='list_view'),
    url(r'^list_view/(?P<category>.+)$', ProductListView.as_view(), name='list_view'),

    url(r'^grid_view/', ProductGridView.as_view(), name='grid_view'),
    url(r'^product_details/(?P<pk>[0-9]+)$', ProductDetailView.as_view(), name='product_details'),



]