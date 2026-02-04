# Final Project: Troubleshoot and Optimize a Serverless AWS Application

## Project Overview

### The Challenge

It's 2 AM and your phone is buzzing with alerts. ShopFast, a rapidly growing e-commerce startup, is experiencing their worst nightmare during Black Friday weekend.

**ShopFast** has grown from a small online retailer to processing over 50,000 orders daily. Their engineering team worked around the clock to scale their AWS infrastructure for the holiday rush, but the hastily assembled system is now falling apart. Customers are reporting slow page loads, failed API calls, and missing notifications. The CEO is demanding answers.

As a **Senior DevOps Consultant**, the CTO has brought you in to save their platform. You'll find a serverless application built with Lambda, API Gateway, DynamoDB, and Step Functions. The previous team left minimal documentation, inconsistent logging, and no centralized monitoring.

Your mission? Bring order to chaos. Implement proper observability, identify and fix the issues plaguing the platform, optimize performance, and build production-grade monitoring before the next traffic surge.

### Why This Project Matters

This project puts you in a realistic scenario faced by cloud engineers at companies of all sizes. You will:

- **Implement Observability**: Transform a poorly instrumented application into a fully observable system
- **Debug Under Pressure**: Use logs, metrics, and traces to identify root causes of production issues
- **Optimize for Performance**: Profile bottlenecks and implement caching strategies that reduce latency by 50%+
- **Build for Production**: Create monitoring and alerting that will catch problems before customers do

If you're ready to tackle a real-world challenge, let's begin.

---

## Project Structure

This project is organized into two tiers:

| Tier | Description | Time Estimate |
|------|-------------|---------------|
| **MVP (Required)** | Core tasks that demonstrate fundamental competency | 3-4 hours |
| **Stretch Goals (Optional)** | Advanced tasks for those who want to go deeper | 1-2 additional hours |

**To pass this project, you must complete all MVP requirements.** Stretch goals are optional and provide opportunities to demonstrate advanced skills.

---

## Environment Overview

### Application Architecture

ShopFast's e-commerce platform is built entirely on serverless AWS services:

**Frontend Layer**
- CloudFront distribution serving a React single-page application
- Lambda functions invoked via AWS SDK/CLI

**Application Layer**
- **Product Service**: Lambda functions (Python) serving the product catalog
- **Notification Service**: Lambda function processing SNS/SQS notifications
- **Workflow Service**: Step Functions orchestrating product catalog refresh operations

**Data Layer**
- DynamoDB for product catalog (high-read workload)
- ElastiCache Redis (deployed but not integrated)
- S3 for static assets and product images

**Integration Layer**
- SNS topics for product events and notifications
- SQS queues for async processing with dead-letter queues
- EventBridge for cross-service event routing

### Pre-Deployed Resources

All infrastructure is provisioned and ready. See the **Environment Setup Guide** for:
- Complete resource inventory
- Access credentials and CLI configuration
- Initial verification commands
- Known gaps in the current state

---

## Instructions

### Part 1: Implement Comprehensive Observability

**MVP Time Estimate**: 60-75 minutes | **With Stretch Goals**: 90-120 minutes

#### Situation

The ShopFast engineering team deployed services quickly without proper instrumentation. Lambda functions use basic `print()` statements. There's no distributed tracing, no custom metrics, and no operational dashboards. When issues occur, the team spends hours manually correlating logs across services.

#### Objectives

Transform the under-instrumented application into a fully observable system.

---

### MVP Requirements (Required)

**1. Implement Structured Logging**

Update the logging in Lambda functions to output structured JSON format. Your logs should include:
- Timestamp in ISO 8601 format
- Log level (INFO, WARN, ERROR)
- Service name and function identifier
- Contextual data (request ID, product ID as appropriate)

**2. Enable X-Ray Tracing on Lambda**

Configure X-Ray tracing for core services:
- Enable active tracing on Lambda functions
- Verify traces appear in the X-Ray console

**3. Implement Basic Custom Metrics**

Use CloudWatch Embedded Metric Format (EMF) to publish at least 2 business metrics:
- Product views
- API errors (or similar business metric)

Define at least one dimension (e.g., service name).

**4. Build Basic Operational Dashboard**

Create a CloudWatch dashboard that provides visibility into:
- Request rates and error rates for Lambda functions
- Latency metrics (at minimum P50)
- At least one custom business metric

#### MVP Deliverables

- [ ] Screenshot of structured JSON log output in CloudWatch Logs
- [ ] Screenshot of X-Ray service map showing Lambda functions
- [ ] Screenshot of custom metrics in CloudWatch Metrics console
- [ ] Screenshot of operational dashboard

---

### Stretch Goals (Optional)

**5. Add Correlation ID Propagation**

Implement correlation ID generation and propagation:
- Generate a correlation ID for incoming requests (or extract from headers)
- Pass the correlation ID to all downstream service calls
- Include the correlation ID in all log entries
- Ensure the ID appears in X-Ray traces

**6. X-Ray Advanced Features**

Enhance X-Ray tracing:
- Add custom annotations for filtering (product ID, request type)
- Add metadata for debugging context
- Trace SNS/SQS message flows

**7. Enhanced Custom Metrics**

Expand business metrics coverage:
- Cache hit/miss rates
- DynamoDB consumed capacity
- Additional dimensions (environment, operation type)

**8. Enhanced Dashboard**

Expand the dashboard to include:
- Latency percentiles (P90, P99)
- Log insights widgets
- Alarm status indicators
- Coverage across all service layers

#### Stretch Goal Deliverables

- [ ] Screenshot showing correlation ID propagation across services
- [ ] Screenshot of X-Ray traces with annotations and metadata
- [ ] Screenshot of enhanced dashboard with all widget types

---

### Part 2: Diagnose and Fix Application Issues

**MVP Time Estimate**: 60-75 minutes | **With Stretch Goals**: 90-120 minutes

#### Situation

With observability in place, you can now see what's happening across the platform. Users are reporting:
- Product pages that sometimes take 10+ seconds to load
- API requests that timeout with 504 errors
- Step Functions workflows that hang indefinitely
- Events that don't trigger expected actions

Your job is to find and fix these issues using the observability tools you implemented.

#### Objectives

Use CloudWatch Logs Insights, X-Ray traces, and metrics to identify and fix production issues.

---

### MVP Requirements (Required)

**1. Analyze Logs with CloudWatch Insights**

Write Logs Insights queries to:
- Find error patterns across services
- Identify the most frequent error types
- Track error frequency over time

**2. Debug Lambda Issues**

Use CloudWatch Logs and X-Ray to:
- Identify Lambda functions with high error rates or timeouts
- Analyze at least one timeout issue and its root cause
- Find slow downstream dependencies (DynamoDB throttling, cold starts)

**3. Troubleshoot Step Functions Workflow**

Review the Step Functions execution history to:
- Identify a stuck or failed execution
- Diagnose the root cause (misconfiguration, timeout, etc.)
- Document the issue and resolution

**4. Document and Verify Fixes**

For each issue found:
- Document the symptoms
- Explain the root cause
- Describe the fix applied
- Provide evidence that the fix resolved the issue

Document and fix at least **3 distinct issues** across the platform.

#### MVP Deliverables

- [ ] CloudWatch Logs Insights queries showing identified issues (at least 2 queries)
- [ ] X-Ray trace screenshots showing root cause analysis for at least 1 issue
- [ ] Documentation of 3 issues found: symptoms, root cause, and fix applied
- [ ] Evidence (logs, metrics, or traces) showing fixes resolved the issues

---

### Stretch Goals (Optional)

**5. Debug Service Integration Issues**

Investigate the messaging and orchestration layer:
- Investigate SNS/SQS message flow problems and DLQ contents
- Check EventBridge rule configurations for pattern mismatches
- Review Step Functions execution history for all failed states

**6. Correlate Logs and Traces**

Demonstrate correlation of log entries with X-Ray traces using correlation IDs or request IDs to identify root cause of an issue.

**7. Advanced Lambda Debugging**

Investigate Lambda-specific issues:
- Cold start impact analysis
- Memory and timeout configuration issues
- Provisioned concurrency considerations

#### Stretch Goal Deliverables

- [ ] DLQ message analysis showing failed message inspection
- [ ] EventBridge rule pattern mismatch identification
- [ ] Step Functions execution history showing all failed state identification
- [ ] Documentation showing log-to-trace correlation technique
- [ ] Lambda cold start analysis with recommendations

---

### Part 3: Optimize Performance and Implement Caching

**MVP Time Estimate**: 45-60 minutes | **With Stretch Goals**: 60-90 minutes

#### Situation

With critical issues fixed, the platform is stable but still too slow and expensive. Product pages take 2-3 seconds to load. Lambda functions are misconfigured, causing slow cold starts. The ElastiCache cluster sits idle while every request hits DynamoDB. CloudFront serves API requests without caching.

#### Objectives

Profile, analyze, and optimize the application for better performance.

---

### MVP Requirements (Required)

**1. Profile Application Performance**

Use X-Ray and CloudWatch to:
- Identify the slowest operations in request traces
- Analyze Lambda duration and memory metrics
- Find at least 2 operations that could benefit from optimization

**2. Right-Size Lambda Resources**

Optimize Lambda resource allocation:
- Analyze Lambda memory usage and cold start times
- Determine optimal memory settings based on actual usage
- Document before/after metrics showing improvement or cost savings

**3. Implement Application Caching**

Integrate ElastiCache with the product service:
- Connect to the pre-deployed Redis cluster
- Implement cache-aside pattern for product data
- Set appropriate TTLs
- Verify caching is working (logs or metrics)

#### MVP Deliverables

- [ ] X-Ray trace analysis identifying slowest operations
- [ ] Lambda memory analysis with optimization recommendations and before/after metrics
- [ ] Screenshot or logs showing ElastiCache integration working
- [ ] Evidence of cache hit/miss (logs or metrics)

---

### Stretch Goals (Optional)

**4. Profile Database Query Performance**

Analyze database performance:
- DynamoDB consumed capacity analysis
- Identify throttling events
- Identify specific slow query patterns

**5. Configure Edge Caching**

Optimize CloudFront for static assets:
- Configure cache behaviors for different content types (HTML, JS, CSS, images)
- Set appropriate TTLs for different content types
- Monitor cache hit rates for static content

**6. Optimize Message Routing**

Add SNS filter policies to:
- Route messages only to relevant subscribers
- Reduce unnecessary message processing
- Filter by message attributes

#### Stretch Goal Deliverables

- [ ] Database query performance analysis with throttling identification
- [ ] CloudFront cache behavior configuration with appropriate TTLs for static content
- [ ] Cache hit rate metrics showing improvement
- [ ] SNS subscription filter policy configuration

---

### Part 4: Configure Monitoring, Alerts, and Health Checks

**MVP Time Estimate**: 30-45 minutes | **With Stretch Goals**: 45-60 minutes

#### Situation

The platform is now stable, fast, and cost-optimized. But you need to ensure it stays that way. Currently, there are no health checks, no alarms to catch problems early, and no way to track whether the platform is meeting its service level objectives.

#### Objectives

Implement production-grade monitoring to maintain platform health.

---

### MVP Requirements (Required)

**1. Implement Basic Health Endpoints**

Add health check endpoints that:
- Return meaningful health status (not just 200 OK)
- Check at least one dependency (DynamoDB or cache)

**2. Create Essential CloudWatch Alarms**

Create alarms for critical metrics (at least 3):
- Lambda error rate threshold
- Lambda duration/timeout threshold
- One additional alarm of your choice (DynamoDB throttling, etc.)

**3. Set Up Basic Notifications**

Configure SNS for alerting:
- Create a notification topic
- Subscribe an email endpoint
- Connect alarms to the notification topic
- Test alert delivery

#### MVP Deliverables

- [ ] Health endpoint responses (AWS Lambda invoke output or screenshot)
- [ ] Screenshot showing at least 3 CloudWatch alarms configured
- [ ] SNS notification test confirmation (email received)

---

### Stretch Goals (Optional)

**4. Advanced Alerting**

Implement sophisticated alerting:
- Create composite alarms for service-level health
- Implement tiered alerting (warning vs critical levels)
- Create EventBridge rules for Lambda error events

**5. Build SLI/SLO Dashboard**

Create a dashboard tracking:
- Availability (successful requests / total requests)
- Latency (P99 < target)
- Error rate (errors / total requests)
- Service level indicators with defined targets

**6. Resource Utilization Analysis**

Analyze and document:
- Current resource utilization patterns across services
- Recommendations for capacity planning
- Cost optimization opportunities

#### Stretch Goal Deliverables

- [ ] Composite alarm or tiered alerting configuration
- [ ] EventBridge rule for operational events
- [ ] SLI/SLO monitoring dashboard with defined targets

---

## Helpful Hints

### General Tips

- **Start with exploration**: Before making changes, use the AWS Console to explore the current state of each service
- **Work incrementally**: Implement one change at a time and verify it works before moving on
- **Document as you go**: Take screenshots and notes as you complete each task
- **Use the course materials**: Reference specific lessons for techniques and code examples
- **Check the logs**: CloudWatch Logs is your best friend for debugging
- **Focus on MVP first**: Complete all required tasks before attempting stretch goals

### Part-Specific Hints

**Part 1: Observability**
- AWS Lambda Powertools simplifies structured logging and X-Ray integration
- EMF metrics can be emitted directly from Lambda without API calls
- Remember to enable X-Ray on both the Lambda function AND API Gateway

**Part 2: Debugging**
- Always check the Dead Letter Queue (DLQ) for failed messages
- Step Functions execution history shows exactly where workflows fail
- X-Ray annotations make traces searchable by business identifiers
- Look for DynamoDB throttling (ProvisionedThroughputExceededException)

**Part 3: Optimization**
- Start with the biggest impact optimizations (usually caching)
- Lambda memory directly affects CPU allocation
- CloudFront cache hit ratio should be >80% for static content
- Filter policies on SNS can dramatically reduce unnecessary processing

**Part 4: Monitoring**
- Health checks should verify dependencies, not just return 200
- Composite alarms reduce alert fatigue
- Start with conservative alarm thresholds and adjust based on baselines
- SLOs should be based on customer experience, not arbitrary numbers

---

## Submission Checklist

Before submitting your project, verify you have completed the required items.

### MVP Requirements (All Required to Pass)

#### Part 1: Observability (Required)
- [ ] Structured JSON logging implemented
- [ ] X-Ray tracing enabled on Lambda
- [ ] At least 2 custom EMF metrics published
- [ ] Basic operational dashboard created

#### Part 2: Debugging (Required)
- [ ] At least 2 Logs Insights queries demonstrating issue identification
- [ ] At least 1 X-Ray trace analysis showing root cause
- [ ] 3 distinct issues documented with symptoms, root cause, and fix
- [ ] Evidence showing fixes resolved the issues

#### Part 3: Optimization (Required)
- [ ] Performance bottlenecks identified via X-Ray/CloudWatch
- [ ] Lambda memory analyzed and optimized with before/after metrics
- [ ] ElastiCache integrated with evidence of working cache

#### Part 4: Monitoring (Required)
- [ ] Health endpoint implemented with dependency check
- [ ] At least 3 CloudWatch alarms created
- [ ] SNS notifications configured and tested

---

### Stretch Goals (Optional - For Additional Credit)

#### Part 1: Observability (Optional)
- [ ] Correlation IDs propagating across services
- [ ] X-Ray annotations and metadata
- [ ] Enhanced dashboard with all widget types

#### Part 2: Debugging (Optional)
- [ ] Service integration issues (SNS/SQS/EventBridge/Step Functions) debugged
- [ ] Log-to-trace correlation demonstrated
- [ ] Lambda cold start analysis completed

#### Part 3: Optimization (Optional)
- [ ] Database query performance profiled
- [ ] CloudFront edge caching configured
- [ ] SNS filter policies created

#### Part 4: Monitoring (Optional)
- [ ] Composite or tiered alarms implemented
- [ ] EventBridge rules for operational events
- [ ] SLI/SLO dashboard with targets

---

### Required Artifacts

For all completed work (MVP and any stretch goals):
- [ ] Screenshots for all deliverables listed
- [ ] Documentation of issues found and fixes applied
- [ ] Code snippets or configuration for key implementations
- [ ] Evidence of working solutions (logs, metrics, traces)

---

## Time Summary

| Part | MVP (Required) | With Stretch Goals |
|------|----------------|-------------------|
| Part 1: Observability | 60-75 min | 90-120 min |
| Part 2: Debugging | 60-75 min | 90-120 min |
| Part 3: Optimization | 45-60 min | 60-90 min |
| Part 4: Monitoring | 30-45 min | 45-60 min |
| **Total** | **3-4 hours** | **4-6 hours** |

---

## Evaluation

Your work will be assessed using the rubric provided on the following page. Review the rubric before starting, consult it as you work, and verify all requirements are met before submission.

**Grading**: This project is graded on a **pass/fail** basis.

- **To Pass**: All MVP rubric items must be satisfied
- **Stretch Goals**: Completing stretch goals demonstrates advanced competency but is not required to pass

**Note**: Stretch goal completion will be noted in feedback and may be considered for distinctions or recommendations.
