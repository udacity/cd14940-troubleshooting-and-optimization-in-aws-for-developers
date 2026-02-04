# Submission Guidelines

## Final Submission Content

Your final submission will be a folder containing:
- Your corrected code repository
- Screenshots demonstrating each achieved objective

---

## Screenshot Naming Convention

All screenshots must follow this standardized naming pattern:

```
Project_Pt_X_screenshot_Y.png
```

Where:
- **X** = Part number (1-4)
- **Y** = Screenshot number within that part (sequential)

**Examples**: `Project_Pt_1_screenshot_1.png`, `Project_Pt_2_screenshot_3.png`

---

## Required Screenshots by Part

### Part 1: Implement Comprehensive Observability (4 screenshots)

| Screenshot | Description |
|------------|-------------|
| `Project_Pt_1_screenshot_1.png` | CloudWatch Logs showing log group `/aws/lambda/shopfast-product-service-dev` with JSON structured logs containing `timestamp`, `level`, `service`, `message` fields |
| `Project_Pt_1_screenshot_2.png` | X-Ray service map showing `shopfast-product-service-dev` with active traces and subsegments for SDK calls |
| `Project_Pt_1_screenshot_3.png` | CloudWatch Metrics showing namespace `ShopFast/Application` with at least 2 custom EMF metrics |
| `Project_Pt_1_screenshot_4.png` | "ShopFast MVP Dashboard" with 3+ widgets: invocations/errors, latency, and custom metrics |

### Part 2: Diagnose and Fix Application Issues (4 screenshots)

| Screenshot | Description |
|------------|-------------|
| `Project_Pt_2_screenshot_1.png` | Logs Insights console showing query results with visible query text (must use `filter`, `parse`, or `stats` functions) |
| `Project_Pt_2_screenshot_2.png` | X-Ray trace detail view showing timing breakdown with problematic operation identified |
| `Project_Pt_2_screenshot_3.png` | Before fix evidence (logs/metrics showing errors, high latency, or failures with timestamp) |
| `Project_Pt_2_screenshot_4.png` | After fix evidence showing measurable improvement with later timestamp |

### Part 3: Optimize Performance and Implement Caching (3 screenshots)

| Screenshot | Description |
|------------|-------------|
| `Project_Pt_3_screenshot_1.png` | X-Ray trace showing slowest operations with quantified latency values annotated |
| `Project_Pt_3_screenshot_2.png` | Before/after Lambda Duration metrics showing memory adjustment impact |
| `Project_Pt_3_screenshot_3.png` | CloudWatch Logs showing cache operations (`CACHE_HIT`, `CACHE_MISS`, `CACHE_SET`) |

### Part 4: Configure Monitoring, Alerts, and Health Checks (3 screenshots)

| Screenshot | Description |
|------------|-------------|
| `Project_Pt_4_screenshot_1.png` | Health endpoint response showing dependency status (DynamoDB/Redis connection checks) |
| `Project_Pt_4_screenshot_2.png` | CloudWatch Alarms console showing `ShopFast-dev-ProductService-Errors`, `ShopFast-dev-ProductService-Duration`, `ShopFast-dev-DynamoDB-Throttling` |
| `Project_Pt_4_screenshot_3.png` | Email screenshot showing received alarm notification from SNS |

---

## Stretch Goal Screenshots (Optional)

If you complete stretch goals, continue the screenshot sequence for each part:

| Part | Example Stretch Screenshots |
|------|----------------------------|
| Part 1 | `Project_Pt_1_screenshot_5.png` - Correlation IDs across services |
| Part 2 | `Project_Pt_2_screenshot_5.png` - DLQ message inspection from `shopfast-product-processing-dlq-dev` |
| Part 3 | Additional screenshots for DynamoDB profiling, SNS filter policies, or CloudFront configuration |
| Part 4 | Additional screenshots for EventBridge rules, SLI/SLO dashboard, or composite alarms |

---

## Required Format

1. **Screenshots** must be:
   - Clearly legible with relevant portions visible
   - Following the naming convention above
   - PNG format recommended

2. **Code Repository** must include:
   - All fixes applied to the codebase
   - No broken or incomplete implementations

3. **Documentation** must include:
   - Written explanation of issues found and fixes applied (Part 2)
   - TTL justification for caching strategy (Part 3)
   - Alarm threshold justification (Part 4)

4. **Before/after comparisons** must include:
   - Visible timestamps or version indicators
   - Quantified improvement metrics where applicable

---

## Submission Package

Your final submission should be a single compressed folder containing:

1. **Screenshots folder** - All screenshots organized by part (or in a flat structure with proper naming)
2. **Code repository** - Your corrected codebase with all fixes
3. **Documentation** - Written analysis of issues found, fixes applied, and design decisions
4. **Configuration exports** (optional) - Alarm definitions, filter policies, dashboard JSON, etc.
5. **Stretch goals indicator** - Clear indication of which stretch goals were attempted (if any)

---

## Tips for Success

- **Take screenshots as you work** - Don't wait until the end to capture evidence
- **Include timestamps** - Ensure timestamps are visible in before/after comparisons
- **Annotate where helpful** - Circle or highlight key elements in screenshots
- **Be specific in documentation** - Include exact values, not vague descriptions
- **Test your fixes** - Ensure improvements are measurable before taking final screenshots
