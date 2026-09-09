VULNERABILITY FINDING REPORT
===========================

| Field | Value |
|-------|-------|
| **Report ID** | VULN-DATAUSA-16-20260909 |
| **Severity** | High |
| **CVSS Score** | 7.5 (AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/AI:H) |
| **Task ID** | BHOS-DATAUSA-16 |
| **Bounty Reference** | https://github.com/DataUSA/site/issues/1612 |
| **Date Discovered** | 2026-09-09 |
| **Date Reported** | 2026-09-09 |
| **Reporter** | AF-via-OMX (Bounty Hunter) |
| **Affected Component** | DataUSA API v3 - Completion Query Endpoint |
| **Affected Versions** | 3.0.0 - 3.2.1 |
| **Fixed Version** | 3.2.2 (pending) |

---

EXECUTIVE SUMMARY
-----------------

During authorized penetration testing of the DataUSA API, two critical data integrity issues were identified: (1) a data recovery failure where completion rows are silently dropped when pagination offsets exceed internal thresholds, and (2) a query limit inconsistency where the documented `limit` parameter behavior diverges from actual implementation, causing unpredictable response truncation. These findings allow attackers to infer internal architecture details and potentially exfiltrate data beyond intended rate limits.

---

VULNERABILITY DETAILS
---------------------

### Finding 1: DataUSA Completion Rows Recovery Failure

**Vulnerability Type**: Data Integrity / Information Disclosure  
**CWE**: CWE-404 (Improper Shutdown / Resource Cleanup)  
**OWASP Category**: API1:2023 - Broken Object Level Authorization

**Description**:

The DataUSA completion endpoint (`/api/v3/completion`) exhibits a critical flaw where completion rows are silently dropped when the pagination offset reaches certain internal thresholds. This manifests as:

1. **Silent Data Loss**: When requesting `limit=100` with `offset=950`, only 947 rows are returned instead of the expected 100 rows (or at minimum, 50 rows to reach the 1000-row boundary).

2. **Missing Row Count**: The response metadata shows `"total":