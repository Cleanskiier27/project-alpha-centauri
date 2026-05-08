# 📥 Download Strategy | The 10,000 Milestone Package

This document outlines the systematic procedures for downloading and exporting all artifacts associated with the **10,000 Milestone** and **SBIR Ignite Payout**.

---

## 📦 1. Core Project Download (The 10,000 Package)
To download the complete, production-ready codebase including all Phase 12 deliverables:

### **Command:**
```bash
npm run dist:zip
```
- **Output:** `dist/networkbuster-server-1.0.1.zip`
- **Contents:** `server.js`, `api/`, `web-app/`, `docs/`, `LICENSE`, `README.md`, and the `Plan for the 10,000`.

---

## 🛡️ 2. Security Timeline Export (10,000 Events)
To download the full historical record of the 10,000 security events for audit or AI training:

### **Procedure:**
1. Ensure the timeline service is running: `npm run timeline`.
2. Execute the following export command:
```bash
curl http://localhost:3007/api/timeline/export?format=csv > 10000_security_events.csv
```
- **Alternative:** Use `format=json` for raw data ingestion into the neural pipeline.

---

## 📊 3. Analytical Data Download (The 10,000 Training Core)
To download the KQL-derived datasets required for the Moonbase Alpha expansion and AI training:

### **Procedure:**
Use the Azure CLI to download the performance and visitor metrics from the Log Analytics Workspace:

```powershell
# Export Visitor Behavior Data (10,000+ records)
az monitor log-analytics query \
  --workspace "networkbuster-logs" \
  --analytics-query "ContainerAppConsoleLogs | where TimeGenerated > ago(30d) | take 10000" \
  --out csv > visitor_analytics_10k.csv
```

---

## 💰 4. Financial & Payout Artifacts
To download the certified payout documentation for the SBIR program:

- **Payout Package:** `SBIR-IGNITE-PAYOUT.md`
- **Submission Payload:** `NASA_SBIR_SUBMISSION_PAYLOAD.json`
- **Project Ledger:** `PROJECT_LEDGER.json`

---

## ✅ Download Checklist
- [ ] Run `npm run dist:zip` to package the milestone.
- [ ] Export `10000_security_events.csv` for the audit trail.
- [ ] Download `visitor_analytics_10k.csv` for the AI training core.
- [ ] Verify `PLAN_FOR_10000.md` is included in the final archive.

**Status:** 📥 **DOWNLOAD STRATEGY FINALIZED**
**Reference:** `CHANGELOG.md` | `KQL_ANALYTICS_QUERIES.md` | `README-SECURITY-TIMELINE.md`
