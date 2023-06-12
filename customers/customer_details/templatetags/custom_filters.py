from django import template
from customer_details.custom_filters import add_class

register = template.Library()

register.filter('add_class', add_class)
