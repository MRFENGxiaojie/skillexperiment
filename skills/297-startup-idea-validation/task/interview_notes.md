# Accountant interview notes (8 interviewees, June 2026)

> Background: exploratory interviews around the idea of building AI agents for small and medium accounting firms that automatically handle the reconciliation of customers' bank-statement flows. All were verbal exchanges (phone/WeChat), with no paid commitment. Excerpts of the original quotes follow.

## 1. Accountant Wang (Hangzhou, 2-person small firm, mainly bookkeeping)
"We do reconciliation for every client every month, and it is genuinely annoying, especially for the ones with lots of transactions. But let me be honest with you: out of ten flows clients send us, eight are incomplete - missing banks, missing months. Before we even receive payment we spend a lot of time chasing clients for materials. If you are really going to build a tool, get the collection step right first; the reconciliation itself is not that hard."
"Fees? We charge clients CNY 6,000 to 9,000 a year for bookkeeping, and CNY 12,000 for clients with lots of transactions. For me to pay for a tool out of pocket, CNY 200-300 a month is the absolute ceiling; above CNY 500 I would have to think about it."
"We also use Excel macros ourselves. We have tried several of those cloud accounting software products on the market - they are all too dumb, and I still have to keep an eye on them myself."

## 2. Accountant Li (Suzhou, 5-person firm, some audit work)
"Bank statements not matching the books is extremely common - uncleared items, fees not booked, reversals; it happens all year round. If AI could classify these automatically and produce a draft, our re-checking would be much faster."
"But what I worry about most is liability for errors. In this line of work, if we make a mistake we are held responsible. If the software says it is fine, do we dare sign? So in the end a human has to look at it. If it can tell me 'why this entry was matched this way' and give a reasoned explanation, then I can trust it."
"Price? Our audit fees are high, so a pricier tool is acceptable. A few thousand CNY a year is negotiable, but it must save us headcount; otherwise I might as well hire someone."

## 3. Accountant Chen (Fuzhou, sole-proprietor bookkeeping, serving 40+ small and micro businesses)
"I have 40+ clients, and it is basically all flow reconciliation plus tax filing. Around the end of each month I am on a continuous treadmill - I do not even have time to eat."
"Honestly, I do not even have time to organize the raw data. If you make me re-enter everything into a new system, I would rather spend two extra days on the old way. It has to be direct import, direct reconciliation, one-stop, or I will not use it."
"Spend money? I do this for a living. Do not talk to me about subscriptions. I do not have much profit in a year; if the tool is expensive, I will just make do with Excel myself."

## 4. Accountant Zhao (Chengdu, 8-person firm, focused on high-tech enterprises and export-tax refunds)
"Among our clients, e-commerce and foreign-trade flows are especially heavy - large volumes, thousands of entries a month. Doing it by hand, you genuinely cannot finish. We actually sample: we reconcile 30% and rely on balancing for the rest."
"Fully automatic AI reconciliation is genuinely attractive for high-volume firms like ours. It could save roughly... conservatively, 3-4 person-days a month."
"But I have heard that large models confidently make things up about numbers. One wrong entry in an amount is an incident. If you build this, start with 'flag only, don't replace' - a human still reviews the anomalies."
"There is willingness to pay. The firm's annual software budget is about CNY 50,000. For a new tool, I could push for CNY 10,000-20,000 a year."

## 5. Accountant Sun (Qingdao, family workshop, 2-person husband-and-wife shop)
"My husband runs the clients and I do the books. We cannot hire - young people do not want to come to small firms."
"The stuff machines can do, I genuinely want to hand off. I cannot get off work before ten every night."
"But my clients are all small restaurants and small supermarkets with few transactions - a few dozen a month. After AI reconciles them, I could do it by hand in half an hour anyway. Whether your tool is worth it for someone like me, you weigh that yourself."
"Above CNY 300 I basically will not consider it; our fees are low too."

## 6. Accountant Zhou (Shenzhen, 12-person firm, includes Hong Kong business)
"We are currently negotiating with a chain-restaurant client with 12 stores. Each store's bank-statement format is a bit different - just aligning the templates is exhausting."
"What you would be selling is not reconciliation; it is 'reconciliation that needs no person'. Our managing partner calculated that if this client were fully auto-reconciled, it could save us two full-time positions."
"But data security is a big issue. Client flows are sensitive data; you cannot just put them on some cloud tool. It needs to support private deployment, or data that stays in-country. If you can do that, we would be willing to pay more - a few tens of thousands of CNY a year is worth talking about."

## 7. Accountant Wu (Wuhan, 4-person firm, bookkeeping + messy-books cleanup)
"Many of our clients have not had books kept for six months or a year; they come in for a messy-books cleanup first. Those flows are unrecognizable next to the accounts, and there is a pile of bank slips. Can your AI handle that? If it cannot, we do not have much pure-reconciliation work."
"Clients actually do not care what tool you use; they care whether you are cheap and fast. If the tool saves me time, I have time to take more clients. That math I can do."

## 8. Accountant Zheng (Guangzhou, accountant + bookkeeping, solo studio)
"I have used a few AI tools, and honestly they are all mediocre; some are even a trap - importing data alone can hang for a long time."
"What annoys me most about reconciliation is not the reconciling; it is chasing clients to send their bank flows. Clients always drag their feet. If you are going to build something, build the 'remind the client' step - e.g., automatically send clients a WeChat message asking for their flows. That would save me a huge amount of work."
"For payment I am fine with monthly, but: first, it has to work well in the trial; second, do not make me sign an annual contract - I am afraid of being locked in."
