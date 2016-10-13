from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^index/', views.index, name='index'),
    url(r'^about/', views.about, name='about'),
    url(r'^add_product/', views.add_product, name='add_product'),
    url(r'^general/', views.general, name='general'),
    url(r'^list_view/', views.list_view, name='list_view'),
    url(r'^grid_view/', views.grid_view, name='grid_view'),
    url(r'^product_details/(?P<product_id>[0-9]+)$', views.product_details, name='product_details'),
]