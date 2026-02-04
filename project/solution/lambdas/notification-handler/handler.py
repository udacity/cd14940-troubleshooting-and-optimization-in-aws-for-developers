"""
Notification Handler Lambda - MVP SOLUTION

MVP Requirements Implemented:
1. Structured JSON logging
2. X-Ray tracing enabled
3. Basic EMF metrics (NotificationsSent, NotificationErrors)

NOT included in MVP (see Stretch Goals):
- Correlation ID extraction and propagation
- X-Ray annotations for filtering
- Advanced metrics with multiple dimensions
"""

import json
import os
from datetime import datetime

import boto3

# Initialize SES client for sending emails
ses = boto3.client('ses')


# =============================================================================
# MVP: Structured Logging
# =============================================================================

def log_structured(level: str, message: str, **context):
    """MVP structured logging - outputs JSON format."""
    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "level": level,
        "service": "notification-handler",
        "function": os.environ.get('AWS_LAMBDA_FUNCTION_NAME', 'local'),
        "message": message,
        **context
    }
    print(json.dumps(log_entry))


# =============================================================================
# MVP: EMF Custom Metrics
# =============================================================================

def emit_metric(metric_name: str, value: float, unit: str = "Count"):
    """MVP: Emit CloudWatch metric using EMF."""
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
        "Service": "notification-handler",
        metric_name: value
    }
    print(json.dumps(emf_log))


# =============================================================================
# Lambda Handler
# =============================================================================

def lambda_handler(event, context):
    """
    Process SNS notifications and send emails.

    MVP Implementation:
    - Structured logging
    - X-Ray tracing (via template.yaml)
    - EMF metrics for notifications
    """
    log_structured("INFO", "Notification handler invoked",
                   record_count=len(event.get('Records', [])))

    processed = 0
    errors = 0

    for record in event.get('Records', []):
        try:
            # Parse SNS message
            sns_message = record.get('Sns', {})
            message_body = json.loads(sns_message.get('Message', '{}'))

            log_structured("INFO", "Processing notification",
                          event_type=message_body.get('event_type'),
                          order_id=message_body.get('order_id'))

            # Send notification based on event type
            event_type = message_body.get('event_type', 'unknown')

            if event_type == 'order.created':
                send_order_confirmation(message_body)
            elif event_type == 'order.shipped':
                send_shipping_notification(message_body)
            else:
                log_structured("WARN", "Unknown event type",
                              event_type=event_type)

            processed += 1

        except Exception as e:
            errors += 1
            log_structured("ERROR", "Failed to process notification",
                          error=str(e),
                          error_type=type(e).__name__,
                          record=str(record)[:200])

    # MVP: Emit metrics
    emit_metric("NotificationsSent", processed)
    if errors > 0:
        emit_metric("NotificationErrors", errors)

    log_structured("INFO", "Notification processing complete",
                  processed=processed,
                  errors=errors)

    return {
        'statusCode': 200,
        'body': json.dumps({
            'processed': processed,
            'errors': errors
        })
    }


def send_order_confirmation(message: dict):
    """Send order confirmation email."""
    order_id = message.get('order_id', 'unknown')
    customer_email = message.get('customer_email')

    if not customer_email:
        log_structured("WARN", "No customer email provided",
                      order_id=order_id)
        return

    log_structured("INFO", "Sending order confirmation",
                  order_id=order_id,
                  email=customer_email[:3] + "***")  # Mask email in logs

    # In production, would send actual email via SES
    # For demo, just log the action
    log_structured("INFO", "Order confirmation sent",
                  order_id=order_id)


def send_shipping_notification(message: dict):
    """Send shipping notification email."""
    order_id = message.get('order_id', 'unknown')
    tracking_number = message.get('tracking_number')

    log_structured("INFO", "Sending shipping notification",
                  order_id=order_id,
                  has_tracking=tracking_number is not None)

    # In production, would send actual email via SES
    log_structured("INFO", "Shipping notification sent",
                  order_id=order_id)
