from django.shortcuts import render, redirect
from django.core.paginator import Paginator

from .forms import CustomerForm

from .models import Customer


# Create your views here.

def index(request):
    order_by = request.GET.get('order_by')
    if order_by == '' or order_by is None:
        order_by = 'id'
    customer_list = Customer.objects.order_by(order_by)
    total = len(customer_list)
    per_page = request.GET.get('per_page')
    try:
        per_page = int(per_page)
    except:
        per_page = 5
    if per_page <= 0:
        per_page = 5
    elif per_page > 20:
        per_page = 20
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
            'total': total
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
    return render(request, 'create_customer.html', {'form': form})


def edit_customer(request, customer_id):
    pass


def delete_customer(request, customer_id):
    if request.method == 'POST' and request.POST.get('HTTP_X_METHOD_OVERRIDE') == "DELETE":
        Customer.objects.get(id=customer_id).delete()
    return redirect('customer_index')
