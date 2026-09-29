# Ticket Classification Detailed Guidelines (Reference Material)

This file is supporting material for SKILL.md, for reference when classification boundaries are in doubt.

## 1. Business-line arbitration priority

When a ticket can belong to multiple business lines, arbitrate in the following order (higher priority first):
Fund safety > Regulatory/legal > Core transaction path > User experience > Consultation/advice.

## 2. Common boundary cases

| Ticket description | Assignment | Reason |
| --- | --- | --- |
| Payment succeeded but order status not updated | ORDER (note PAY) | Resolve the order status first; the payment issue is the trigger |
| Invoice title does not match the payer | PAY | Involves invoice-issuance rules; finance-scope |
| Goods received short-shipped; customer requests reshipment | AFTER | It is an after-sales fulfillment issue |
| Refund initiated but not received within 3 days | PAY | Funds-arrival issues belong to the payments line |
| Member points not credited | ACCT | Account-data issue |
| Asks when a new product launches | OTHER | Pure consultation |
| Customer complains about poor agent attitude | OTHER (note complaint) | Complaints go through a separate process |

## 3. Escalation rules (any trigger raises the level by one)

1. The same customer's 3rd ticket of the same type within 30 days;
2. The ticket involves an amount of ≥ CNY 5,000;
3. The issue affects the core transaction path for more than 30 minutes;
4. The customer is a VIP customer with an annual fee of ≥ CNY 100K;
5. Regulatory, legal, or media risk (any incident that could spill over).

## 4. Re-review marks

The following cases must be marked "needs re-review":
- Refund amount exceeding CNY 5,000;
- Payout / compensation-type promises;
- Involves interpretation of contract terms;
- A first-seen abnormal pattern (new system defect).

## 5. QA scoring criteria

QA score = business-line accuracy (40%) + priority accuracy (35%) + note completeness (15%) + format compliance (10%).
Format compliance means strictly following the three-line output in Section 4 of SKILL.md; any extra field incurs a deduction.
