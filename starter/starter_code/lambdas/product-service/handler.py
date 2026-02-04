"""
Product Service Lambda Handler

This Lambda function handles product catalog operations.
It retrieves product data from DynamoDB.
"""

import json
import os
import boto3
from decimal import Decimal

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('PRODUCTS_TABLE', 'shopfast-products')
table = dynamodb.Table(table_name)


class DecimalEncoder(json.JSONEncoder):
    """Handle Decimal types from DynamoDB."""
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)


def lambda_handler(event, context):
    """
    Main Lambda handler for product operations.

    Routes:
    - GET /products - List all products
    - GET /products/{id} - Get single product
    """
    print(f"Received event: {json.dumps(event)}")

    http_method = event.get('httpMethod', '')
    path = event.get('path', '')
    path_parameters = event.get('pathParameters') or {}

    try:
        if http_method == 'GET':
            if path == '/products':
                return get_all_products()
            elif path_parameters.get('id'):
                return get_product(path_parameters['id'])

        return {
            'statusCode': 404,
            'headers': get_cors_headers(),
            'body': json.dumps({'error': 'Not found'})
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': get_cors_headers(),
            'body': json.dumps({'error': 'Internal server error'})
        }


def get_all_products():
    """Retrieve all products from DynamoDB."""
    print("Fetching all products from DynamoDB...")

    # Full table scan - this is slow and will timeout
    response = table.scan()
    products = response.get('Items', [])

    # Handle pagination if there are more items
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        products.extend(response.get('Items', []))

    print(f"Found {len(products)} products")

    return {
        'statusCode': 200,
        'headers': get_cors_headers(),
        'body': json.dumps(products, cls=DecimalEncoder)
    }


def get_product(product_id):
    """Retrieve a single product by ID."""
    print(f"Fetching product: {product_id}")

    response = table.get_item(Key={'id': product_id})
    product = response.get('Item')

    if not product:
        return {
            'statusCode': 404,
            'headers': get_cors_headers(),
            'body': json.dumps({'error': 'Product not found'})
        }

    return {
        'statusCode': 200,
        'headers': get_cors_headers(),
        'body': json.dumps(product, cls=DecimalEncoder)
    }


def get_cors_headers():
    """Return CORS headers for API Gateway responses."""
    return {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }
