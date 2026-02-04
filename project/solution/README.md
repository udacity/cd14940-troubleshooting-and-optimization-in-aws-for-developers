# ShopFast - MVP Solution Code

This directory contains the **Minimum Viable Product (MVP)** solution that meets all **required** rubric criteria. Students must implement at least this level to pass the project.

## Time Estimate: 3-4 hours

---

## What's Included in MVP

### Part 1: Observability (MVP)

| Requirement | Implementation |
|-------------|---------------|
| Structured JSON logging | Basic JSON format with timestamp, level, service, message |
| X-Ray on Lambda | Enabled via template.yaml (`Tracing: Active`) |
| X-Ray on API Gateway | Enabled via CloudFormation |
| Custom EMF metrics | 2 metrics: ProductViews, NotificationsSent |
| Basic dashboard | 3 widgets: Lambda invocations/errors, API latency, custom metrics |

**NOT included (Stretch Goals):**
- Correlation ID propagation across services
- X-Ray annotations and metadata
- Enhanced metrics with multiple dimensions
- Log Insights widgets on dashboard

### Part 2: Debugging (MVP)

| Requirement | Implementation |
|-------------|---------------|
| Lambda timeout fix | Increased from 3s to 30s |
| Lambda low memory fix | Increased from 128MB to 512MB |
| DEBUG log level fix | Changed LOG_LEVEL from DEBUG to INFO |
| SNS filter fix | Added `eventType` message attribute |
| EventBridge fix | Changed detail-type to "OrderEvent" |

**NOT included (Stretch Goals):**
- API Gateway 504 advanced debugging
- Step Functions detailed analysis
- Log-trace correlation

### Part 3: Optimization (MVP)

| Requirement | Implementation |
|-------------|---------------|
| Lambda right-sizing | Memory optimized to 512MB based on usage |
| Pagination | Added to prevent timeout on large scans |

**NOT included (Stretch Goals):**
- ElastiCache integration
- CloudFront TTL optimization
- SNS filter policies

### Part 4: Monitoring (MVP)

| Requirement | Implementation |
|-------------|---------------|
| Health endpoint | Basic `/health` returning status |
| CloudWatch alarms | 3 alarms: Lambda errors, API 5xx, DynamoDB throttling |
| SNS notifications | Alarms connected to SNS topic |

**NOT included (Stretch Goals):**
- Composite alarms
- SLI/SLO dashboard

---

## Directory Structure

```
solution_code_mvp/
├── README.md                    # This file
├── lambdas/
│   ├── product-service/
│   │   ├── handler.py           # Basic structured logging, EMF metrics
│   │   └── template.yaml        # X-Ray enabled, 30s timeout, 512MB memory
│   ├── order-service/
│   │   ├── handler.py           # Order processing with EventBridge integration
│   │   └── template.yaml        # X-Ray enabled, SNS/EventBridge fixes
│   ├── inventory-service/
│   │   ├── handler.py           # Inventory management
│   │   └── template.yaml        # X-Ray enabled
│   └── notification-handler/
│       ├── handler.py           # Basic structured logging
│       └── template.yaml        # X-Ray enabled
└── observability/
    ├── dashboards/
    │   └── shopfast-dashboard-mvp.json  # 3-widget dashboard
    └── alarms/
        └── shopfast-alarms-mvp.yaml     # 3 critical alarms
```

---

## Deployment

```bash
# Deploy Lambda functions
cd lambdas/product-service && sam build && sam deploy
cd ../order-service && sam build && sam deploy
cd ../inventory-service && sam build && sam deploy
cd ../notification-handler && sam build && sam deploy

# Deploy observability
cd ../../observability
aws cloudwatch put-dashboard --dashboard-name ShopFast-MVP --dashboard-body file://dashboards/shopfast-dashboard-mvp.json
aws cloudformation deploy --template-file alarms/shopfast-alarms-mvp.yaml --stack-name shopfast-alarms
```

---

## Verification Checklist

- [ ] Structured JSON logs visible in CloudWatch Logs
- [ ] X-Ray traces show Lambda and API Gateway
- [ ] Custom metrics appear in ShopFast/Application namespace
- [ ] Dashboard shows 3 widgets
- [ ] All planted issues fixed (no more timeouts, OOM, crashes)
- [ ] 3 CloudWatch alarms configured
- [ ] Health endpoint returns 200

---

## Next Steps: Stretch Goals

To go beyond MVP, see `solution_code_stretch/` for:
- Correlation ID propagation across Lambda functions
- X-Ray annotations and metadata for searchable traces
- ElastiCache integration for caching
- Advanced dashboards with SLI/SLO
- Composite alarms and EventBridge rules
