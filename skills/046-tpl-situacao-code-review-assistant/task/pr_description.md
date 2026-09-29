# PR Description — WeChat Pay channel support

**PR #312** | branch: `feat/wechat-pay` → `main` | ~300 lines changed | CI: green

## Summary

This change adds a WeChat Pay channel to the payment module. It consists of three parts:

1. **Webhook callback handling** (`payment/webhook_handler.py`): adds an entry point for WeChat Pay result notifications; on receiving a callback, updates the corresponding order status to PAID.
2. **Refund API** (`payment/refunds.py`): adds `refund(order_id, amount)` so the operations backend can initiate refunds on paid orders; after a successful refund, sets the order to REFUNDED.
3. **Order state-machine refactor** (`payment/models.py`): extends the order statuses from `created/pending/paid` to `created/pending/paid/refunded/cancelled`, and adds the `mark_paid` / `mark_refunded` methods.

## Supporting changes

- Added a `DELETE /api/payments/:id` route: lets operations cancel an unpaid order.
- `payment/config.py`: added WeChat Pay API configuration.

## Testing & verification

- Local manual verification passed (curl-simulated callback + refund).
- CI is all green.
- No new automated tests added (to be supplemented in a later PR).

## Background

The business team requested enabling WeChat Pay as a collection channel; the Q3 goal is to cover 30% of domestic orders.
