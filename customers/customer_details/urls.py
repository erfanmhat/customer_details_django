from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='customer_index'),
    path('create', views.create_customer, name='create_customer'),
    path('edit/<int:customer_id>', views.edit_customer, name='edit_customer'),
    path('delete/<int:customer_id>', views.delete_customer, name='delete_customer')
]
