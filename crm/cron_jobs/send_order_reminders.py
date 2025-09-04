import os
import sys
from datetime import datetime, timedelta, timezone
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# Add the project root to the Python path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(PROJECT_ROOT))

LOG_FILE = "/tmp/order_reminders_log.txt"
GRAPHQL_ENDPOINT = "http://localhost:8000/graphql"

def send_reminders():
    """
    Fetches recent orders via GraphQL and logs reminders.
    """
    transport = RequestsHTTPTransport(url=GRAPHQL_ENDPOINT)
    client = Client(transport=transport, fetch_schema_from_transport=False)

    seven_days_ago = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()

    query = gql("""
        query GetRecentOrders($date: DateTime!) {
          allOrders(orderDate_Gte: $date) {
            id
            customer {
              email
            }
          }
        }
    """)

    try:
        result = client.execute(query, variable_values={"date": seven_days_ago})
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(LOG_FILE, "a") as f:
            if result.get("allOrders"):
                for order in result["allOrders"]:
                    order_id = order.get("id")
                    customer_email = order.get("customer", {}).get("email")
                    log_entry = f"{timestamp} - Reminder for Order ID: {order_id}, Customer: {customer_email}\n"
                    f.write(log_entry)
            else:
                f.write(f"{timestamp} - No recent orders found.\n")

        print("Order reminders processed!")

    except Exception as e:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, "a") as f:
            f.write(f"{timestamp} - ERROR: {e}\n")
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    send_reminders()