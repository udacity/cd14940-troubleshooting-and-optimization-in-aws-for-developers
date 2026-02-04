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

| Criteria | Submission Requirements | Reviewer Tip |
|----------|------------------------|--------------|
| **Implement structured JSON logging** - At the end of the project, the learner will be able to implement structured JSON logging on Lambda functions in order to enable efficient log analysis in production. | `Project_Pt_1_screenshot_1.png`: CloudWatch Logs showing log group `/aws/lambda/shopfast-product-service-dev` with JSON entries containing `timestamp`, `level`, `service`, `message` fields. | Verify the log format is valid JSON, not string concatenation. Look for proper field names and consistent structure. |
| **Enable X-Ray distributed tracing** - At the end of the project, the learner will be able to enable X-Ray tracing on Lambda functions in order to visualize request flows and identify bottlenecks. | `Project_Pt_1_screenshot_2.png`: X-Ray service map showing `shopfast-product-service-dev` with active traces and subsegments for SDK calls. | Verify traces show Lambda execution details including subsegments for SDK calls. |
| **Publish custom EMF metrics** - At the end of the project, the learner will be able to publish custom metrics using EMF in order to track application-specific KPIs. | `Project_Pt_1_screenshot_3.png`: CloudWatch Metrics showing namespace `ShopFast/Application` with at least 2 metrics (e.g., `ProductViews`, `NotificationsSent`). | Verify metrics are queryable in CloudWatch Metrics console. Check that metric values make sense. |
| **Create operational dashboard** - At the end of the project, the learner will be able to create a CloudWatch dashboard in order to provide at-a-glance visibility into application health. | `Project_Pt_1_screenshot_4.png`: "ShopFast MVP Dashboard" showing 3+ widgets: invocations/errors, latency, and custom metrics. | Dashboard should provide at-a-glance visibility into Lambda health. |

### Stretch Goals (Optional)

| Criteria | Submission Requirements | Reviewer Tip |
|----------|------------------------|--------------|
| **Propagate correlation IDs** - At the end of the project, the learner will be able to propagate correlation IDs across services in order to enable cross-service request tracing. | Screenshots showing same correlation ID in API Gateway, `shopfast-product-service-dev`, and `shopfast-notification-handler-dev` logs. | Check that the same correlation ID appears in API Gateway, Lambda, and downstream services. |
| **Add X-Ray annotations** - At the end of the project, the learner will be able to add custom X-Ray annotations in order to enable searchable trace filtering. | X-Ray trace screenshot showing custom annotations (`user_id`, `product_id`). | Annotations must be visible and searchable. Metadata should contain debugging context. |
| **Trace async message flows** - At the end of the project, the learner will be able to trace async message flows in order to debug SNS/SQS processing issues. | X-Ray traces showing `shopfast-product-events-dev` to `shopfast-notification-handler-dev` flow. | Should be able to follow a message from producer to consumer. |
| **Enhanced metrics** | Multiple metric types (4+) with multiple dimensions (2+). | Check dimension cardinality is reasonable. |
| **Enhanced dashboard** | Dashboard with metrics widgets, log insights widgets, and alarm status covering all service layers. | Look for holistic view across compute, data, and integration layers. |

---

## Part 2: Diagnose and Fix Application Issues

### MVP Requirements (Required)

| Criteria | Submission Requirements | Reviewer Tip |
|----------|------------------------|--------------|
| **Write Logs Insights queries** - At the end of the project, the learner will be able to write CloudWatch Logs Insights queries in order to identify and analyze errors efficiently. | `Project_Pt_2_screenshot_1.png`: Logs Insights console showing query results with actual query text visible (must use `filter`, `parse`, or `stats` functions). | Queries should use appropriate functions (filter, parse, stats). Simple `fields *` queries do not demonstrate skill. |
| **Debug Lambda functions** - At the end of the project, the learner will be able to debug Lambda errors using CloudWatch Logs in order to identify root causes from stack traces. | Documentation showing error analysis from `/aws/lambda/shopfast-product-service-dev` logs with error type and stack trace. | Student should demonstrate ability to find specific invocations and correlate with request context. |
| **Analyze X-Ray traces** - At the end of the project, the learner will be able to analyze X-Ray traces in order to identify slow or failing operations. | `Project_Pt_2_screenshot_2.png`: X-Ray trace detail view showing timing breakdown with problematic operation identified. | Trace should show timing breakdown. Student should identify which specific operations are problematic. |
| **Debug Step Functions** - At the end of the project, the learner will be able to debug Step Functions workflows in order to identify failed states and understand execution flow. | Documentation showing `shopfast-product-workflow-dev` execution history analysis with failed state identified. | Student should demonstrate ability to identify failed states and understand workflow execution flow. |
| **Document issues** - At the end of the project, the learner will be able to document issues with symptoms, root cause, and fixes in order to create maintainable knowledge bases. | Written documentation of 3+ distinct issues with: symptoms, root cause, fix applied, verification evidence. | Each issue should be clearly different. Fixes must address actual root cause. |
| **Verify fixes** - At the end of the project, the learner will be able to verify fixes using metrics and logs in order to ensure production reliability. | `Project_Pt_2_screenshot_3.png` and `Project_Pt_2_screenshot_4.png`: Before/after comparisons showing measurable improvement. | Before/after comparison should show measurable improvement. |

### Stretch Goals (Optional)

| Criteria | Submission Requirements | Reviewer Tip |
|----------|------------------------|--------------|
| **Debug EventBridge rules** - At the end of the project, the learner will be able to debug EventBridge rules in order to fix event routing issues. | Before/after of `shopfast-product-updated-dev` event pattern (fix: "ProductEvent" vs "product.updated"). | Show before/after event pattern. Rule correction should be specific and verifiable. |
| **Inspect DLQ messages** - At the end of the project, the learner will be able to inspect DLQ messages in order to understand async processing failures. | `Project_Pt_2_screenshot_5.png`: SQS console showing message from `shopfast-product-processing-dlq-dev`. | Should demonstrate understanding of async patterns and failure modes. |
| **Step Functions advanced** | Detailed execution history analysis showing state machine debugging across multiple states. | Should show ability to navigate execution history and identify specific failure points. |
| **Log-trace correlation** | Documentation showing correlation of logs with X-Ray traces using correlation ID or request ID. | Must demonstrate actual correlation technique, not just viewing both separately. |

---

## Part 3: Optimize Performance and Implement Caching

### MVP Requirements (Required)

| Criteria | Submission Requirements | Reviewer Tip |
|----------|------------------------|--------------|
| **Profile performance** - At the end of the project, the learner will be able to profile performance using X-Ray traces in order to identify optimization opportunities. | `Project_Pt_3_screenshot_1.png`: X-Ray trace showing slowest operations with quantified latency values. | Must identify specific slow operations, not just overall slow traces. |
| **Analyze Lambda resources** - At the end of the project, the learner will be able to analyze Lambda memory and duration metrics in order to make data-driven optimization decisions. | CloudWatch metrics for `shopfast-product-service-dev` showing Duration and MemoryUsed with analysis. | Recommendations should be data-driven based on actual metrics. |
| **Optimize Lambda configuration** - At the end of the project, the learner will be able to optimize Lambda memory configuration in order to balance cost and performance. | `Project_Pt_3_screenshot_2.png`: Before/after metrics showing memory adjustment impact with cost/performance justification. | Memory choice should be justified with data showing cost/performance tradeoff. |
| **Integrate Redis caching** - At the end of the project, the learner will be able to integrate ElastiCache Redis with Lambda in order to reduce database load and improve response times. | Code snippet showing `shopfast-redis-dev` integration + `Project_Pt_3_screenshot_3.png`: Logs showing cache operations. | Cache operations should be visible in logs or metrics. Verify Redis connection. |
| **Implement cache-aside pattern** - At the end of the project, the learner will be able to implement cache-aside pattern with TTLs in order to balance freshness with performance. | Documentation of caching pattern with TTL justification. | TTL should be justified. Pattern should be appropriate for the use case. |
| **Verify caching** - At the end of the project, the learner will be able to verify caching effectiveness in order to confirm performance improvements. | Logs or metrics showing cache hits/misses from `shopfast-product-service-dev`. | Should show measurable cache activity. |

### Stretch Goals (Optional)

| Criteria | Submission Requirements | Reviewer Tip |
|----------|------------------------|--------------|
| **Profile DynamoDB queries** - At the end of the project, the learner will be able to profile DynamoDB queries in order to identify inefficient access patterns. | CloudWatch metrics showing `shopfast-products-dev` consumed capacity. | Should show specific query patterns that need optimization. |
| **Configure SNS filter policies** - At the end of the project, the learner will be able to configure SNS filter policies in order to reduce unnecessary Lambda invocations. | Filter policy JSON for `shopfast-product-events-dev` subscription. | Filter syntax must be correct. Should filter on appropriate message attributes. |
| **CloudFront configuration** | Cache behavior settings showing appropriate behaviors for static content types (HTML, JS, CSS, images). | Configuration should make sense for static assets being served. |
| **CloudFront TTLs** | TTL configuration with justification for static content types. | TTLs should be reasonable (not causing excessive misses or stale content). |
| **Cache hit monitoring** | Cache hit rate metrics showing caching effectiveness. | Should show measurable improvement in hit rate or reduced origin requests. |

---

## Part 4: Configure Monitoring, Alerts, and Health Checks

### MVP Requirements (Required)

| Criteria | Submission Requirements | Reviewer Tip |
|----------|------------------------|--------------|
| **Implement health endpoint** - At the end of the project, the learner will be able to implement a health check endpoint in order to enable proactive monitoring. | `Project_Pt_4_screenshot_1.png`: Lambda invoke output or API response showing health check with dependency status (DynamoDB/Redis). | Health endpoint should check at least one dependency (database or cache), not just return 200 OK. |
| **Configure CloudWatch alarms** - At the end of the project, the learner will be able to configure CloudWatch alarms in order to enable automated incident detection. | `Project_Pt_4_screenshot_2.png`: Alarms console showing `ShopFast-dev-ProductService-Errors`, `ShopFast-dev-ProductService-Duration`, `ShopFast-dev-DynamoDB-Throttling`. | Alarms should cover critical failure modes (Lambda errors, Lambda duration, DynamoDB throttling, etc.). |
| **Set alarm thresholds** - At the end of the project, the learner will be able to set appropriate alarm thresholds in order to minimize false positives while catching real issues. | Alarm configuration showing thresholds with brief justification (e.g., >5 errors/5min, >2500ms average). | Thresholds should be reasonable, not arbitrary values. |
| **Configure SNS notifications** - At the end of the project, the learner will be able to configure SNS topics for notifications in order to enable multi-channel alerting. | Screenshot showing `shopfast-notifications-dev` topic with confirmed email subscription. | Should demonstrate notification setup connected to alarms. |
| **Test notifications** - At the end of the project, the learner will be able to test notification delivery in order to verify alerting works end-to-end. | `Project_Pt_4_screenshot_3.png`: Email screenshot showing received alarm notification. | Verify subscription is confirmed and delivery works. |

### Stretch Goals (Optional)

| Criteria | Submission Requirements | Reviewer Tip |
|----------|------------------------|--------------|
| **Create EventBridge rules for ops events** - At the end of the project, the learner will be able to create EventBridge rules for operational events in order to capture operational events. | EventBridge rule showing pattern for `shopfast-events-dev` bus. | Rule should capture meaningful events and integrate with notification workflow. |
| **Build SLI/SLO dashboard** - At the end of the project, the learner will be able to build an SLI/SLO dashboard in order to measure customer-facing service health. | Dashboard with availability, latency, error rate with target lines. | SLIs should measure customer-facing service health. Targets should be realistic. |
| **Composite alarms** | Composite alarm configuration or tiered alerting (warning vs critical). | Should demonstrate understanding of alert fatigue and actionable alerting principles. |
| **Resource utilization** | Analysis of Lambda and DynamoDB resource utilization with capacity planning recommendations. | Analysis should be data-driven and consider cost-performance tradeoffs. |

---

## Submission Guidelines

### Screenshot Naming Convention

All screenshots must follow this standardized naming pattern:

```
Project_Pt_X_screenshot_Y.png
```

Where:
- **X** = Part number (1-4)
- **Y** = Screenshot number within that part (sequential)

**Examples**: `Project_Pt_1_screenshot_1.png`, `Project_Pt_2_screenshot_3.png`

#### Required Screenshots by Part

| Part | Screenshot | Description |
|------|------------|-------------|
| 1 | `Project_Pt_1_screenshot_1.png` | CloudWatch Logs showing log group `/aws/lambda/shopfast-product-service-dev` with JSON structured logs |
| 1 | `Project_Pt_1_screenshot_2.png` | X-Ray service map showing `shopfast-product-service-dev` with active traces |
| 1 | `Project_Pt_1_screenshot_3.png` | CloudWatch Metrics showing namespace `ShopFast/Application` with custom EMF metrics |
| 1 | `Project_Pt_1_screenshot_4.png` | "ShopFast MVP Dashboard" with 3+ widgets |
| 2 | `Project_Pt_2_screenshot_1.png` | Logs Insights query results with visible query text |
| 2 | `Project_Pt_2_screenshot_2.png` | X-Ray trace detail showing timing breakdown |
| 2 | `Project_Pt_2_screenshot_3.png` | Before fix evidence (logs/metrics) |
| 2 | `Project_Pt_2_screenshot_4.png` | After fix evidence showing improvement |
| 2 | `Project_Pt_2_screenshot_5.png` | DLQ message inspection from `shopfast-product-processing-dlq-dev` (stretch) |
| 3 | `Project_Pt_3_screenshot_1.png` | X-Ray trace with performance bottlenecks identified |
| 3 | `Project_Pt_3_screenshot_2.png` | Lambda memory optimization before/after comparison |
| 3 | `Project_Pt_3_screenshot_3.png` | ElastiCache integration logs showing cache operations |
| 4 | `Project_Pt_4_screenshot_1.png` | Health endpoint response with dependency status |
| 4 | `Project_Pt_4_screenshot_2.png` | CloudWatch alarms showing `ShopFast-dev-*` alarms |
| 4 | `Project_Pt_4_screenshot_3.png` | SNS notification email received |

Additional screenshots for stretch goals should continue the sequence (e.g., `Project_Pt_1_screenshot_5.png` for Part 1 stretch goal screenshots).

### Required Format

1. **Screenshots** must be clearly legible with relevant portions visible and follow the naming convention above
2. **Code snippets** must be in code blocks or syntax-highlighted
3. **Documentation** must clearly explain what was done and why
4. **Before/after comparisons** must include timestamps or version indicators

### Automatic Fail Conditions

- Plagiarized or copied solutions from other students
- Screenshots from a different AWS account than assigned
- Missing any required MVP deliverable from the checklist
- Evidence of running destructive commands outside project scope
- Solutions that do not address the actual issues (e.g., just increasing timeout without fixing root cause)

### Submission Package

Students should submit a single document or compressed folder containing:
1. All screenshots organized by part (Part 1, Part 2, etc.)
2. Written documentation of issues found and fixes applied
3. Code snippets for key implementations
4. Any exported configurations (alarm definitions, filter policies, etc.)
5. Clear indication of which stretch goals were attempted (if any)

---

## Reviewer Notes

### Time Expectations

| Part | MVP (Required) | With Stretch Goals |
|------|----------------|-------------------|
| Part 1: Observability | 60-75 min | 90-120 min |
| Part 2: Debugging | 60-75 min | 90-120 min |
| Part 3: Optimization | 45-60 min | 60-90 min |
| Part 4: Monitoring | 30-45 min | 45-60 min |
| **Total** | **3-4 hours** | **4-6 hours** |

### Evaluation Process

1. **First**: Verify all MVP requirements are met
   - If any MVP item is missing or inadequate, request revision
   - Be specific about what is missing and reference the rubric criteria

2. **Then**: Review completed stretch goals (if any)
   - Note which stretch goals were completed
   - Provide positive feedback on advanced work
   - Stretch goal gaps do not require revision

### Common Issues to Watch For

**MVP-Level Issues (Require Revision)**
1. **Partial implementations**: Student enables X-Ray on Lambda but not verifying traces
2. **Surface-level fixes**: Increasing timeout without identifying root cause
3. **Missing evidence**: Claims fix worked but no before/after comparison
4. **Insufficient issue count**: Less than 3 documented issues in Part 2
5. **No cache verification**: ElastiCache "integrated" but no evidence it's being used

**Stretch Goal Quality (Feedback Only)**
1. **Missing correlation**: Logs exist but correlation IDs don't propagate
2. **Over-caching**: Student caches everything without considering cache invalidation
3. **Alert spam**: Too many alarms at too sensitive thresholds

### Providing Feedback

**For MVP Revisions:**
- Be specific about what is missing or incorrect
- Reference the relevant MVP rubric criteria
- Suggest resources from the course lessons for guidance
- Acknowledge what was done correctly

**For Stretch Goal Feedback:**
- Acknowledge the additional effort
- Provide constructive feedback on implementation quality
- Note any particularly impressive work
- Suggest improvements without requiring revision

### Sample Feedback Templates

**Passing with MVP Only:**
> Your submission meets all MVP requirements. Your structured logging implementation is well-done, and you clearly documented the issues you found. To go further, consider implementing correlation IDs to make cross-service debugging easier.

**Passing with Stretch Goals:**
> Excellent work! You've completed all MVP requirements and demonstrated advanced competency by completing [X stretch goals]. Your SLI/SLO dashboard shows a strong understanding of production monitoring practices.

**Requires Revision:**
> Your submission is close but needs revision in the following areas:
> - Part 2: Only 2 issues documented (3 required). Please identify and document one additional issue.
> - Part 3: ElastiCache integration shown, but no evidence of cache hits/misses. Please add logs or metrics showing the cache is being used.
