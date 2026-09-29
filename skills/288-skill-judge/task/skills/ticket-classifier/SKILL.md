---
name: ticket-classifier
description: >
  A skill for customer-service ticket classification. Use when the user (the internal customer-service team) needs to classify tickets by business line,
  priority, and urgency for triage or review. May be used together with the classification guide and examples
  under the references/ directory.
---

# Ticket Classification Skill

A ticket-classification process guide for the internal customer-service team. This skill helps agents stably classify tickets into the
correct business lines and priorities, reducing human judgment variance.

## 1. When to use

- When a new ticket needs to be classified before being handled;
- When weekly/monthly reports need ticket volumes counted by business line;
- When judging whether a certain type of ticket should be handed off to another team.

## 2. Classification dimensions

Each ticket needs three fields: **business line**, **priority**, and **urgency**.

### 2.1 Business line

| Business line | Code | Coverage |
| --- | --- | --- |
| Account and login | ACCT | Registration, login, password recovery, account lock |
| Order and logistics | ORDER | Order placement, payment, shipping, logistics tracking, returns and exchanges |
| Payment and invoice | PAY | Payment failure, refunds, invoice issuance and title changes |
| After-sales and warranty | AFTER | Quality issues, repairs, in-warranty replacement |
| Other inquiries | OTHER | Product inquiries, feedback, complaints and suggestions |

### 2.2 Priority (P0-P3)

- **P0**: System-level issues (widespread failures), fund-safety issues, legal or regulatory risk;
- **P1**: Severe single-customer issues (cannot place an order, abnormal deduction, lost order), any VIP-customer ticket;
- **P2**: Routine functional issues that affect a single customer's experience but are not urgent;
- **P3**: Inquiry-type, suggestion-type, or tickets that can be handled later.

### 2.3 Urgency

Urgency = customer impact scope x time sensitivity, divided into three levels: "High / Medium / Low":

1. Impact-scope judgment: the issue affects more than 10 customers / affects the core transaction path -> High;
2. Time-sensitivity judgment: involves funds, shipping deadlines, or regulatory deadlines (e.g. statutory invoice deadlines) -> High;
3. Combined judgment: both High -> High; one High and one Medium -> Medium; otherwise -> Low.

## 3. Classification steps

1. Read the full ticket, first determine which business line it belongs to (compare with the 2.1 table);
2. Identify the issue type: system failure, operation question, or process problem;
3. Determine the priority per 2.2;
4. Determine the urgency per 2.3;
5. Output format: `business-line-priority-urgency`, e.g. `ORDER-P1-High`.

## 4. Output spec

Each classification must output three lines:

```
Business line: ORDER
Priority: P1
Urgency: High
```

Outputting any other irrelevant information is forbidden. If supplementary explanation is needed, put it in a separate "Notes" paragraph.

## 5. Common misclassifications and tips

- Do not assign logistics-timeout tickets directly to ORDER; first confirm whether a third-party carrier is at fault (still ORDER in that case, but note the carrier);
- For "forgot password" tickets, always guide self-service recovery first (help-center link is in the reference material); issues resolvable by self-service do not count as P1;
- For the same customer's third consecutive ticket of the same type, raise the priority one level regardless of content (escalation rule per Section 4 of references/classification-guidelines.md);
- Tickets involving a refund amount over CNY 5,000 must be marked "needs re-review".

## 6. Actions after classification

1. Enter the three classification fields into the ticketing system;
2. If P0, immediately @ the on-duty supervisor in the group and attach the ticket number;
3. If marked "needs re-review", copy the finance review team;
4. Before leaving each day, paste the day's classification results into the team's daily-report template.

## 7. Classification examples

See the 8 examples in references/example-tickets.md (including both correct and incorrect classifications).

## 8. FAQ

### 8.1 What if a ticket involves multiple business lines at once?

Assign to the business line that "first affects the customer's core goal", and note the other business line in the remarks.
For example, "payment failure prevents shipment" is assigned to PAY (resolve the payment first), with ORDER noted in the remarks.

### 8.2 Does an emotional customer affect the priority?

No. Priority is judged only on facts (2.2); emotional issues are handled by the on-duty team lead and do not change the classification result.

### 8.3 What if the customer adds new information after classification?

Re-run the classification steps in Section 3 with the new information, overwrite the original classification, and record "re-classified" in the remarks.

### 8.4 What if the business line cannot be determined?

Refer to the boundary-case table in Section 6 of references/classification-guidelines.md; if still uncertain, assign OTHER and hand it to the on-duty team lead for manual review.

### 8.5 Can priority be adjusted across levels?

Yes, but it must be confirmed by the on-duty team lead, and the adjuster and reason must be recorded in the ticket.

## 9. Quick reference

When you need to apply this process quickly, follow the five steps in Section 3 directly; do not skip steps.
Remember: business line first, then priority, then urgency; the order cannot be reversed.
Strictly follow the output format in Section 4, keeping the field names and examples identical.
Read the tables in 2.1 and 2.2 a few times; classification accuracy will be higher.

## 10. Relationship with QA

The QA team spot-checks 20 classified tickets every month. Common deduction points: missing priority, missing notes,
and business-line boundary misjudgments. This skill's output spec (Section 4) is consistent with the QA criteria; please follow it.
