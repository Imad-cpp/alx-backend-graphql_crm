import django_filters
from .models import Customer, Product, Order

class CustomerFilter(django_filters.FilterSet):
    # Case-insensitive partial match filters
    name = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')
    
    # Date range filter
    created_at = django_filters.DateFromToRangeFilter()
    
    # Custom filter for phone pattern
    phone_starts_with = django_filters.CharFilter(method='filter_phone_starts_with')
    
    # Ordering
    order_by = django_filters.OrderingFilter(
        fields=(
            ('name', 'name'),
            ('email', 'email'),
            ('created_at', 'createdAt'),
        )
    )

    class Meta:
        model = Customer
        fields = ['name', 'email', 'created_at']

    def filter_phone_starts_with(self, queryset, name, value):
        return queryset.filter(phone__startswith=value)


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    
    # Range filters
    price = django_filters.RangeFilter()
    stock = django_filters.RangeFilter()

    # Low stock filter
    low_stock = django_filters.NumberFilter(field_name='stock', lookup_expr='lt')

    order_by = django_filters.OrderingFilter(
        fields=(
            ('name', 'name'),
            ('price', 'price'),
            ('stock', 'stock'),
        )
    )

    class Meta:
        model = Product
        fields = ['name', 'price', 'stock']


class OrderFilter(django_filters.FilterSet):
    total_amount = django_filters.RangeFilter()
    order_date = django_filters.DateFromToRangeFilter()
    
    # Related field lookups
    customer_name = django_filters.CharFilter(field_name='customer__name', lookup_expr='icontains')
    product_name = django_filters.CharFilter(field_name='products__name', lookup_expr='icontains')
    
    # Filter by specific product id
    has_product_id = django_filters.NumberFilter(field_name='products__id', lookup_expr='exact')

    order_by = django_filters.OrderingFilter(
        fields=(
            ('total_amount', 'totalAmount'),
            ('order_date', 'orderDate'),
            ('customer__name', 'customerName'),
        )
    )

    class Meta:
        model = Order
        fields = ['total_amount', 'order_date', 'customer_name', 'product_name']