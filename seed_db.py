import os
import django
import random
from datetime import timedelta
from django.utils import timezone

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_graphql_crm.settings')
django.setup()

from crm.models import Customer, Product, Order

def seed_data():
    print("Deleting old data...")
    Customer.objects.all().delete()
    Product.objects.all().delete()
    Order.objects.all().delete()

    print("Creating new data...")
    # Create Customers
    customers = [
        Customer.objects.create(name='Alice Johnson', email='alice@example.com', phone='+15551234567'),
        Customer.objects.create(name='Bob Smith', email='bob@example.com', phone='123-456-7890'),
        Customer.objects.create(name='Charlie Brown', email='charlie@example.com'),
    ]

    # Create Products
    products = [
        Product.objects.create(name='Laptop Pro', price=1200.00, stock=15),
        Product.objects.create(name='Wireless Mouse', price=25.50, stock=50),
        Product.objects.create(name='Mechanical Keyboard', price=75.99, stock=30),
        Product.objects.create(name='4K Monitor', price=450.00, stock=8),
    ]

    # Create Orders
    for customer in customers:
        num_orders = random.randint(1, 3)
        for _ in range(num_orders):
            order_products = random.sample(products, k=random.randint(1, len(products)))
            total = sum(p.price for p in order_products)
            order = Order.objects.create(
                customer=customer,
                total_amount=total,
                order_date=timezone.now() - timedelta(days=random.randint(0, 90))
            )
            order.products.set(order_products)
    
    print("Database has been seeded successfully! ")

if __name__ == '__main__':
    seed_data()