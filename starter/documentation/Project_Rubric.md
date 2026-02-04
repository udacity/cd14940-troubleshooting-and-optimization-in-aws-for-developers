# Project Rubric: Troubleshoot and Optimize a Multi-Tier AWS Application

## Grading Overview

This project is graded on a **pass/fail** basis.

| Tier | Requirement | Outcome |
|------|-------------|---------|
| **MVP (Required)** | All MVP rubric items must be satisfied | Required to pass |
| **Stretch Goals (Optional)** | Additional criteria for advanced work | Not required to pass; noted in feedback |

---

## AWS Resource Names Reference

| Resource Type | Name |
|---------------|------|
| Lambda Functions | `shopfast-product-service-dev`, `shopfast-notification-handler-dev` |
| Dashboard | "ShopFast MVP Dashboard" |
| Metrics Namespace | `ShopFast/Application` |
| DynamoDB Table | `shopfast-products-dev` |
| Step Functions | `shopfast-product-workflow-dev` |
| SNS Topics | `shopfast-product-events-dev`, `shopfast-notifications-dev` |
| SQS DLQ | `shopfast-product-processing-dlq-dev` |
| EventBridge Bus | `shopfast-events-dev` |
| Alarms | `ShopFast-dev-ProductService-Errors`, `ShopFast-dev-ProductService-Duration`, `ShopFast-dev-DynamoDB-Throttling` |
| ElastiCache | `shopfast-redis-dev` |

---

## Part 1: Implement Comprehensive Observability

### MVP Requirements (Required)

| Criteria | Submission Requirements |
|----------|------------------------|
| **Implement structured JSON logging** - At the end of the project, the learner will be able to implement structured JSON logging on Lambda functions in order to enable efficient log analysis in production. | `Project_Pt_1_screenshot_1.png`: CloudWatch Logs showing log group `/aws/lambda/shopfast-product-service-dev` with JSON entries containing `timestamp`, `level`, `service`, `message` fields. |
| **Enable X-Ray distributed tracing** - At the end of the project, the learner will be able to enable X-Ray tracing on Lambda functions in order to visualize request flows and identify bottlenecks. | `Project_Pt_1_screenshot_2.png`: X-Ray service map showing `shopfast-product-service-dev` with active traces and subsegments for SDK calls. |
| **Publish custom EMF metrics** - At the end of the project, the learner will be able to publish custom metrics using EMF in order to track application-specific KPIs. | `Project_Pt_1_screenshot_3.png`: CloudWatch Metrics showing namespace `ShopFast/Application` with at least 2 metrics (e.g., `ProductViews`, `NotificationsSent`). |
| **Create operational dashboard** - At the end of the project, the learner will be able to create a CloudWatch dashboard in order to provide at-a-glance visibility into application health. | `Project_Pt_1_screenshot_4.png`: "ShopFast MVP Dashboard" showing 3+ widgets: invocations/errors, latency, and custom metrics. |

### Stretch Goals (Optional)

| Criteria | Submission Requirements |
|----------|------------------------|
| **Propagate correlation IDs** - At the end of the project, the learner will be able to propagate correlation IDs across services in order to enable cross-service request tracing. | Screenshots showing same correlation ID in API Gateway, `shopfast-product-service-dev`, and `shopfast-notification-handler-dev` logs. |
| **Add X-Ray annotations** - At the end of the project, the learner will be able to add custom X-Ray annotations in order to enable searchable trace filtering. | X-Ray trace screenshot showing custom annotations (`user_id`, `product_id`). |
| **Trace async message flows** - At the end of the project, the learner will be able to trace async message flows in order to debug SNS/SQS processing issues. | X-Ray traces showing `shopfast-product-events-dev` to `shopfast-notification-handler-dev` flow. |
| **Enhanced metrics** | Multiple metric types (4+) with multiple dimensions (2+). |
| **Enhanced dashboard** | Dashboard with metrics widgets, log insights widgets, and alarm status covering all service layers. |

---

## Part 2: Diagnose and Fix Application Issues

### MVP Requirements (Required)

| Criteria | Submission Requirements |
|----------|------------------------|
| **Write Logs Insights queries** - At the end of the project, the learner will be able to write CloudWatch Logs Insights queries in order to identify and analyze errors efficiently. | `Project_Pt_2_screenshot_1.png`: Logs Insights console showing query results with actual query text visible (must use `filter`, `parse`, or `stats` functions). |
| **Debug Lambda functions** - At the end of the project, the learner will be able to debug Lambda errors using CloudWatch Logs in order to identify root causes from stack traces. | Documentation showing error analysis from `/aws/lambda/shopfast-product-service-dev` logs with error type and stack trace. |
| **Analyze X-Ray traces** - At the end of the project, the learner will be able to analyze X-Ray traces in order to identify slow or failing operations. | `Project_Pt_2_screenshot_2.png`: X-Ray trace detail view showing timing breakdown with problematic operation identified. |
| **Debug Step Functions** - At the end of the project, the learner will be able to debug Step Functions workflows in order to identify failed states and understand execution flow. | Documentation showing `shopfast-product-workflow-dev` execution history analysis with failed state identified. |
| **Document issues** - At the end of the project, the learner will be able to document issues with symptoms, root cause, and fixes in order to create maintainable knowledge bases. | Written documentation of 3+ distinct issues with: symptoms, root cause, fix applied, verification evidence. |
| **Verify fixes** - At the end of the project, the learner will be able to verify fixes using metrics and logs in order to ensure production reliability. | `Project_Pt_2_screenshot_3.png` and `Project_Pt_2_screenshot_4.png`: Before/after comparisons showing measurable improvement. |

### Stretch Goals (Optional)

| Criteria | Submission Requirements |
|----------|------------------------|
| **Debug EventBridge rules** - At the end of the project, the learner will be able to debug EventBridge rules in order to fix event routing issues. | Before/after of `shopfast-product-updated-dev` event pattern (fix: "ProductEvent" vs "product.updated"). |
| **Inspect DLQ messages** - At the end of the project, the learner will be able to inspect DLQ messages in order to understand async processing failures. | `Project_Pt_2_screenshot_5.png`: SQS console showing message from `shopfast-product-processing-dlq-dev`. |
| **Step Functions advanced** | Detailed execution history analysis showing state machine debugging across multiple states. |
| **Log-trace correlation** | Documentation showing correlation of logs with X-Ray traces using correlation ID or request ID. |

---

## Part 3: Optimize Performance and Implement Caching

### MVP Requirements (Required)

| Criteria | Submission Requirements |
|----------|------------------------|
| **Profile performance** - At the end of the project, the learner will be able to profile performance using X-Ray traces in order to identify optimization opportunities. | `Project_Pt_3_screenshot_1.png`: X-Ray trace showing slowest operations with quantified latency values. |
| **Analyze Lambda resources** - At the end of the project, the learner will be able to analyze Lambda memory and duration metrics in order to make data-driven optimization decisions. | CloudWatch metrics for `shopfast-product-service-dev` showing Duration and MemoryUsed with analysis. |
| **Optimize Lambda configuration** - At the end of the project, the learner will be able to optimize Lambda memory configuration in order to balance cost and performance. | `Project_Pt_3_screenshot_2.png`: Before/after metrics showing memory adjustment impact with cost/performance justification. |
| **Integrate Redis caching** - At the end of the project, the learner will be able to integrate ElastiCache Redis with Lambda in order to reduce database load and improve response times. | Code snippet showing `shopfast-redis-dev` integration + `Project_Pt_3_screenshot_3.png`: Logs showing cache operations. |
| **Implement cache-aside pattern** - At the end of the project, the learner will be able to implement cache-aside pattern with TTLs in order to balance freshness with performance. | Documentation of caching pattern with TTL justification. |
| **Verify caching** - At the end of the project, the learner will be able to verify caching effectiveness in order to confirm performance improvements. | Logs or metrics showing cache hits/misses from `shopfast-product-service-dev`. |

### Stretch Goals (Optional)

| Criteria | Submission Requirements |
|----------|------------------------|
| **Profile DynamoDB queries** - At the end of the project, the learner will be able to profile DynamoDB queries in order to identify inefficient access patterns. | CloudWatch metrics showing `shopfast-products-dev` consumed capacity. |
| **Configure SNS filter policies** - At the end of the project, the learner will be able to configure SNS filter policies in order to reduce unnecessary Lambda invocations. | Filter policy JSON for `shopfast-product-events-dev` subscription. |
| **CloudFront configuration** | Cache behavior settings showing appropriate behaviors for static content types (HTML, JS, CSS, images). |
| **CloudFront TTLs** | TTL configuration with justification for static content types. |
| **Cache hit monitoring** | Cache hit rate metrics showing caching effectiveness. |

---

## Part 4: Configure Monitoring, Alerts, and Health Checks

### MVP Requirements (Required)

| Criteria | Submission Requirements |
|----------|------------------------|
| **Implement health endpoint** - At the end of the project, the learner will be able to implement a health check endpoint in order to enable proactive monitoring. | `Project_Pt_4_screenshot_1.png`: Lambda invoke output or API response showing health check with dependency status (DynamoDB/Redis). |
| **Configure CloudWatch alarms** - At the end of the project, the learner will be able to configure CloudWatch alarms in order to enable automated incident detection. | `Project_Pt_4_screenshot_2.png`: Alarms console showing `ShopFast-dev-ProductService-Errors`, `ShopFast-dev-ProductService-Duration`, `ShopFast-dev-DynamoDB-Throttling`. |
| **Set alarm thresholds** - At the end of the project, the learner will be able to set appropriate alarm thresholds in order to minimize false positives while catching real issues. | Alarm configuration showing thresholds with brief justification (e.g., >5 errors/5min, >2500ms average). |
| **Configure SNS notifications** - At the end of the project, the learner will be able to configure SNS topics for notifications in order to enable multi-channel alerting. | Screenshot showing `shopfast-notifications-dev` topic with confirmed email subscription. |
| **Test notifications** - At the end of the project, the learner will be able to test notification delivery in order to verify alerting works end-to-end. | `Project_Pt_4_screenshot_3.png`: Email screenshot showing received alarm notification. |

### Stretch Goals (Optional)

| Criteria | Submission Requirements |
|----------|------------------------|
| **Create EventBridge rules for ops events** - At the end of the project, the learner will be able to create EventBridge rules for operational events in order to capture operational events. | EventBridge rule showing pattern for `shopfast-events-dev` bus. |
| **Build SLI/SLO dashboard** - At the end of the project, the learner will be able to build an SLI/SLO dashboard in order to measure customer-facing service health. | Dashboard with availability, latency, error rate with target lines. |
| **Composite alarms** | Composite alarm configuration or tiered alerting (warning vs critical). |
| **Resource utilization** | Analysis of Lambda and DynamoDB resource utilization with capacity planning recommendations. |
