import requests
from celery import shared_task
from datetime import datetime

LOG_FILE = "/tmp/crm_report_log.txt"
GRAPHQL_ENDPOINT = "http://localhost:8000/graphql"

@shared_task
def generate_crm_report():
    """
    Generates a CRM report by making a GraphQL query and logs it to a file.
    """
    timestamp = datetime.now().strftime("%Y-m-%d %H:%M:%S")
    
    graphql_query = "{ totalCustomerCount totalOrderCount totalRevenue }"
    
    try:
        response = requests.post(GRAPHQL_ENDPOINT, json={'query': graphql_query})
        response.raise_for_status() 
        
        data = response.json()['data']
        customer_count = data.get('totalCustomerCount', 0)
        order_count = data.get('totalOrderCount', 0)
        total_revenue = data.get('totalRevenue', 0)

        log_entry = (
            f"{timestamp} - Report: {customer_count} customers, "
            f"{order_count} orders, {total_revenue} revenue.\n"
        )
    except Exception as e:
        log_entry = f"{timestamp} - FAILED to generate report: {e}\n"

    with open(LOG_FILE, "a") as f:
        f.write(log_entry)

