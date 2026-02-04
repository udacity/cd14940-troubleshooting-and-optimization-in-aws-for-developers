# Fixes Explained

This document explains each issue in the starter code and the corresponding fix in the solution code.

---

## Issue 1: Lambda Timeout (Product Service)

### Symptom
- Product listing requests return 504 Gateway Timeout
- CloudWatch Logs show "Task timed out after 3.00 seconds"

### Root Cause
The Lambda function timeout was set to 3 seconds, but the DynamoDB scan operation on large tables takes 4-5 seconds.

### Diagnosis Steps
1. Check CloudWatch Logs for the Lambda function
2. Look for "Task timed out" messages
3. Review the Lambda configuration in AWS Console
4. Compare timeout value with actual execution duration

### Fix
**File:** `lambdas/product-service/template.yaml`

```yaml
# Before (starter code)
Timeout: 3

# After (solution code)
Timeout: 30
```

**Additional improvements:**
- Added ElastiCache caching to reduce DynamoDB calls
- Implemented pagination instead of full table scan
- Added X-Ray tracing to identify slow operations

---

## Issue 2: ECS Out of Memory (Order Service)

### Symptom
- Order service pods restart frequently
- ECS task stops with exit code 137 (OOM killed)
- Orders intermittently fail during high load

### Root Cause
The ECS task definition allocated only 256MB memory, but the order processing requires 512MB under load.

### Diagnosis Steps
1. Check ECS task stopped reason in AWS Console
2. Review CloudWatch Container Insights memory metrics
3. Check for exit code 137 in task history
4. Monitor memory utilization over time

### Fix
**File:** `bootstrap_scripts/templates/compute-ecs.yaml`

```yaml
# Before (starter code)
Memory: 256

# After (solution code)
Memory: 512
```

**Additional improvements:**
- Added memory utilization alarms
- Implemented auto-scaling based on memory pressure
- Added structured logging to track resource usage

---

## Issue 3: EKS CrashLoopBackOff (Inventory Service)

### Symptom
- Pod status shows CrashLoopBackOff
- `kubectl logs` shows "DATABASE_URL environment variable is not set"
- Inventory checks fail with 503 errors

### Root Cause
The Kubernetes deployment manifest was missing the DATABASE_URL environment variable required to connect to RDS Aurora.

### Diagnosis Steps
1. Run `kubectl get pods` to see pod status
2. Run `kubectl describe pod <pod-name>` for events
3. Run `kubectl logs <pod-name>` to see error message
4. Check deployment manifest for missing environment variables

### Fix
**File:** `eks/inventory-service/k8s/deployment.yaml`

```yaml
# Before (starter code - missing)
# DATABASE_URL was commented out

# After (solution code)
env:
  - name: DATABASE_URL
    valueFrom:
      secretKeyRef:
        name: inventory-secrets
        key: database_url
```

**Additional improvements:**
- Added Kubernetes Secret for secure credential storage
- Implemented proper readiness probes
- Added startup probe for slow database connections

---

## Issue 4: SNS Filter Failure (Notification Handler)

### Symptom
- Notification Lambda never invokes
- Orders are placed but no confirmation emails sent
- SNS topic has messages but subscription shows low delivery count

### Root Cause
The order-service publishes SNS messages without the `eventType` message attribute. The notification-handler subscription has a filter policy that requires this attribute.

### Diagnosis Steps
1. Check SNS topic metrics for publish count
2. Check Lambda invocation metrics (should be 0)
3. Review subscription filter policy
4. Inspect message attributes being published

### Fix
**File:** `ecs/order-service/src/order_service/services/order_service.py`

```python
# Before (starter code)
self.sns.publish(
    TopicArn=settings.sns_topic_arn,
    Message=json.dumps(event_detail),
    # Missing MessageAttributes
)

# After (solution code)
self.sns.publish(
    TopicArn=settings.sns_topic_arn,
    Message=json.dumps(event_detail),
    MessageAttributes={
        'eventType': {
            'DataType': 'String',
            'StringValue': 'order.created'
        }
    }
)
```

---

## Issue 5: EventBridge Pattern Mismatch

### Symptom
- Step Functions workflow never starts
- EventBridge rule shows 0 invocations
- Orders created but workflow not triggered

### Root Cause
The order-service publishes events with detail-type "order.created", but the EventBridge rule is configured to match "OrderEvent".

### Diagnosis Steps
1. Check EventBridge rule metrics in CloudWatch
2. Review the rule's event pattern
3. Use CloudWatch Logs Insights to search for matching events
4. Compare event pattern with actual published events

### Fix
**File:** `ecs/order-service/src/order_service/services/order_service.py`

```python
# Before (starter code)
'DetailType': 'order.created',

# After (solution code)
'DetailType': 'OrderEvent',
```

**Alternative fix (in CloudFormation):**
```yaml
# Update the rule pattern to match
EventPattern:
  source:
    - shopfast.order-service
  detail-type:
    - order.created  # Changed from OrderEvent
```

---

## Issue 6: Step Functions Wait State

### Symptom
- Order workflow gets stuck
- Step Functions shows execution waiting indefinitely
- Order status never progresses past "processing"

### Root Cause
The Wait state was misconfigured with an incorrect timestamp format or missing timeout.

### Diagnosis Steps
1. View Step Functions execution in AWS Console
2. Check which state the execution is stuck on
3. Review state machine definition
4. Check wait state configuration

### Fix
**File:** `bootstrap_scripts/templates/stepfunctions.yaml`

```yaml
# Before (starter code)
WaitForShipping:
  Type: Wait
  Timestamp: "2099-01-01T00:00:00Z"  # Far future date

# After (solution code)
WaitForShipping:
  Type: Wait
  Seconds: 30  # Wait 30 seconds then continue
```

---

## Observability Best Practices Applied

### X-Ray Tracing

All services now include X-Ray SDK:
- Lambda: Tracing enabled via SAM template (`Tracing: Active`)
- ECS: X-Ray daemon sidecar container
- EKS: X-Ray daemon DaemonSet

### Structured Logging

Using AWS Lambda Powertools for Python:
```python
from aws_lambda_powertools import Logger

logger = Logger(service="product-service")

@logger.inject_lambda_context(correlation_id_path="headers.x-correlation-id")
def handler(event, context):
    logger.info("Processing request", extra={"product_id": "123"})
```

### EMF Metrics

Custom metrics with dimensions:
```python
from aws_lambda_powertools import Metrics

metrics = Metrics(namespace="ShopFast", service="order-service")

@metrics.log_metrics(capture_cold_start_metric=True)
def handler(event, context):
    metrics.add_metric(name="OrdersCreated", unit="Count", value=1)
    metrics.add_dimension(name="Environment", value="production")
```

### CloudWatch Alarms

Key alarms configured:
- Lambda error rate > 5%
- Lambda duration threshold (approaching timeout)
- ECS memory utilization > 80%
- EKS pod restart count > 3
- DynamoDB throttling
- Step Functions execution failures > 0
