#!/bin/bash

# Determine the absolute path of the project's root directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$SCRIPT_DIR/../../"

# Define the log file
LOG_FILE="/tmp/customer_cleanup_log.txt"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

# Python command to find and delete customers with no orders in the last year
PYTHON_CMD="
from django.utils import timezone
from datetime import timedelta
from crm.models import Customer, Order

one_year_ago = timezone.now() - timedelta(days=365)
recent_customer_ids = Order.objects.filter(order_date__gte=one_year_ago).values_list('customer_id', flat=True).distinct()
customers_to_delete = Customer.objects.exclude(id__in=recent_customer_ids)
count = customers_to_delete.count()
if count > 0:
    customers_to_delete.delete()
print(f'{count} inactive customers deleted.')
"

# Execute the Django management command from the project root

DELETED_INFO=$(cd "$PROJECT_ROOT" && python manage.py shell -c "$PYTHON_CMD")

# Log the result
echo "$TIMESTAMP - $DELETED_INFO" >> $LOG_FILE