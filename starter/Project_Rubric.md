# Project Rubric: Troubleshoot and Optimize a Multi-Tier AWS Application

## Grading Overview

This project is graded on a **pass/fail** basis.

| Tier | Requirement | Outcome |
|------|-------------|---------|
| **MVP (Required)** | All MVP rubric items must be satisfied | Required to pass |
| **Stretch Goals (Optional)** | Additional criteria for advanced work | Not required to pass; noted in feedback |

---

## Part 1: Implement Comprehensive Observability

### MVP Requirements (Required)

| Criteria | Submission Requirements | Reviewer Tip |
|----------|------------------------|--------------|
| **Structured JSON logging** | Screenshots showing JSON-formatted log entries in CloudWatch Logs for at least one Lambda function. Log entries must include: timestamp, log level, service name, and contextual data. | Verify the log format is valid JSON, not string concatenation. Look for proper field names and consistent structure. |
| **X-Ray tracing on Lambda** | X-Ray service map screenshot showing Lambda functions with active tracing enabled. | Verify traces show Lambda execution details including subsegments for SDK calls. |
| **Custom EMF metrics** | CloudWatch Metrics screenshot showing at least 2 custom metrics appearing in a custom namespace. | Verify metrics are queryable in CloudWatch Metrics console. Check that metric values make sense. |
| **Basic operational dashboard** | Dashboard screenshot showing at least 3 widgets: request/error rates, latency, and one custom metric. | Dashboard should provide at-a-glance visibility into Lambda health. |

### Stretch Goals (Optional)

| Criteria | Submission Requirements | Reviewer Tip |
|----------|------------------------|--------------|
| **Correlation ID propagation** | Screenshots showing correlation ID present in logs across multiple services for the same request. | Check that the same correlation ID appears in Lambda and downstream services. |
| **X-Ray on containers** | Service map showing ECS tasks and/or EKS pods with proper trace segments. | Container traces must show subsegments for outgoing calls (database, HTTP, etc.). |
| **X-Ray annotations/metadata** | X-Ray trace screenshot showing custom annotations (user_id, order_id) and metadata. | Annotations must be visible and searchable. Metadata should contain debugging context. |
| **Trace SNS/SQS flows** | X-Ray traces showing message propagation through SNS/SQS to consumer functions. | Should be able to follow a message from producer to consumer. |
| **Enhanced metrics** | Multiple metric types (4+) with multiple dimensions (2+). | Check dimension cardinality is reasonable. |
| **Enhanced dashboard** | Dashboard with metrics widgets, log insights widgets, and alarm status covering all service layers. | Look for holistic view across compute, data, and integration layers. |

---

## Part 2: Diagnose and Fix Application Issues

### MVP Requirements (Required)

| Criteria | Submission Requirements | Reviewer Tip |
|----------|------------------------|--------------|
| **Logs Insights queries** | At least 2 Logs Insights queries showing error identification. Must include actual queries and explanation of findings. | Queries should use appropriate functions (filter, parse, stats). Simple `fields *` queries do not demonstrate skill. |
| **Lambda debugging** | Documentation of Lambda issue identification using CloudWatch Logs, including error type and stack trace analysis. | Student should demonstrate ability to find specific invocations and correlate with request context. |
| **X-Ray trace analysis** | X-Ray trace screenshot showing analysis of at least one issue, identifying slow or failing operations. | Trace should show timing breakdown. Student should identify which specific operations are problematic. |
| **Container debugging** | Documentation of at least one ECS or EKS issue including logs, root cause, and resolution. | Student must show understanding of why container failed, not just that it failed. |
| **Issue documentation** | Documentation of at least 3 distinct issues with: symptoms, root cause, fix applied, and verification evidence. | Each issue should be clearly different. Fixes must address actual root cause. |
| **Fix verification** | Evidence (logs, metrics, or traces) showing that fixes resolved the identified issues. | Before/after comparison should show measurable improvement. |

### Stretch Goals (Optional)

| Criteria | Submission Requirements | Reviewer Tip |
|----------|------------------------|--------------|
| **ECS task failure analysis** | Documentation including task stopped reason, exit code analysis, and applied fix. | Student must demonstrate understanding of ECS failure modes (OOM, dependency, config). |
| **EKS pod debugging** | kubectl describe output, event analysis, and resolution of scheduling or crash issues. | Look for proper use of kubectl commands and understanding of Kubernetes concepts. |
| **SNS/SQS message flow** | Analysis including DLQ inspection and message format validation. | Should demonstrate understanding of async patterns and failure modes. |
| **EventBridge debugging** | Documentation of rule issue with event pattern analysis and correction. | Show before/after event pattern. Rule correction should be specific and verifiable. |
| **Step Functions debugging** | Execution history showing failed state identification and analysis. | Should show ability to navigate execution history and identify specific failure points. |
| **Log-trace correlation** | Documentation showing correlation of logs with X-Ray traces using correlation ID or request ID. | Must demonstrate actual correlation technique, not just viewing both separately. |

---

## Part 3: Optimize Performance and Implement Caching

### MVP Requirements (Required)

| Criteria | Submission Requirements | Reviewer Tip |
|----------|------------------------|--------------|
| **Performance profiling** | X-Ray traces showing identification of slowest operations/subsegments with quantified latency. | Must identify specific slow operations, not just overall slow traces. |
| **Lambda memory analysis** | CloudWatch metrics showing Lambda duration and memory usage analysis with optimization recommendations. | Recommendations should be data-driven based on actual metrics. |
| **Lambda optimization** | Before/after metrics showing memory adjustment impact on cost or performance. | Memory choice should be justified with data showing cost/performance tradeoff. |
| **ElastiCache integration** | Code snippet and evidence (logs/metrics) showing cache integration working. | Cache operations should be visible in logs or metrics. Verify Redis connection. |
| **Caching pattern** | Documentation of cache-aside pattern implementation with appropriate TTLs. | TTL should be justified. Pattern should be appropriate for the use case. |
| **Cache verification** | Evidence of cache hits/misses (logs or metrics showing caching is active). | Should show measurable cache activity. |

### Stretch Goals (Optional)

| Criteria | Submission Requirements | Reviewer Tip |
|----------|------------------------|--------------|
| **Database query profiling** | DynamoDB consumed capacity or RDS Performance Insights analysis showing slow query identification. | Should show specific query patterns that need optimization. |
| **CloudFront configuration** | Cache behavior settings showing appropriate behaviors for different content types. | Configuration should make sense for content being served. |
| **CloudFront TTLs** | TTL configuration with justification for different content types. | TTLs should be reasonable (not causing excessive misses or stale content). |
| **Cache hit monitoring** | Cache hit rate metrics showing caching effectiveness. | Should show measurable improvement in hit rate or reduced origin requests. |
| **Container optimization** | ECS task definition showing optimized CPU/memory limits with utilization data justification. | Resource limits should match actual utilization with appropriate headroom. |
| **SNS filter policies** | Filter policy JSON showing message filtering logic with evidence of reduced processing. | Filter syntax must be correct. Should filter on appropriate message attributes. |

---

## Part 4: Configure Monitoring, Alerts, and Health Checks

### MVP Requirements (Required)

| Criteria | Submission Requirements | Reviewer Tip |
|----------|------------------------|--------------|
| **Health endpoint** | Curl output or screenshot showing health endpoint response with dependency check. | Health endpoint should check at least one dependency (database or cache), not just return 200 OK. |
| **CloudWatch alarms** | Screenshot showing at least 3 alarms covering different failure scenarios. | Alarms should cover critical failure modes (Lambda errors, Lambda duration, DynamoDB throttling, etc.). |
| **Alarm thresholds** | Alarm configuration showing thresholds with brief justification. | Thresholds should be reasonable, not arbitrary values. |
| **SNS notification topic** | SNS topic with subscription showing alarm notification configuration. | Should demonstrate notification setup connected to alarms. |
| **Notification test** | Confirmation that test notification was received (email screenshot or confirmation). | Verify subscription is confirmed and delivery works. |

### Stretch Goals (Optional)

| Criteria | Submission Requirements | Reviewer Tip |
|----------|------------------------|--------------|
| **Container health probes** | Task definition or pod spec showing liveness and readiness probes with appropriate intervals. | Probe configuration should include reasonable timeout, interval, and failure threshold values. |
| **Composite alarms** | Composite alarm configuration or tiered alerting (warning vs critical). | Should demonstrate understanding of alert fatigue and actionable alerting principles. |
| **EventBridge rules** | EventBridge rule showing event pattern matching for operational events. | Rule should capture meaningful events and integrate with notification workflow. |
| **SLI/SLO dashboard** | Dashboard showing availability, latency, error rate with SLO targets indicated. | SLIs should measure customer-facing service health. Targets should be realistic. |
| **Resource utilization** | Analysis of resource utilization with capacity planning recommendations. | Analysis should be data-driven and consider cost-performance tradeoffs. |

---

## Submission Guidelines

### Required Format

1. **Screenshots** must be clearly legible with relevant portions visible
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
