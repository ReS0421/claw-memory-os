---
title: Design Review Checklist
---

# System Design Review Checklist

> Verification checklist for when you create or significantly change an operational structure.

## Checklist

### 1. Source of Truth Consistency
- [ ] Does the same information exist in 2+ places?
- [ ] If so, is there 1 source + pointers everywhere else?

### 2. Missing Update Detection
- [ ] If one place is updated and another is missed, can it be detected?
- [ ] Is the detection mechanism automatic or manual?

### 3. Session Read Burden
- [ ] How many files must be read at session start?
- [ ] How many lines to grasp the full structure?

### 4. Folder Role Boundaries
- [ ] Do folder roles overlap?
- [ ] Are there cases where "which folder does this go in?" is ambiguous?

### 5. State vs. Time Axis Separation
- [ ] Is current state visible directly from source-of-truth docs?
- [ ] Have Daily files devolved into state summaries?
- [ ] Have Channels/Tickets become bloated with past history?

### 6. Long-term Memory Quality
- [ ] Does MEMORY.md contain only long-term valid items?
- [ ] Are temporary states, short-term tasks, or unverified ideas mixed in?
- [ ] Are repeatedly valid rules missing?

### 7. Document Freshness
- [ ] Are active documents left stale?
- [ ] Are no-longer-valid documents still in active folders?

### 8. Exception Handling / Recovery
- [ ] Can missed updates be detected?
- [ ] Is there a recovery path when source-of-truth and Daily diverge?
- [ ] Can context still be traced after Archive moves?

### 9. Operational Friction / Maintenance Cost
- [ ] Are manual updates during sessions excessive?
- [ ] Are there bottlenecks that can't be maintained without cron?
- [ ] If so, does cron cover them?

### 10. Discoverability
- [ ] Can "what's the current state?" be found quickly?
- [ ] Can "why did this happen?" be traced within 1-2 steps?
- [ ] Does "where is this rule?" resolve from a consistent location?
