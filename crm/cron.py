import requests
from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from gql.transport.exceptions import TransportQueryError

# --- Constants ---
HEARTBEAT_LOG_FILE = "/tmp/crm_heartbeat_log.txt"
LOW_STOCK_LOG_FILE = "/tmp/low_stock_updates_log.txt"
GRAPHQL_ENDPOINT = "http://localhost:8000/graphql"

# --- Cron Job Functions ---

def log_crm_heartbeat():
    """
    Logs a heartbeat message and checks the GraphQL endpoint's health using the gql library.
    """
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    status = "alive"

    try:
        # 1. Set up the GQL client and transport
        transport = RequestsHTTPTransport(url=GRAPHQL_ENDPOINT, timeout=5)
        client = Client(transport=transport, fetch_schema_from_transport=False)
        
        # 2. Define and execute the simple health-check query
        query = gql("{ hello }")
        client.execute(query)

    except (TransportQueryError, Exception):
        # Catches GraphQL errors, connection errors, timeouts, etc.
        status = "unreachable or unresponsive"

    with open(HEARTBEAT_LOG_FILE, "a") as f:
        f.write(f"{timestamp} CRM is {status}\n")


def update_low_stock():
    """
    Executes the GraphQL mutation to restock low-stock products and logs the result.
    """
    graphql_mutation = """
        mutation {
          updateLowStockProducts {
            message
            updatedProducts {
              name
              stock
            }
          }
        }
    """
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = ""
    
    try:
        response = requests.post(GRAPHQL_ENDPOINT, json={'query': graphql_mutation}, timeout=10)
        response.raise_for_status()
        data = response.json()

        if 'errors' in data:
            log_entry = f"{timestamp} - ERROR: {data['errors']}\n"
        else:
            mutation_data = data['data']['updateLowStockProducts']
            message = mutation_data['message']
            updated_products = mutation_data.get('updatedProducts', [])
            
            log_entry = f"{timestamp} - {message}\n"
            for product in updated_products:
                log_entry += f"  - Product: {product['name']}, New Stock: {product['stock']}\n"

    except requests.RequestException as e:
        log_entry = f"{timestamp} - FAILED to execute mutation: {e}\n"

    with open(LOW_STOCK_LOG_FILE, "a") as f:
        f.write(log_entry)