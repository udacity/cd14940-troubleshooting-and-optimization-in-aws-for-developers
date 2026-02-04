# Detailed Project Solution: Troubleshoot and Optimize a Serverless AWS Application

## Introduction

### Purpose

This document provides a detailed, step-by-step walkthrough for completing the ShopFast troubleshooting and optimization project. It serves as an **instructor verification guide** with exact file paths, line numbers, and deployment commands for each task.

### Prerequisites

Before starting this guide, ensure:
- Your AWS environment is bootstrapped using the provided setup script
- You have AWS Console access with appropriate permissions
- AWS CLI is configured with valid credentials
- You can access CloudWatch, X-Ray, Lambda, DynamoDB, and other services

### How to Use This Guide

1. **Follow in order**: Complete Part 1 before Part 2, etc.
2. **Work incrementally**: Implement one change, verify it works, then proceed
3. **Take screenshots**: Capture evidence as you complete each task using the naming convention
4. **Document issues**: Note symptoms, root causes, and fixes as you discover them

### Screenshot Naming Convention

All screenshots must follow this pattern:
```
Project_Pt_X_screenshot_Y.png
```
Where X = Part number (1-4) and Y = Screenshot number within that part.

---

## Instructor Environment Setup

### Accessing Cloud9

1. Open the **AWS Management Console**
2. Navigate to **Cloud9** service (search in the top bar)
3. In the left sidebar, click **Your environments**
4. Find the environment named `shopfast-dev`
5. Click **Open** to launch the Cloud9 IDE

### Setting Up the Working Directory

After opening Cloud9, open a terminal and set up your working directory:

```bash
# Navigate to the project root
cd ~/environment/cd14940-troubleshooting-and-optimization-in-aws-for-developers-solution/project

# Verify the project structure
ls -la
```

**Expected output:**
```
bootstrap_scripts/
documentation/
solution/
starter_code/
```

### Verifying Bootstrap Completed Successfully

```bash
# Check that all CloudFormation stacks are deployed
aws cloudformation list-stacks --query "StackSummaries[?starts_with(StackName, 'shopfast-') && StackStatus=='CREATE_COMPLETE'].StackName"

# Verify Lambda functions exist
aws lambda list-functions --query "Functions[?starts_with(FunctionName, 'shopfast-')].FunctionName"

# Check DynamoDB table
aws dynamodb describe-table --table-name shopfast-products-dev --query 'Table.TableName'
```

### Project File Structure Reference

```
project/
├── starter_code/lambdas/
│   ├── product-service/
│   │   ├── handler.py        ← Main Lambda code to edit
│   │   ├── template.yaml     ← SAM template with planted issues
│   │   └── requirements.txt
│   └── notification-handler/
│       ├── handler.py
│       └── template.yaml     ← Has SNS filter policy issue
├── bootstrap_scripts/
│   ├── bootstrap.sh          ← Main deployment orchestration
│   ├── cleanup.sh
│   ├── scripts/
│   │   └── deploy-lambdas.sh ← Lambda-specific deployment
│   └── templates/
│       ├── messaging.yaml    ← EventBridge issue
│       └── stepfunctions.yaml ← Wait state issue
└── solution/                  ← Reference implementation
```

### AWS Resource Names Quick Reference

| Resource | Name |
|----------|------|
| Product Service Lambda | `shopfast-product-service-dev` |
| Notification Handler Lambda | `shopfast-notification-handler` |
| DynamoDB Table | `shopfast-products-dev` |
| SNS Topics | `shopfast-notifications-dev`, `shopfast-product-events-dev` |
| SQS Queue | `shopfast-product-processing-dev` |
| SQS DLQ | `shopfast-product-processing-dlq-dev` |
| Step Functions | `shopfast-product-workflow-dev` |
| CloudWatch Log Group | `/aws/lambda/shopfast-product-service-dev` |

---

## Planted Issues Summary

This project contains 8 planted issues across various files. Below is the master reference table:

| # | Issue | File (from project root) | Lines | Current Value | Fix |
|---|-------|-------------------------|-------|---------------|-----|
| 1 | Low Memory | `starter_code/lambdas/product-service/template.yaml` | 8-11 | `MemorySize: 128` | `MemorySize: 512` |
| 2 | Short Timeout | `starter_code/lambdas/product-service/template.yaml` | 12-16 | `Timeout: 3` | `Timeout: 30` |
| 3 | DEBUG Log Level | `starter_code/lambdas/product-service/template.yaml` | 21-24 | `LOG_LEVEL: DEBUG` | `LOG_LEVEL: INFO` |
| 4 | X-Ray Disabled | `starter_code/lambdas/product-service/template.yaml` | 34-37 | `Tracing: PassThrough` | `Tracing: Active` |
| 5 | Short Log Retention | `starter_code/lambdas/product-service/template.yaml` | 47-50 | `RetentionInDays: 1` | `RetentionInDays: 7` |
| 6 | SNS Filter Mismatch | `starter_code/lambdas/notification-handler/template.yaml` | 28-39 | Missing `eventType` attribute in publisher | Add MessageAttributes to publish call |
| 7 | EventBridge Pattern | `bootstrap_scripts/templates/messaging.yaml` | 119-133 | `detail-type: ProductEvent` | `detail-type: product.updated` |
| 8 | Step Functions Wait | `bootstrap_scripts/templates/stepfunctions.yaml` | 151-156 | `Timestamp: "2099-01-01T00:00:00Z"` | `Seconds: 30` |

---

## Part 1: Implement Comprehensive Observability

**Time Estimate**: MVP 60-75 minutes | With Stretch Goals 90-120 minutes

### 1.1 Structured Logging Implementation (MVP)

#### Objective
Replace basic `print()` statements with JSON-structured logging that includes timestamp, level, service name, and contextual data.

#### File to Edit
`starter_code/lambdas/product-service/handler.py`

#### Current Code (Starter - Lines 39, 59, 74, 85, 96)
```python
print(f"Received event: {json.dumps(event)}")
print(f"Error: {str(e)}")
print("Fetching all products from DynamoDB...")
print(f"Found {len(products)} products")
print(f"Fetching product: {product_id}")
```

#### Step 1: Add the Logging Utility Functions

Add this code after line 20 (after the `table = dynamodb.Table(table_name)` line):

```python
from datetime import datetime

def log_structured(level: str, message: str, **context):
    """Output structured JSON logs for CloudWatch."""
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
    """Log INFO level message."""
    log_structured("INFO", message, **context)

def log_warn(message: str, **context):
    """Log WARN level message."""
    log_structured("WARN", message, **context)

def log_error(message: str, error=None, **context):
    """Log ERROR level message with optional exception details."""
    if error:
        context["error"] = str(error)
        context["error_type"] = type(error).__name__
    log_structured("ERROR", message, **context)
```

#### Step 2: Replace print() Statements

| Location | Before | After |
|----------|--------|-------|
| Line 39 | `print(f"Received event: {json.dumps(event)}")` | `log_info("Request received", path=event.get('path'), method=event.get('httpMethod'))` |
| Line 59 | `print(f"Error: {str(e)}")` | `log_error("Request failed", error=e)` |
| Line 74 | `print("Fetching all products from DynamoDB...")` | `log_info("Fetching products from DynamoDB")` |
| Line 85 | `print(f"Found {len(products)} products")` | `log_info("Retrieved products", count=len(products))` |
| Line 96 | `print(f"Fetching product: {product_id}")` | `log_info("Fetching product", product_id=product_id)` |

#### Step 3: Deploy and Verify

```bash
# Navigate to project directory
cd ~/environment/cd14940-troubleshooting-and-optimization-in-aws-for-developers-solution/project

# Build the Lambda function
cd starter_code/lambdas/product-service
sam build

# Deploy using SAM sync
SAM_BUCKET="shopfast-sam-artifacts-$(aws sts get-caller-identity --query Account --output text)"
echo Y | sam sync \
    --stack-name shopfast-lambda \
    --s3-bucket "${SAM_BUCKET}" \
    --no-watch \
    --no-dependency-layer

# Return to project root
cd ~/environment/cd14940-troubleshooting-and-optimization-in-aws-for-developers-solution/project
```

#### Step 4: Invoke and Verify Logs

```bash
# Invoke the function
aws lambda invoke \
  --function-name shopfast-product-service-dev \
  --payload '{"httpMethod": "GET", "path": "/products"}' \
  --cli-binary-format raw-in-base64-out \
  response.json

# View structured logs
aws logs filter-log-events \
  --log-group-name "/aws/lambda/shopfast-product-service-dev" \
  --filter-pattern '{ $.level = "INFO" }' \
  --limit 5
```

#### Expected Output

```json
{
  "timestamp": "2026-02-03T15:30:45.123Z",
  "level": "INFO",
  "service": "product-service",
  "function": "shopfast-product-service-dev",
  "message": "Request received",
  "path": "/products",
  "method": "GET"
}
```

#### Screenshot: `Project_Pt_1_screenshot_1.png`
Navigate to **CloudWatch → Log groups → /aws/lambda/shopfast-product-service-dev** and capture a screenshot showing JSON-formatted log entries with the required fields (timestamp, level, service, message, context).

---

### 1.2 Enable X-Ray Tracing on Lambda (MVP)

#### Objective
Enable active tracing on Lambda functions so traces appear in the X-Ray console.

#### File to Edit
`starter_code/lambdas/product-service/template.yaml`

#### Location
Lines 34-37

#### Current Code (Planted Issue #4)
```yaml
      # PLANTED ISSUE #4: X-Ray tracing disabled - no distributed tracing visibility
      # Discovery: No X-Ray traces appear for Lambda function
      # Fix: Add Tracing: Active
      Tracing: PassThrough
```

#### Fixed Code
```yaml
      # FIX: Enable X-Ray active tracing for distributed tracing visibility
      Tracing: Active
```

#### Deploy Changes

```bash
cd ~/environment/cd14940-troubleshooting-and-optimization-in-aws-for-developers-solution/project/starter_code/lambdas/product-service
sam build

SAM_BUCKET="shopfast-sam-artifacts-$(aws sts get-caller-identity --query Account --output text)"
echo Y | sam sync \
    --stack-name shopfast-lambda \
    --s3-bucket "${SAM_BUCKET}" \
    --no-watch \
    --no-dependency-layer

cd ~/environment/cd14940-troubleshooting-and-optimization-in-aws-for-developers-solution/project
```

#### Verify X-Ray is Enabled

```bash
# Verify the configuration
aws lambda get-function-configuration \
  --function-name shopfast-product-service-dev \
  --query 'TracingConfig'
```

**Expected output:**
```json
{
    "Mode": "Active"
}
```

#### Generate Traces

```bash
# Invoke function multiple times to generate traces
for i in {1..5}; do
  aws lambda invoke \
    --function-name shopfast-product-service-dev \
    --payload '{"httpMethod": "GET", "path": "/products"}' \
    --cli-binary-format raw-in-base64-out \
    /dev/null
  sleep 1
done
```

#### View Service Map

1. Navigate to **AWS Console → X-Ray → Service map**
2. Select the appropriate time range (last 15 minutes)
3. Verify `shopfast-product-service-dev` appears in the service map

#### Screenshot: `Project_Pt_1_screenshot_2.png`
Capture the X-Ray service map showing the Lambda function with connections to downstream services (DynamoDB, etc.).

---

### 1.3 Implement Basic Custom Metrics with EMF (MVP)

#### Objective
Publish at least 2 custom business metrics (ProductViews, Errors) using CloudWatch Embedded Metric Format.

#### File to Edit
`starter_code/lambdas/product-service/handler.py`

#### Step 1: Add EMF Metrics Helper

Add this function after the logging utility functions (around line 45):

```python
import time

def emit_metric(metric_name: str, value: float, unit: str = "Count"):
    """Emit a metric using CloudWatch Embedded Metric Format."""
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
```

#### Step 2: Add Metric Calls in Handler

Update the `lambda_handler` function to emit metrics:

**In get_all_products() before the return statement:**
```python
    # Emit ProductViews metric
    emit_metric("ProductViews", len(products))
```

**In the exception handler (around line 58):**
```python
    except Exception as e:
        log_error("Request failed", error=e)
        emit_metric("Errors", 1)  # ADD THIS LINE
        return {
            'statusCode': 500,
            ...
        }
```

**In get_product() after successful retrieval:**
```python
    emit_metric("ProductViews", 1)
```

#### Deploy and Verify

```bash
cd ~/environment/cd14940-troubleshooting-and-optimization-in-aws-for-developers-solution/project/starter_code/lambdas/product-service
sam build

SAM_BUCKET="shopfast-sam-artifacts-$(aws sts get-caller-identity --query Account --output text)"
echo Y | sam sync \
    --stack-name shopfast-lambda \
    --s3-bucket "${SAM_BUCKET}" \
    --no-watch \
    --no-dependency-layer
```

#### Verify Metrics Appear

```bash
# Generate some traffic
for i in {1..10}; do
  aws lambda invoke \
    --function-name shopfast-product-service-dev \
    --payload '{"httpMethod": "GET", "path": "/products"}' \
    --cli-binary-format raw-in-base64-out \
    /dev/null
done

# Wait a few minutes for metrics to appear, then list custom metrics
aws cloudwatch list-metrics --namespace "ShopFast/Application"
```

#### Screenshot: `Project_Pt_1_screenshot_3.png`
Navigate to **CloudWatch → Metrics → All metrics → ShopFast/Application** and capture a screenshot showing your custom metrics (ProductViews, Errors) with the Service dimension.

---

### 1.4 Build Basic Operational Dashboard (MVP)

#### Objective
Create a CloudWatch dashboard with at least 3 widgets: request/error rates, latency (P50), and one custom business metric.

#### Step 1: Create Dashboard JSON File

Create a new file at `starter_code/observability/dashboard.json`:

```bash
mkdir -p ~/environment/cd14940-troubleshooting-and-optimization-in-aws-for-developers-solution/project/starter_code/observability
```

Create the file with this content:

```json
{
  "widgets": [
    {
      "type": "metric",
      "x": 0,
      "y": 0,
      "width": 12,
      "height": 6,
      "properties": {
        "title": "Lambda Invocations & Errors",
        "region": "us-east-1",
        "metrics": [
          ["AWS/Lambda", "Invocations", "FunctionName", "shopfast-product-service-dev", {"stat": "Sum", "period": 60}],
          [".", "Errors", ".", ".", {"stat": "Sum", "period": 60, "color": "#d62728"}]
        ],
        "view": "timeSeries",
        "stacked": false
      }
    },
    {
      "type": "metric",
      "x": 12,
      "y": 0,
      "width": 12,
      "height": 6,
      "properties": {
        "title": "Lambda Duration (P50)",
        "region": "us-east-1",
        "metrics": [
          ["AWS/Lambda", "Duration", "FunctionName", "shopfast-product-service-dev", {"stat": "p50", "period": 60}]
        ],
        "view": "timeSeries"
      }
    },
    {
      "type": "metric",
      "x": 0,
      "y": 6,
      "width": 12,
      "height": 6,
      "properties": {
        "title": "Product Views (Custom Metric)",
        "region": "us-east-1",
        "metrics": [
          ["ShopFast/Application", "ProductViews", "Service", "product-service", {"stat": "Sum", "period": 60}]
        ],
        "view": "timeSeries"
      }
    }
  ]
}
```

#### Step 2: Create Dashboard via CLI

```bash
cd ~/environment/cd14940-troubleshooting-and-optimization-in-aws-for-developers-solution/project

# Create the dashboard
aws cloudwatch put-dashboard \
  --dashboard-name "ShopFast-Operations" \
  --dashboard-body file://starter_code/observability/dashboard.json

# Verify dashboard was created
aws cloudwatch list-dashboards
```

#### Step 3: View Dashboard in Console

Navigate to **CloudWatch → Dashboards → ShopFast-Operations** to view your dashboard.

#### Screenshot: `Project_Pt_1_screenshot_4.png`
Capture a screenshot of the complete dashboard showing all three widgets (Invocations/Errors, Duration, ProductViews).

---

### 1.5 Correlation ID Propagation (Stretch Goal)

#### Implementation

Add to `starter_code/lambdas/product-service/handler.py`:

```python
import uuid

def get_correlation_id(event, context):
    """Extract correlation ID from headers or generate a new one."""
    headers = event.get('headers', {}) or {}
    correlation_id = (
        headers.get('x-correlation-id') or
        headers.get('X-Correlation-ID') or
        context.aws_request_id or
        str(uuid.uuid4())
    )
    return correlation_id

def log_with_correlation(level, message, correlation_id, **context):
    """Log with correlation ID included in all entries."""
    log_structured(level, message, correlation_id=correlation_id, **context)
```

---

### 1.6 X-Ray Annotations and Metadata (Stretch Goal)

#### Implementation

Add to `starter_code/lambdas/product-service/handler.py`:

```python
from aws_xray_sdk.core import xray_recorder

def handler(event, context):
    # Get the current segment
    segment = xray_recorder.current_segment()

    # Add annotations (indexed, searchable in X-Ray console)
    segment.put_annotation('product_id', event.get('productId', 'unknown'))
    segment.put_annotation('request_type', event.get('action', 'unknown'))

    # Add metadata (not indexed, for debugging)
    segment.put_metadata('request', {
        'path': event.get('path'),
        'headers': event.get('headers')
    })
```

---

### 1.7 Enhanced Dashboard (Stretch Goal)

Add P90/P99 latency metrics by adding this widget to your dashboard:

```json
{
  "type": "metric",
  "x": 12,
  "y": 6,
  "width": 12,
  "height": 6,
  "properties": {
    "title": "Lambda Duration Percentiles",
    "metrics": [
      ["AWS/Lambda", "Duration", "FunctionName", "shopfast-product-service-dev", {"stat": "p50", "label": "P50"}],
      ["...", {"stat": "p90", "label": "P90"}],
      ["...", {"stat": "p99", "label": "P99"}]
    ]
  }
}
```

---

## Part 2: Diagnose and Fix Application Issues

**Time Estimate**: MVP 60-75 minutes | With Stretch Goals 90-120 minutes

### 2.1 CloudWatch Logs Insights Queries (MVP)

#### Objective
Write Logs Insights queries to find error patterns and identify issues.

Navigate to **CloudWatch → Logs Insights** and select the log group `/aws/lambda/shopfast-product-service-dev`.

#### Query 1: Find Error Patterns

```sql
fields @timestamp, @message, level, message, error_type
| filter level = "ERROR"
| stats count() as error_count by error_type, message
| sort error_count desc
| limit 20
```

#### Query 2: Identify Timeouts

```sql
filter @type = "REPORT"
| filter @duration > 3000
| stats count() as timeout_count, avg(@duration) as avg_duration, max(@duration) as max_duration by bin(1h)
| sort @timestamp desc
```

#### Query 3: Track Error Frequency Over Time

```sql
fields @timestamp, level
| filter level = "ERROR"
| stats count() as errors by bin(5m)
| sort @timestamp desc
```

#### Screenshot: `Project_Pt_2_screenshot_1.png`
Capture a screenshot of the Logs Insights console showing one of your queries with results that identify error patterns.

---

### 2.2 Planted Issue #1: Lambda Timeout (MVP)

#### Symptoms
- Product API intermittently returns 504 Gateway Timeout
- Some requests complete successfully while others fail
- X-Ray traces show requests exceeding 3 seconds

#### Discovery Using Logs Insights

Navigate to **CloudWatch → Logs Insights** and run:

```sql
filter @type = "REPORT"
| filter @duration > 2500
| fields @timestamp, @duration, @requestId
| sort @timestamp desc
| limit 20
```

Look for invocations approaching or exceeding the 3-second limit.

#### Discovery Using X-Ray

1. Navigate to **X-Ray → Traces**
2. Filter by `service.name = "shopfast-product-service-dev"`
3. Sort by duration (descending)
4. Look for traces that timeout

#### Root Cause

**File:** `starter_code/lambdas/product-service/template.yaml`
**Lines:** 12-16

```yaml
    # PLANTED ISSUE #2: Timeout is too short (3s) for DynamoDB scan operations
    # which can take 4-5 seconds on cold start + large table scan
    # Discovery: CloudWatch Logs show "Task timed out after 3.00 seconds"
    # Fix: Increase to 30 seconds
    Timeout: 3
```

Lambda configured with 3-second timeout, but DynamoDB scan operations can take 4-5 seconds under load.

#### Fix

**Edit the file:** `starter_code/lambdas/product-service/template.yaml`

**Change line 16 from:**
```yaml
    Timeout: 3
```

**To:**
```yaml
    Timeout: 30
```

#### Deploy Fix

```bash
cd ~/environment/cd14940-troubleshooting-and-optimization-in-aws-for-developers-solution/project/starter_code/lambdas/product-service
sam build

SAM_BUCKET="shopfast-sam-artifacts-$(aws sts get-caller-identity --query Account --output text)"
echo Y | sam sync \
    --stack-name shopfast-lambda \
    --s3-bucket "${SAM_BUCKET}" \
    --no-watch \
    --no-dependency-layer
```

#### Verify Fix

```bash
aws lambda get-function-configuration \
  --function-name shopfast-product-service-dev \
  --query 'Timeout'
# Expected: 30
```

#### Screenshot: `Project_Pt_2_screenshot_2.png`
Capture an X-Ray trace showing a request that exceeded the timeout, with the timeline breakdown visible.

---

### 2.3 Planted Issue #2: Lambda Low Memory (MVP)

#### Symptoms
- High cold start times (3-4 seconds)
- Intermittent slow responses even for warm invocations
- Memory usage near the configured limit

#### Discovery Using CloudWatch Logs

Navigate to **CloudWatch → Logs Insights** and run:

```sql
filter @type = "REPORT"
| stats avg(@duration) as avg_duration,
        max(@maxMemoryUsed) as max_memory_used,
        avg(@maxMemoryUsed) as avg_memory_used,
        max(@memorySize) as configured_memory
| limit 1
```

Look for `max_memory_used` approaching `configured_memory` (128 MB).

#### Discovery Using CLI

```bash
aws lambda get-function-configuration \
  --function-name shopfast-product-service-dev \
  --query 'MemorySize'
# Output: 128 (too low!)
```

#### Root Cause

**File:** `starter_code/lambdas/product-service/template.yaml`
**Lines:** 8-11

```yaml
    # PLANTED ISSUE #1: Memory is too low (128MB) causing slow cold starts (6-8 seconds)
    # Discovery: X-Ray traces show long initialization, Lambda Insights shows high cold start duration
    # Fix: Increase to 512MB or higher - memory affects CPU allocation proportionally
    MemorySize: 128
```

Lambda configured with only 128MB memory, causing slow cold starts and memory pressure.

#### Fix

**Edit the file:** `starter_code/lambdas/product-service/template.yaml`

**Change line 11 from:**
```yaml
    MemorySize: 128
```

**To:**
```yaml
    MemorySize: 512
```

#### Deploy Fix

```bash
cd ~/environment/cd14940-troubleshooting-and-optimization-in-aws-for-developers-solution/project/starter_code/lambdas/product-service
sam build

SAM_BUCKET="shopfast-sam-artifacts-$(aws sts get-caller-identity --query Account --output text)"
echo Y | sam sync \
    --stack-name shopfast-lambda \
    --s3-bucket "${SAM_BUCKET}" \
    --no-watch \
    --no-dependency-layer
```

#### Verify Fix

```bash
aws lambda get-function-configuration \
  --function-name shopfast-product-service-dev \
  --query '[MemorySize, Timeout]'
# Expected: [512, 30]
```

#### Screenshot: `Project_Pt_2_screenshot_3.png`
Capture CloudWatch metrics or Logs Insights showing the before/after memory usage and duration improvement.

---

### 2.4 Planted Issue #3: DEBUG Log Level (MVP)

#### Symptoms
- Excessive CloudWatch Logs volume
- High CloudWatch costs
- Log groups filling rapidly

#### Discovery Using Logs Insights

```sql
fields @timestamp, @message
| filter @message like /DEBUG/
| stats count() as debug_logs by bin(1h)
| sort @timestamp desc
```

If you see thousands of DEBUG messages per hour, the log level is misconfigured.

#### Root Cause

**File:** `starter_code/lambdas/product-service/template.yaml`
**Lines:** 21-24

```yaml
        # PLANTED ISSUE #3: Log level set to DEBUG causes excessive logging costs
        # Discovery: CloudWatch Logs showing high volume of debug output
        # Fix: Change to INFO or WARN for production
        LOG_LEVEL: DEBUG
```

#### Fix

**Edit the file:** `starter_code/lambdas/product-service/template.yaml`

**Change line 24 from:**
```yaml
        LOG_LEVEL: DEBUG
```

**To:**
```yaml
        LOG_LEVEL: INFO
```

#### Deploy and Verify

```bash
cd ~/environment/cd14940-troubleshooting-and-optimization-in-aws-for-developers-solution/project/starter_code/lambdas/product-service
sam build

SAM_BUCKET="shopfast-sam-artifacts-$(aws sts get-caller-identity --query Account --output text)"
echo Y | sam sync \
    --stack-name shopfast-lambda \
    --s3-bucket "${SAM_BUCKET}" \
    --no-watch \
    --no-dependency-layer

# Verify
aws lambda get-function-configuration \
  --function-name shopfast-product-service-dev \
  --query 'Environment.Variables.LOG_LEVEL'
# Expected: "INFO"
```

#### Screenshot: `Project_Pt_2_screenshot_4.png`
Capture a Logs Insights query showing the log volume comparison before and after the fix.

---

### 2.5 Planted Issue #4: SNS Message Attribute Missing (MVP)

#### Symptoms
- Order notifications not being sent
- Messages accumulating in Dead Letter Queue (DLQ)
- No errors in publisher Lambda logs

#### Discovery: Inspect DLQ Messages

```bash
# Get the DLQ URL
DLQ_URL=$(aws sqs get-queue-url --queue-name shopfast-product-processing-dlq-dev --query 'QueueUrl' --output text)

# Receive and inspect messages
aws sqs receive-message \
  --queue-url "$DLQ_URL" \
  --message-attribute-names All \
  --max-number-of-messages 5
```

#### Root Cause

**File:** `starter_code/lambdas/notification-handler/template.yaml`
**Lines:** 28-39

The notification handler template has a filter policy requiring `eventType` attribute:

```yaml
        FilterPolicy:
          eventType:
            - order.created
            - order.shipped
            - order.delivered
```

But the publisher Lambda is not including this attribute when publishing.

#### Fix

The publisher Lambda must include MessageAttributes when publishing to SNS.

**Before (missing attributes):**
```python
sns_client.publish(
    TopicArn=TOPIC_ARN,
    Message=json.dumps(event_data)
)
```

**After (with required attributes):**
```python
sns_client.publish(
    TopicArn=TOPIC_ARN,
    Message=json.dumps(event_data),
    MessageAttributes={
        'eventType': {
            'DataType': 'String',
            'StringValue': 'order.created'
        }
    }
)
```

#### Screenshot: `Project_Pt_2_screenshot_5.png`
Capture the DLQ message inspection showing messages without the required attribute.

---

### 2.6 Planted Issue #5: EventBridge Rule Mismatch (Stretch Goal)

#### Symptoms
- Events published to EventBridge don't trigger expected targets
- No errors in source Lambda
- Target Lambda never invoked

#### Root Cause

**File:** `bootstrap_scripts/templates/messaging.yaml`
**Lines:** 119-133

```yaml
  ProductUpdatedRule:
    Type: AWS::Events::Rule
    Properties:
      Name: !Sub shopfast-product-updated-${Environment}
      ...
      EventPattern:
        source:
          - shopfast.products
        detail-type:
          - ProductEvent  # PLANTED ISSUE: Should be "product.updated"
```

Rule expects `detail-type: "ProductEvent"` but source is sending `detail-type: "product.updated"`.

#### Fix

**Change line 133 from:**
```yaml
          - ProductEvent  # PLANTED ISSUE: Should be "product.updated"
```

**To:**
```yaml
          - product.updated
```

#### Deploy Fix

```bash
cd ~/environment/cd14940-troubleshooting-and-optimization-in-aws-for-developers-solution/project

aws cloudformation update-stack \
  --stack-name shopfast-messaging \
  --template-body file://bootstrap_scripts/templates/messaging.yaml \
  --parameters ParameterKey=Environment,ParameterValue=dev \
  --capabilities CAPABILITY_IAM
```

---

### 2.7 Planted Issue #6: Step Functions Stuck Workflow (Stretch Goal)

#### Symptoms
- Workflow executions show "Running" status indefinitely
- No progress past the "WaitForUpdates" state

#### Discovery

1. Navigate to **Step Functions → State machines → shopfast-product-workflow-dev**
2. Click on a stuck execution
3. Review execution history - will show stuck at "WaitForUpdates" state

#### Root Cause

**File:** `bootstrap_scripts/templates/stepfunctions.yaml`
**Lines:** 151-156

```json
"WaitForUpdates": {
  "Type": "Wait",
  "Comment": "PLANTED ISSUE: Timestamp in far future causes workflow to hang indefinitely. Fix: Use 'Seconds': 30 instead",
  "Timestamp": "2099-01-01T00:00:00Z",
  "Next": "RetryFetchProducts"
}
```

Wait state configured with far-future timestamp (`2099-01-01T00:00:00Z`).

#### Fix

Replace the Timestamp with Seconds:

```json
"WaitForUpdates": {
  "Type": "Wait",
  "Seconds": 30,
  "Next": "RetryFetchProducts"
}
```

---

## Part 3: Optimize Performance and Implement Caching

**Time Estimate**: MVP 45-60 minutes | With Stretch Goals 60-90 minutes

### 3.1 Profile Application Performance (MVP)

#### Objective
Use X-Ray and CloudWatch to identify the slowest operations.

#### Step 1: Analyze X-Ray Traces

1. Navigate to **X-Ray → Traces**
2. Filter traces by `service.name = "shopfast-product-service-dev"`
3. Sort by response time (descending)
4. Click on slow traces to see subsegment breakdown

#### Step 2: Identify Bottlenecks

Look for:
- DynamoDB operations taking >100ms
- External API calls with high latency
- Large response payload serialization times

#### Screenshot: `Project_Pt_3_screenshot_1.png`
Capture an X-Ray trace showing the timing breakdown with the slowest subsegments highlighted.

---

### 3.2 Lambda Right-Sizing (MVP)

#### Objective
Analyze Lambda memory usage and optimize resource allocation.

This was addressed in Issue #2. Verify the fix is in place:

```bash
aws lambda get-function-configuration \
  --function-name shopfast-product-service-dev \
  --query '[MemorySize, Timeout]'
# Expected: [512, 30]
```

#### Analyze Actual Usage After Fix

```sql
-- Run in CloudWatch Logs Insights for /aws/lambda/shopfast-product-service-dev
filter @type = "REPORT"
| stats avg(@maxMemoryUsed) as avg_memory,
        max(@maxMemoryUsed) as max_memory,
        avg(@duration) as avg_duration,
        max(@memorySize) as configured_memory
```

#### Screenshot: `Project_Pt_3_screenshot_2.png`
Capture CloudWatch metrics showing the before/after comparison of memory usage and duration.

---

### 3.3 Implement ElastiCache Integration (MVP)

#### Objective
Integrate with Redis for caching using cache-aside pattern.

> **Note:** This project does not include a pre-deployed ElastiCache cluster. If ElastiCache is available, follow the steps below.

#### Step 1: Get ElastiCache Endpoint (if deployed)

```bash
aws elasticache describe-cache-clusters \
  --cache-cluster-id shopfast-redis-dev \
  --show-cache-node-info \
  --query 'CacheClusters[0].CacheNodes[0].Endpoint'
```

#### Step 2: Update Lambda Configuration

```bash
# Add Redis host to environment variables (replace with actual endpoint)
aws lambda update-function-configuration \
  --function-name shopfast-product-service-dev \
  --environment "Variables={PRODUCTS_TABLE=shopfast-products-dev,ENVIRONMENT=dev,LOG_LEVEL=INFO,REDIS_HOST=your-cache-endpoint.cache.amazonaws.com}"
```

#### Step 3: Add Caching Code to handler.py

Add to `starter_code/lambdas/product-service/handler.py`:

```python
import redis

# Initialize Redis client (outside handler for connection reuse)
redis_host = os.environ.get('REDIS_HOST')
redis_client = None
if redis_host:
    redis_client = redis.Redis(
        host=redis_host,
        port=6379,
        decode_responses=True,
        socket_connect_timeout=5
    )

CACHE_TTL = 300  # 5 minutes

def get_product_cached(product_id):
    """Get product with cache-aside pattern."""
    cache_key = f"product:{product_id}"

    # Try cache first
    if redis_client:
        try:
            cached = redis_client.get(cache_key)
            if cached:
                log_info("Cache HIT", product_id=product_id)
                return json.loads(cached)
        except redis.RedisError as e:
            log_warn("Cache read failed, falling back to database", error=str(e))

    # Cache miss - get from DynamoDB
    log_info("Cache MISS", product_id=product_id)
    response = table.get_item(Key={'id': product_id})
    product = response.get('Item')

    # Store in cache
    if redis_client and product:
        try:
            redis_client.setex(cache_key, CACHE_TTL, json.dumps(product, cls=DecimalEncoder))
        except redis.RedisError as e:
            log_warn("Cache write failed", error=str(e))

    return product
```

#### Step 4: Add redis to requirements.txt

Edit `starter_code/lambdas/product-service/requirements.txt`:

```
redis>=4.0.0
```

#### Step 5: Verify Caching Works

```bash
# Invoke function twice with same product
aws lambda invoke --function-name shopfast-product-service-dev \
  --payload '{"httpMethod": "GET", "path": "/products", "pathParameters": {"id": "PROD-001"}}' \
  --cli-binary-format raw-in-base64-out response1.json

aws lambda invoke --function-name shopfast-product-service-dev \
  --payload '{"httpMethod": "GET", "path": "/products", "pathParameters": {"id": "PROD-001"}}' \
  --cli-binary-format raw-in-base64-out response2.json

# Check logs for cache hit/miss
aws logs filter-log-events \
  --log-group-name "/aws/lambda/shopfast-product-service-dev" \
  --filter-pattern '"Cache HIT"' \
  --limit 5
```

#### Screenshot: `Project_Pt_3_screenshot_3.png`
Capture CloudWatch Logs showing "Cache HIT" and "Cache MISS" messages, demonstrating the caching is working.

---

### 3.4 Fix Log Retention (Planted Issue #5)

#### Root Cause

**File:** `starter_code/lambdas/product-service/template.yaml`
**Lines:** 47-50

```yaml
      # PLANTED ISSUE #5: Retention too short (1 day) - logs disappear before debugging
      # Discovery: Historical log queries return no results
      # Fix: Set to 7-14 days for dev environments
      RetentionInDays: 1
```

#### Fix

**Change line 50 from:**
```yaml
      RetentionInDays: 1
```

**To:**
```yaml
      RetentionInDays: 7
```

#### Deploy and Verify

```bash
cd ~/environment/cd14940-troubleshooting-and-optimization-in-aws-for-developers-solution/project/starter_code/lambdas/product-service
sam build

SAM_BUCKET="shopfast-sam-artifacts-$(aws sts get-caller-identity --query Account --output text)"
echo Y | sam sync \
    --stack-name shopfast-lambda \
    --s3-bucket "${SAM_BUCKET}" \
    --no-watch \
    --no-dependency-layer

# Verify log retention
aws logs describe-log-groups \
  --log-group-name-prefix "/aws/lambda/shopfast-product-service-dev" \
  --query 'logGroups[0].retentionInDays'
# Expected: 7
```

---

## Part 4: Configure Monitoring, Alerts, and Health Checks

**Time Estimate**: MVP 30-45 minutes | With Stretch Goals 45-60 minutes

### 4.1 Implement Health Endpoint (MVP)

#### Objective
Create a health check endpoint that verifies at least one dependency.

#### File to Edit
`starter_code/lambdas/product-service/handler.py`

#### Add Health Check Handler

Add this function and update the handler routing:

```python
def health_check(event, context):
    """Health check endpoint with dependency verification."""
    checks = {}

    # Check DynamoDB connectivity
    try:
        table.table_status  # Simple check to verify table is accessible
        checks["database"] = {"status": "ok"}
    except Exception as e:
        checks["database"] = {"status": "error", "message": str(e)}

    # Check Redis connectivity (if configured)
    if redis_client:
        try:
            redis_client.ping()
            checks["cache"] = {"status": "ok"}
        except Exception as e:
            checks["cache"] = {"status": "error", "message": str(e)}

    # Determine overall health
    is_healthy = all(c.get("status") == "ok" for c in checks.values())

    return {
        "statusCode": 200 if is_healthy else 503,
        "headers": get_cors_headers(),
        "body": json.dumps({
            "status": "healthy" if is_healthy else "unhealthy",
            "checks": checks,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        })
    }
```

#### Update Handler Routing

In the `lambda_handler` function, add health check route:

```python
def lambda_handler(event, context):
    path = event.get('path', '')

    # Health check route
    if path == '/health':
        return health_check(event, context)

    # ... rest of routing
```

#### Test the Health Endpoint

```bash
aws lambda invoke \
  --function-name shopfast-product-service-dev \
  --payload '{"httpMethod": "GET", "path": "/health"}' \
  --cli-binary-format raw-in-base64-out \
  health_response.json

cat health_response.json
```

#### Expected Output

```json
{
  "statusCode": 200,
  "body": "{\"status\": \"healthy\", \"checks\": {\"database\": {\"status\": \"ok\"}}, \"timestamp\": \"2026-02-03T16:30:00.000Z\"}"
}
```

#### Screenshot: `Project_Pt_4_screenshot_1.png`
Capture the health endpoint response showing the dependency checks and overall status.

---

### 4.2 Create CloudWatch Alarms (MVP)

#### Objective
Create at least 3 alarms covering different failure scenarios.

#### Alarm 1: Lambda Error Rate

```bash
aws cloudwatch put-metric-alarm \
  --alarm-name "ShopFast-ProductService-Errors" \
  --alarm-description "Alarm when product service errors exceed threshold" \
  --metric-name Errors \
  --namespace AWS/Lambda \
  --dimensions Name=FunctionName,Value=shopfast-product-service-dev \
  --statistic Sum \
  --period 300 \
  --threshold 5 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 2 \
  --treat-missing-data notBreaching
```

#### Alarm 2: Lambda Duration (Timeout Warning)

```bash
aws cloudwatch put-metric-alarm \
  --alarm-name "ShopFast-ProductService-Duration" \
  --alarm-description "Alarm when duration approaches timeout" \
  --metric-name Duration \
  --namespace AWS/Lambda \
  --dimensions Name=FunctionName,Value=shopfast-product-service-dev \
  --statistic Average \
  --period 60 \
  --threshold 25000 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 3 \
  --treat-missing-data notBreaching
```

#### Alarm 3: DynamoDB Throttling

```bash
aws cloudwatch put-metric-alarm \
  --alarm-name "ShopFast-DynamoDB-Throttling" \
  --alarm-description "Alarm when DynamoDB requests are throttled" \
  --metric-name ThrottledRequests \
  --namespace AWS/DynamoDB \
  --dimensions Name=TableName,Value=shopfast-products-dev \
  --statistic Sum \
  --period 60 \
  --threshold 5 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 2 \
  --treat-missing-data notBreaching
```

#### Verify Alarms

```bash
aws cloudwatch describe-alarms \
  --alarm-name-prefix "ShopFast" \
  --query 'MetricAlarms[*].[AlarmName,StateValue]'
```

#### Screenshot: `Project_Pt_4_screenshot_2.png`
Navigate to **CloudWatch → Alarms** and capture a screenshot showing all three alarms with their configurations.

---

### 4.3 Set Up SNS Notifications (MVP)

#### Step 1: Create Notification Topic

```bash
# Create the topic
TOPIC_ARN=$(aws sns create-topic --name shopfast-alerts --query 'TopicArn' --output text)
echo "Topic ARN: $TOPIC_ARN"
```

#### Step 2: Subscribe Email Endpoint

```bash
aws sns subscribe \
  --topic-arn "$TOPIC_ARN" \
  --protocol email \
  --notification-endpoint your-email@example.com
```

**Important**: Check your email and confirm the subscription by clicking the confirmation link.

#### Step 3: Connect Alarms to Topic

Update the alarms to include SNS actions:

```bash
# Get current account ID
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
TOPIC_ARN="arn:aws:sns:us-east-1:${ACCOUNT_ID}:shopfast-alerts"

# Update Error alarm with notification
aws cloudwatch put-metric-alarm \
  --alarm-name "ShopFast-ProductService-Errors" \
  --alarm-description "Alarm when product service errors exceed threshold" \
  --metric-name Errors \
  --namespace AWS/Lambda \
  --dimensions Name=FunctionName,Value=shopfast-product-service-dev \
  --statistic Sum \
  --period 300 \
  --threshold 5 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 2 \
  --alarm-actions "$TOPIC_ARN" \
  --treat-missing-data notBreaching
```

#### Step 4: Test Notification

```bash
aws sns publish \
  --topic-arn "$TOPIC_ARN" \
  --message "Test alert from ShopFast monitoring system" \
  --subject "ShopFast Test Alert"
```

Check your email for the test notification.

#### Screenshot: `Project_Pt_4_screenshot_3.png`
Capture a screenshot of the email notification you received.

---

### 4.4 Composite Alarms (Stretch Goal)

```bash
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
TOPIC_ARN="arn:aws:sns:us-east-1:${ACCOUNT_ID}:shopfast-alerts"

aws cloudwatch put-composite-alarm \
  --alarm-name "ShopFast-Service-Health" \
  --alarm-rule "ALARM(ShopFast-ProductService-Errors) OR ALARM(ShopFast-ProductService-Duration)" \
  --alarm-actions "$TOPIC_ARN" \
  --alarm-description "Composite alarm for overall service health"
```

---

## Quick Reference Tables

### Deployment Commands

| Action | Command |
|--------|---------|
| Navigate to project | `cd ~/environment/cd14940-troubleshooting-and-optimization-in-aws-for-developers-solution/project` |
| Build Lambda | `cd starter_code/lambdas/product-service && sam build` |
| Deploy Lambda | `echo Y \| sam sync --stack-name shopfast-lambda --s3-bucket shopfast-sam-artifacts-$(aws sts get-caller-identity --query Account --output text) --no-watch --no-dependency-layer` |
| Update CloudFormation Stack | `aws cloudformation update-stack --stack-name <name> --template-body file://<template.yaml>` |

### Resource Lookup Commands

| Resource | Command |
|----------|---------|
| Lambda ARN | `aws lambda get-function --function-name shopfast-product-service-dev --query 'Configuration.FunctionArn'` |
| Lambda Config | `aws lambda get-function-configuration --function-name shopfast-product-service-dev --query '[MemorySize, Timeout, TracingConfig.Mode]'` |
| DynamoDB Table | `aws dynamodb describe-table --table-name shopfast-products-dev --query 'Table.TableName'` |
| SNS Topics | `aws sns list-topics --query "Topics[?contains(TopicArn, 'shopfast')]"` |
| SQS Queues | `aws sqs list-queues --queue-name-prefix shopfast` |
| DLQ URL | `aws sqs get-queue-url --queue-name shopfast-product-processing-dlq-dev --query 'QueueUrl' --output text` |
| CloudWatch Alarms | `aws cloudwatch describe-alarms --alarm-name-prefix ShopFast --query 'MetricAlarms[*].AlarmName'` |
| Step Functions | `aws stepfunctions list-state-machines --query "stateMachines[?contains(name, 'shopfast')]"` |

### Common Troubleshooting Commands

| Issue | Command |
|-------|---------|
| Check Lambda errors | `aws logs filter-log-events --log-group-name /aws/lambda/shopfast-product-service-dev --filter-pattern "ERROR" --limit 10` |
| Check function state | `aws lambda get-function --function-name shopfast-product-service-dev --query 'Configuration.State'` |
| View DLQ messages | `aws sqs receive-message --queue-url $(aws sqs get-queue-url --queue-name shopfast-product-processing-dlq-dev --query 'QueueUrl' --output text) --max-number-of-messages 5` |
| Check X-Ray tracing | `aws lambda get-function-configuration --function-name shopfast-product-service-dev --query 'TracingConfig'` |
| List CloudFormation stacks | `aws cloudformation list-stacks --query "StackSummaries[?starts_with(StackName, 'shopfast-')].[StackName,StackStatus]"` |

---

## Verification Checklist

### MVP Requirements Summary

| Part | Requirement | Verification Command |
|------|-------------|---------------------|
| 1.1 | Structured JSON logging | `aws logs filter-log-events --log-group-name /aws/lambda/shopfast-product-service-dev --filter-pattern '{ $.level = * }' --limit 3` |
| 1.2 | X-Ray tracing enabled | `aws lambda get-function-configuration --function-name shopfast-product-service-dev --query TracingConfig` |
| 1.3 | 2+ custom EMF metrics | `aws cloudwatch list-metrics --namespace ShopFast/Application` |
| 1.4 | Operational dashboard | `aws cloudwatch list-dashboards --query "DashboardEntries[?DashboardName=='ShopFast-Operations']"` |
| 2.x | 3+ issues documented | Written documentation with evidence |
| 3.1 | Performance profiled | X-Ray trace analysis screenshots |
| 3.2 | Lambda right-sized | `aws lambda get-function-configuration --function-name shopfast-product-service-dev --query '[MemorySize, Timeout]'` (expect [512, 30]) |
| 3.3 | ElastiCache integrated | Logs showing cache hit/miss |
| 4.1 | Health endpoint | Lambda invoke with `/health` path |
| 4.2 | 3+ CloudWatch alarms | `aws cloudwatch describe-alarms --alarm-name-prefix ShopFast --query 'MetricAlarms[*].AlarmName'` |
| 4.3 | SNS notifications | Email confirmation screenshot |

---

## Submission Reminder

Before submitting, ensure you have:

1. **All screenshots** following the `Project_Pt_X_screenshot_Y.png` naming convention
2. **Documentation** of at least 3 issues with symptoms, root cause, and fix
3. **Code snippets** for key implementations (structured logging, EMF metrics, caching)
4. **Evidence** that fixes resolved the issues (before/after comparisons)
5. **Clear indication** of which stretch goals were attempted (if any)

Good luck!
