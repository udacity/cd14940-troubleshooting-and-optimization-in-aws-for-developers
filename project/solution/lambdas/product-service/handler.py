"""
Product Service Lambda Handler - MVP SOLUTION

MVP Requirements Implemented:
1. Structured JSON logging (timestamp, level, service, context)
2. X-Ray tracing enabled
3. Basic EMF custom metrics (ProductViews, Errors)
4. Timeout fix (increased from 3s to 30s)

NOT included in MVP (see Stretch Goals):
- ElastiCache integration
- Correlation ID propagation
- X-Ray annotations and metadata
- Advanced metrics with multiple dimensions
"""

import json
import os
from decimal import Decimal
from datetime import datetime

import boto3

# Initialize AWS clients
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('PRODUCTS_TABLE', 'shopfast-products')
table = dynamodb.Table(table_name)


class DecimalEncoder(json.JSONEncoder):
    """Handle Decimal types from DynamoDB."""
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)


# =============================================================================
# MVP: Structured Logging (Basic)
# =============================================================================

def log_structured(level: str, message: str, **context):
    """
    MVP structured logging - outputs JSON format.

    Includes: timestamp, level, service, message, and context.
    Does NOT include: correlation ID propagation (that's a Stretch Goal)
    """
    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "level": level,
        "service": "product-service",
        "function": os.environ.get('AWS_LAMBDA_FUNCTION_NAME', 'local'),
        "message": message,
        **context
    }
    print(json.dumps(log_entry))


# =============================================================================
# MVP: EMF Custom Metrics (Basic - 2 metrics)
# =============================================================================

def emit_metric(metric_name: str, value: float, unit: str = "Count"):
    """
    MVP: Emit CloudWatch metric using Embedded Metric Format.

    Publishes to ShopFast/Application namespace with Service dimension.
    """
    emf_log = {
        "_aws": {
            "Timestamp": int(datetime.utcnow().timestamp() * 1000),
            "CloudWatchMetrics": [{
                "Namespace": "ShopFast/Application",
                "Dimensions": [["Service"]],
                "Metrics": [{
                    "Name": metric_name,
                    "Unit": unit
                }]
            }]
        },
        "Service": "product-service",
        metric_name: value
    }
    print(json.dumps(emf_log))


# =============================================================================
# Lambda Handler
# =============================================================================

def lambda_handler(event, context):
    """
    Main Lambda handler for product operations.

    MVP Implementation:
    - Structured JSON logging
    - X-Ray tracing (enabled via template.yaml)
    - EMF metrics for ProductViews and Errors
    - Fixed timeout (30s instead of 3s)
    """
    log_structured("INFO", "Request received",
                   path=event.get('path'),
                   method=event.get('httpMethod'))

    http_method = event.get('httpMethod', '')
    path = event.get('path', '')
    path_parameters = event.get('pathParameters') or {}

    try:
        if http_method == 'GET':
            if path == '/products':
                return get_all_products(event)
            elif path_parameters.get('id'):
                return get_product(path_parameters['id'])

        return error_response(404, 'Not found')

    except Exception as e:
        log_structured("ERROR", "Request failed",
                      error=str(e),
                      error_type=type(e).__name__)
        emit_metric("Errors", 1)
        return error_response(500, 'Internal server error')


def get_all_products(event):
    """
    Retrieve products from DynamoDB.

    MVP FIX: Added pagination to prevent timeout.
    (Caching is a Stretch Goal)
    """
    log_structured("INFO", "Fetching products from DynamoDB")

    # MVP: Use pagination instead of full table scan
    query_params = event.get('queryStringParameters') or {}
    limit = min(int(query_params.get('limit', 50)), 100)
    last_key = query_params.get('lastKey')

    scan_kwargs = {'Limit': limit}
    if last_key:
        scan_kwargs['ExclusiveStartKey'] = {'id': last_key}

    response = table.scan(**scan_kwargs)
    products = response.get('Items', [])
    last_evaluated_key = response.get('LastEvaluatedKey')

    log_structured("INFO", "Retrieved products",
                  count=len(products),
                  has_more=last_evaluated_key is not None)

    # MVP: Emit ProductViews metric
    emit_metric("ProductViews", len(products))

    result = {
        'products': products,
        'count': len(products),
        'lastKey': last_evaluated_key.get('id') if last_evaluated_key else None
    }

    return success_response(result)


def get_product(product_id: str):
    """Retrieve a single product by ID."""
    log_structured("INFO", "Fetching product", product_id=product_id)

    response = table.get_item(Key={'id': product_id})
    product = response.get('Item')

    if not product:
        log_structured("WARN", "Product not found", product_id=product_id)
        return error_response(404, 'Product not found')

    # MVP: Emit metric for single product view
    emit_metric("ProductViews", 1)

    return success_response(product)


def success_response(data: dict) -> dict:
    """Return a successful API response."""
    return {
        'statusCode': 200,
        'headers': get_cors_headers(),
        'body': json.dumps(data, cls=DecimalEncoder)
    }


def error_response(status_code: int, message: str) -> dict:
    """Return an error API response."""
    return {
        'statusCode': status_code,
        'headers': get_cors_headers(),
        'body': json.dumps({'error': message})
    }


def get_cors_headers() -> dict:
    """Return CORS headers for API Gateway responses."""
    return {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }
