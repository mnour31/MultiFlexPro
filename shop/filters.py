import django_filters
from .models import Order , Product , Shop , Categorie
class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = [
            'shipping',
            'delivery',
            'throwback',
        ]

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = [
            'title',
            'price',
            'digital',
            'created_date',
        ]