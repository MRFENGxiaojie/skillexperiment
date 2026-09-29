# Kuaibao (Internal Reimbursement System) System Description

## System Overview
- Product: Kuaibao, an internal web-based reimbursement system. Employees submit invoices, approvers approve them.
- Platform: Web browser (desktop-first; some approvers use tablets).
- User roles: employees (reimbursers), approvers (department managers/finance), administrators.
- Launch time: 2 months ago.

## Page Structure

### Home Page (Dashboard)
- Top navigation bar: product logo "Kuaibao" on the left; on the right, 4 **small icons without text labels**: plus sign (new reimbursement), bell (messages), person (personal center), gear (settings).
- Statistics card area: 4 white cards showing "Total monthly reimbursement", "Pending approval", "Approved", and "Rejected" respectively; the cards are display-only and **not clickable**.
- Quick actions area: 4 icon buttons, likewise **icons only with no text**: "Submit reimbursement" (plus icon), "My documents" (document icon), "Invoice center" (invoice icon), "Help" (question mark icon).
- Recent documents list: shows the 10 most recent documents (document number + status badge: pending approval / approved / rejected).

### New Reimbursement Flow (Submit Reimbursement)
1. Home page → click the small icon at the top-right (plus sign, no text label) → enter the "New Reimbursement" page.
2. Fill in the form: reimbursement type (dining / travel / office supplies, etc.), amount, invoice upload, remarks.
3. Click the "Submit" button.
4. **No success message of any kind after submitting** — the page does not change, does not redirect, shows no toast, and the button does not turn gray either — so users generally suspect that "it did not submit successfully".
5. Successfully submitted documents appear in the "My Documents" list, but new documents are not highlighted or otherwise marked, so users have to proactively check.

### Approval Flow
- Approvers receive notification by **email** (there is no approval task list, red dot, or badge indicator inside the system).
- Approval/rejection is notified **only via email**; there is no in-system message notification.
- After a rejection, employees cannot see the rejection reason in the system (the reason is only written in the email body, and some of those emails are treated as spam).

## Common Tasks
1. Submit a dining reimbursement
2. Check approval progress
3. Modify an already-submitted document (currently requires contacting the administrator for manual modification; there is no self-service entry point)

## Known Problem Signals
- Customer service receives a large number of help requests every week such as "can't find the submit button" and "don't know which step the reimbursement is at".
- See user-feedback.md for details of user feedback; see the screenshots/ directory for text descriptions of interface screenshots.