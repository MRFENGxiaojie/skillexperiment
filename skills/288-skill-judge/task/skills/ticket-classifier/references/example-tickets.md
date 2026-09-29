# Ticket Classification Examples (8 cases: 4 correct + 4 error comparisons)

## Example 1 (correct)

> Ticket content: Payment succeeded in the mobile App, but the order keeps showing "Pending Payment", and the order cannot be found in the App either.
> Classification: ORDER-P1-High
> Explanation: Assign to the order line first, note the payment anomaly; it involves the core transaction path, so P1 High.

## Example 2 (correct)

> Ticket content: The invoice title needs to be changed from "Individual" to "Company"; the invoice has already been applied for. Can it still be changed?
> Classification: PAY-P2-Low
> Explanation: Invoice issues belong to the payments line; does not involve fund safety, P2 Low.

## Example 3 (correct)

> Ticket content: The received product's outer packaging is intact, but the internal power adapter has an obvious crack and cannot be used.
> Classification: AFTER-P2-Medium
> Explanation: Quality issues belong to after-sales; it affects a single customer's usage but is not urgent, P2; involves a replacement process, medium urgency.

## Example 4 (correct)

> Ticket content: At 2 a.m., a large number of users reported being unable to log in, with the error "account locked"; preliminary judgment links it to tonight's maintenance.
> Classification: ACCT-P0-High
> Explanation: A widespread failure is P0; system-level issues are judged directly as High urgency.

## Example 5 (error comparison)

> Ticket content: Forgot password, needs manual reset.
> Classification: ACCT-P1-High (wrong)
> Correct classification: ACCT-P3-Low. Forgot-password should first guide self-service recovery; issues resolvable by self-service do not count as P1.

## Example 6 (error comparison)

> Ticket content: The refund has not arrived after 3 days; asking when it will arrive.
> Classification: AFTER-P1-High (wrong)
> Correct classification: PAY-P2-Medium. Refund-arrival issues belong to the payments line, not after-sales; does not involve safety, P2 Medium.

## Example 7 (error comparison)

> Ticket content: A customer is very dissatisfied with the agent's attitude in the comments and requests to file a complaint.
> Classification: ORDER-P2-Medium (wrong)
> Correct classification: OTHER-P2-Medium (note complaint). Complaints belong to OTHER and go through a separate process.

## Example 8 (error comparison)

> Ticket content: A VIP customer reports not receiving promotional SMS, suspecting they have been blacklisted.
> Classification: OTHER-P2-Low (wrong)
> Correct classification: ACCT-P1-Medium. Account push-status issues belong to the account line; any VIP-customer ticket is escalated to P1.
