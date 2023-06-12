from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q

from .forms import CustomerForm

from .models import Customer


# Create your views here.

def index(request):
    search_query = request.GET.get('q')
    order_by = request.GET.get('order_by')
    if order_by == '' or order_by is None:
        order_by = 'id'
    if search_query:
        customer_list = Customer.objects.filter(
            Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query) |
            Q(address__icontains=search_query) | Q(city__icontains=search_query) |
            Q(country__icontains=search_query) | Q(email__icontains=search_query)
        ).order_by(order_by)
    else:
        customer_list = Customer.objects.order_by(order_by)
    total = len(customer_list)
    per_page = request.GET.get('per_page')
    try:
        per_page = int(per_page)
    except:
        per_page = 5
    if per_page <= 0:
        per_page = 5
    elif per_page > 100:
        per_page = 100
    if per_page > total:
        per_page = total
    paginator = Paginator(customer_list, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        'index.html',
        {
            'page_obj': page_obj,
            'per_page': per_page,
            'total': total,
            'per_pages': ["2", "5", "10", "20", "50", "100"]
        }
    )


def create_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_index')
    else:
        form = CustomerForm()
    return render(
        request,
        'create_or_edit_customer.html',
        {
            'form': form,
            'page_type': 'create'
        }
    )


def edit_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_index')
    else:
        form = CustomerForm(instance=customer)
    return render(
        request,
        'create_or_edit_customer.html',
        {
            'form': form,
            'page_type': 'edit'
        }
    )


def delete_customer(request, customer_id):
    if request.method == 'POST' and request.POST.get('HTTP_X_METHOD_OVERRIDE') == "DELETE":
        get_object_or_404(Customer, id=customer_id).delete()
    return redirect('customer_index')
