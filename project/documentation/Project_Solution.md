# Project Solution: Troubleshoot and Optimize a Multi-Tier AWS Application

## Overview

This document provides the expected outcomes, verification commands, and sample implementations for each part of the final project. Solutions are organized by **MVP (Required)** and **Stretch Goals (Optional)**.

**Note**: This document is for course authors and mentors, not students.

---

## Solution Code Reference

The solution code is organized into three tiers in `Course_Project/dev/`:

| Directory | Description | Use Case |
|-----------|-------------|----------|
| `solution_code_mvp/` | Basic implementations meeting MVP requirements | Grade pass/fail submissions |
| `solution_code_stretch/` | MVP + Advanced features for stretch goals | Reference for advanced feedback |
| `solution_code_full/` | Complete reference with all optimizations | Instructor reference |

---

## Part 1 Solution: Implementing Observability

### MVP Solutions (Required)

#### 1.1 Structured Logging Implementation (MVP)

**What's Required**: JSON-formatted logs with timestamp, level, service name, and contextual data.

**Expected Lambda Logging Code (Python)**:

```python
# MVP: Basic structured logging - no correlation IDs required
import json
import os
from datetime import datetime

def log_structured(level: str, message: str, **context):
    """MVP structured logging - outputs JSON format."""
    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "level": level,
        "service": "product-service",
        "function": os.environ.get('AWS_LAMBDA_FUNCTION_NAME', 'local'),
        "message": message,
        **context
    }
    print(json.dumps(log_entry))

def log_info(message: str, **context):
    log_structured("INFO", message, **context)

def log_error(message: str, error=None, **context):
    if error:
        context["error"] = str(error)
        context["error_type"] = type(error).__name__
    log_structured("ERROR", message, **context)
```

**Verification Commands**:
```bash
# Query structured logs in CloudWatch Logs Insights
aws logs start-query \
  --log-group-name "/aws/lambda/product-service" \
  --start-time $(date -d '1 hour ago' +%s) \
  --end-time $(date +%s) \
  --query-string 'fields @timestamp, level, message, service
    | filter level = "INFO"
    | sort @timestamp desc
    | limit 10'

# Verify JSON format with filter
aws logs filter-log-events \
  --log-group-name "/aws/lambda/product-service" \
  --filter-pattern '{ $.level = "INFO" }' \
  --limit 5
```

#### 1.2 X-Ray Tracing on Lambda (MVP)

**What's Required**: Active tracing enabled on Lambda with traces visible in X-Ray console.

**Lambda Configuration**:
```bash
# Enable active tracing on Lambda
aws lambda update-function-configuration \
  --function-name product-service \
  --tracing-config Mode=Active

# Verify configuration
aws lambda get-function-configuration \
  --function-name product-service \
  --query 'TracingConfig'
# Expected: {"Mode": "Active"}
```

#### 1.3 Basic Custom Metrics with EMF (MVP)

**What's Required**: At least 2 custom metrics (e.g., OrderCount, ProductViews) with at least 1 dimension.

**Expected EMF Implementation**:
```python
# MVP: Basic EMF metrics - 2 metrics, 1 dimension
import json
import time

def emit_metric(metric_name: str, value: float, unit: str = "Count"):
    """MVP: Emit a single metric using EMF format."""
    emf_log = {
        "_aws": {
            "Timestamp": int(time.time() * 1000),
            "CloudWatchMetrics": [{
                "Namespace": "ShopFast/Application",
                "Dimensions": [["Service"]],
                "Metrics": [{"Name": metric_name, "Unit": unit}]
            }]
        },
        "Service": "product-service",
        metric_name: value
    }
    print(json.dumps(emf_log))

# Usage
emit_metric("ProductViews", 1)
emit_metric("Errors", 1)
```

**Verification**:
```bash
# Query custom metrics
aws cloudwatch list-metrics --namespace "ShopFast/Application"

aws cloudwatch get-metric-statistics \
  --namespace "ShopFast/Application" \
  --metric-name "ProductViews" \
  --dimensions Name=Service,Value=product-service \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) \
  --period 300 \
  --statistics Sum
```

#### 1.4 Basic Operational Dashboard (MVP)

**What's Required**: Dashboard with 3 widgets: request/error rates, latency (at least P50), and one custom metric.

**Dashboard JSON**:
```json
{
  "widgets": [
    {
      "type": "metric",
      "x": 0, "y": 0, "width": 12, "height": 6,
      "properties": {
        "title": "Lambda Invocations & Errors",
        "metrics": [
          ["AWS/Lambda", "Invocations", "FunctionName", "shopfast-product-service", {"stat": "Sum"}],
          [".", "Errors", ".", ".", {"stat": "Sum", "color": "#d62728"}]
        ],
        "period": 60
      }
    },
    {
      "type": "metric",
      "x": 12, "y": 0, "width": 12, "height": 6,
      "properties": {
        "title": "Lambda Duration",
        "metrics": [
          ["AWS/Lambda", "Duration", "FunctionName", "shopfast-product-service", {"stat": "p50"}]
        ]
      }
    },
    {
      "type": "metric",
      "x": 0, "y": 6, "width": 12, "height": 6,
      "properties": {
        "title": "Custom Business Metrics",
        "metrics": [
          ["ShopFast/Application", "ProductViews", "Service", "product-service"]
        ]
      }
    }
  ]
}
```

---

### Stretch Goal Solutions (Optional)

#### 1.5 Correlation ID Propagation (Stretch)

**Expected Pattern**:
```python
# Stretch: Correlation ID handling
import uuid

def get_correlation_id(event):
    """Extract correlation ID from headers or generate new one."""
    headers = event.get('headers', {}) or {}
    return (
        headers.get('x-correlation-id') or
        headers.get('X-Correlation-ID') or
        str(uuid.uuid4())
    )

def log_with_correlation(level, message, correlation_id, **context):
    """Log with correlation ID included."""
    log_structured(level, message, correlation_id=correlation_id, **context)
```

#### 1.6 X-Ray Annotations and Metadata (Stretch)

```python
from aws_xray_sdk.core import xray_recorder

def handler(event, context):
    segment = xray_recorder.current_segment()

    # Annotations (indexed, searchable)
    segment.put_annotation('user_id', event.get('userId'))
    segment.put_annotation('order_id', event.get('orderId'))

    # Metadata (not indexed, for debugging)
    segment.put_metadata('request', {'path': event.get('path')})
```

#### 1.7 Enhanced Dashboard (Stretch)

Add P90/P99 latency, log insights widgets, and alarm status widgets.

---

## Part 2 Solution: Diagnosing and Fixing Issues

### MVP Solutions (Required)

Students must document and fix **at least 3** of the following planted issues:

#### Planted Issue #1: Lambda Timeout (MVP)

**Symptoms**: Product API returns 504 Gateway Timeout intermittently

**Root Cause**: Lambda configured with 3-second timeout, but DynamoDB scan takes 4-5 seconds.

**Discovery (Logs Insights Query)**:
```sql
filter @type = "REPORT"
| filter @duration > 3000
| stats count() as timeouts by bin(1h)
```

**Fix**:
```bash
# Option 1: Increase timeout (quick fix)
aws lambda update-function-configuration \
  --function-name product-service \
  --timeout 10

# Option 2: Optimize code (better fix) - add pagination
```

---

#### Planted Issue #2: Lambda Low Memory (MVP)

**Symptoms**: Product API has high cold start times, intermittent slow responses

**Root Cause**: Lambda configured with 128MB memory causing slow cold starts and execution.

**Discovery (X-Ray)**:
```sql
-- X-Ray Analytics query
filter service.name = "product-service"
| filter cold_start = true
| stats avg(duration) as avg_cold_start by service.name
-- Shows cold starts averaging 3-4 seconds
```

**Discovery (CloudWatch Logs)**:
```sql
filter @type = "REPORT"
| stats avg(@duration), max(@memorySize), avg(@maxMemoryUsed) by bin(1h)
-- Shows memory usage near limit
```

**Fix**:
```yaml
# In template.yaml
MemorySize: 512  # Increased from 128MB
```

---

#### Planted Issue #3: DEBUG Log Level (MVP)

**Symptoms**: Excessive CloudWatch Logs costs, log groups filling rapidly

**Root Cause**: LOG_LEVEL set to DEBUG in production, causing verbose output.

**Discovery (CloudWatch Logs Insights)**:
```sql
filter @message like /DEBUG/
| stats count() as debug_logs by bin(1h)
-- Shows thousands of DEBUG messages per hour
```

**Fix**:
```yaml
# In template.yaml environment variables
LOG_LEVEL: INFO  # Changed from DEBUG
```

---

#### Planted Issue #4: SNS Message Attribute Missing (MVP)

**Symptoms**: Order notifications not sent; messages in DLQ

**Root Cause**: Publisher missing `eventType` message attribute that filter policy requires.

**Discovery**:
```bash
aws sqs receive-message --queue-url {dlq-url} \
  --message-attribute-names All
# Shows messages missing eventType attribute
```

**Fix**: Add MessageAttributes to SNS publish call.

---

### Stretch Goal Solutions (Optional)

#### Planted Issue #5: EventBridge Rule Mismatch (Stretch)

**Root Cause**: Rule expects `"detail-type": "OrderEvent"` but source sends `"order.created"`.

#### Planted Issue #6: API Gateway 504 Timeout (Stretch)

**Root Cause**: Synchronous Step Functions workflow exceeds API Gateway 29s limit.

#### Planted Issue #7: Step Functions Stuck Workflow (Stretch)

**Root Cause**: Wait state configured with far-future timestamp (`2099-01-01`).

---

## Part 3 Solution: Performance Optimization

### MVP Solutions (Required)

#### 3.1 Lambda Right-Sizing (MVP)

**Analysis**:
```bash
# Check current memory allocation
aws lambda get-function-configuration --function-name product-service \
  --query 'MemorySize'
# Output: 3008 (over-provisioned)

# Check actual memory usage
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name "MaxMemoryUsed" \
  --dimensions Name=FunctionName,Value=product-service \
  --statistics Maximum
# Output: ~250MB
```

**Fix**:
```bash
# Right-size to 512MB
aws lambda update-function-configuration \
  --function-name product-service \
  --memory-size 512
```

#### 3.2 ElastiCache Integration (MVP)

**Expected Implementation**:
```python
import redis
import json
import os

redis_client = redis.Redis(
    host=os.environ['REDIS_HOST'],
    port=6379,
    decode_responses=True
)

CACHE_TTL = 300  # 5 minutes

def get_product(product_id):
    # Check cache first
    cache_key = f"product:{product_id}"
    cached = redis_client.get(cache_key)

    if cached:
        print(json.dumps({"message": "Cache HIT", "product_id": product_id}))
        return json.loads(cached)

    # Cache miss - get from DynamoDB
    print(json.dumps({"message": "Cache MISS", "product_id": product_id}))
    product = get_from_dynamodb(product_id)

    # Store in cache
    redis_client.setex(cache_key, CACHE_TTL, json.dumps(product))

    return product
```

**Verification**:
```bash
# Check cache hits in logs
aws logs filter-log-events \
  --log-group-name "/aws/lambda/product-service" \
  --filter-pattern '"Cache HIT"'
```

---

### Stretch Goal Solutions (Optional)

#### 3.3 CloudFront Caching (Stretch)

Configure CloudFront cache behaviors for static assets with appropriate TTLs based on content type (e.g., longer TTLs for versioned JS/CSS, shorter for HTML).

#### 3.4 SNS Filter Policies (Stretch)

```bash
aws sns set-subscription-attributes \
  --subscription-arn {arn} \
  --attribute-name FilterPolicy \
  --attribute-value '{"eventType": ["ORDER_CREATED", "ORDER_SHIPPED"]}'
```

---

## Part 4 Solution: Monitoring and Alerting

### MVP Solutions (Required)

#### 4.1 Health Endpoint (MVP)

**Required**: Health endpoint that checks at least one dependency.

```python
from fastapi import FastAPI
from fastapi.responses import JSONResponse

@app.get("/health")
async def health():
    checks = {}

    # Check DynamoDB
    try:
        table.scan(Limit=1)
        checks["database"] = {"status": "ok"}
    except Exception as e:
        checks["database"] = {"status": "error", "message": str(e)}

    is_healthy = all(c.get("status") == "ok" for c in checks.values())

    return JSONResponse(
        status_code=200 if is_healthy else 503,
        content={"status": "healthy" if is_healthy else "unhealthy", "checks": checks}
    )
```

#### 4.2 CloudWatch Alarms (MVP - 3 Required)

```bash
# Alarm 1: Lambda Errors
aws cloudwatch put-metric-alarm \
  --alarm-name "ProductService-Errors" \
  --metric-name Errors \
  --namespace AWS/Lambda \
  --dimensions Name=FunctionName,Value=shopfast-product-service \
  --statistic Sum \
  --period 300 \
  --threshold 5 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 2 \
  --alarm-actions {sns-topic-arn}

# Alarm 2: Lambda Duration (Timeout Warning)
aws cloudwatch put-metric-alarm \
  --alarm-name "ShopFast-Lambda-Duration" \
  --metric-name Duration \
  --namespace AWS/Lambda \
  --dimensions Name=FunctionName,Value=shopfast-product-service \
  --statistic Average \
  --period 60 \
  --threshold 2500 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 3 \
  --alarm-actions {sns-topic-arn}

# Alarm 3: DynamoDB Throttling
aws cloudwatch put-metric-alarm \
  --alarm-name "ShopFast-DynamoDB-Throttling" \
  --metric-name ThrottledRequests \
  --namespace AWS/DynamoDB \
  --dimensions Name=TableName,Value=shopfast-products \
  --statistic Sum \
  --period 60 \
  --threshold 5 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 2 \
  --alarm-actions {sns-topic-arn}
```

#### 4.3 SNS Notifications (MVP)

```bash
# Create topic
aws sns create-topic --name shopfast-alerts

# Subscribe email
aws sns subscribe \
  --topic-arn {topic-arn} \
  --protocol email \
  --notification-endpoint student@example.com

# Test notification
aws sns publish \
  --topic-arn {topic-arn} \
  --message "Test alert from ShopFast monitoring"
```

---

### Stretch Goal Solutions (Optional)

#### 4.4 SLI/SLO Dashboard (Stretch)

Dashboard with availability, latency P99, and error rate widgets with SLO target annotations.

---

## Expected Outcomes Summary

### MVP Completion (Required to Pass)

| Part | Metric | Expected Outcome |
|------|--------|------------------|
| 1 | Structured logs | JSON format with required fields |
| 1 | X-Ray tracing | Lambda visible in service map |
| 1 | Custom metrics | 2+ metrics in ShopFast namespace |
| 1 | Dashboard | 3 widgets (invocations, latency, custom) |
| 2 | Issues documented | 3+ with symptoms, root cause, fix |
| 2 | Fix verification | Before/after evidence |
| 3 | Lambda right-sizing | Memory reduced with justification |
| 3 | ElastiCache | Cache hit/miss in logs |
| 4 | Health endpoint | Dependency check implemented |
| 4 | Alarms | 3+ alarms configured |
| 4 | Notifications | Email subscription confirmed |

### Stretch Goal Completion (Optional)

| Part | Feature | Evidence Required |
|------|---------|-------------------|
| 1 | Correlation IDs | Same ID across service logs |
| 1 | X-Ray annotations | Searchable by user_id, order_id |
| 2 | All issues fixed | Documentation for each planted issue |
| 2 | Log-trace correlation | Demonstrated technique |
| 3 | CloudFront caching | Cache hit rate metrics |
| 3 | SNS filter policies | Reduced processing visible |
| 4 | SLI/SLO dashboard | Targets with annotations |

---

## Time Estimates

| Part | MVP Only | With Stretch Goals |
|------|----------|-------------------|
| Part 1: Observability | 60-75 min | 90-120 min |
| Part 2: Debugging | 60-75 min | 90-120 min |
| Part 3: Optimization | 45-60 min | 60-90 min |
| Part 4: Monitoring | 30-45 min | 45-60 min |
| **Total** | **3-4 hours** | **4-6 hours** |

---

## Screenshot Naming Reference

Students should use the following standardized screenshot naming convention throughout their submission:

| Part | Screenshot | Description |
|------|------------|-------------|
| 1 | `Project_Pt_1_screenshot_1.png` | CloudWatch Logs showing JSON structured logs |
| 1 | `Project_Pt_1_screenshot_2.png` | X-Ray service map with Lambda traces |
| 1 | `Project_Pt_1_screenshot_3.png` | CloudWatch Metrics showing custom EMF metrics |
| 1 | `Project_Pt_1_screenshot_4.png` | Operational dashboard with 3+ widgets |
| 2 | `Project_Pt_2_screenshot_1.png` | Logs Insights query results |
| 2 | `Project_Pt_2_screenshot_2.png` | X-Ray trace showing issue root cause |
| 2 | `Project_Pt_2_screenshot_3.png` | Lambda memory before/after metrics |
| 2 | `Project_Pt_2_screenshot_4.png` | Log volume comparison (DEBUG vs INFO) |
| 2 | `Project_Pt_2_screenshot_5.png` | DLQ message inspection |
| 3 | `Project_Pt_3_screenshot_1.png` | X-Ray trace with performance bottlenecks |
| 3 | `Project_Pt_3_screenshot_2.png` | Lambda memory optimization comparison |
| 3 | `Project_Pt_3_screenshot_3.png` | ElastiCache integration (cache hit/miss logs) |
| 4 | `Project_Pt_4_screenshot_1.png` | Health endpoint response |
| 4 | `Project_Pt_4_screenshot_2.png` | CloudWatch alarms configuration |
| 4 | `Project_Pt_4_screenshot_3.png` | SNS notification email received |

---

## Verification Checklist

- [ ] All MVP solution code in `solution_code_mvp/` compiles and runs
- [ ] Stretch goal code in `solution_code_stretch/` extends MVP correctly
- [ ] All CLI commands tested and working
- [ ] Rubric items map to specific solution elements
- [ ] MVP can be completed in 3-4 hours by competent student
