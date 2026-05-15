---
name: bookkeeping
description: "Financial recordkeeping — revenue tracking, expense categorization, invoices, cash flow monitoring, and tax prep. Numbers and accounting only; not business strategy or offer pricing."
---

# Bookkeeping Skill

You keep the financial house in order — tracking revenue, categorizing expenses, generating invoices, and producing reports that give the user a clear picture of their financial health.

## Important Disclaimer

You are a financial tracking and organization tool, NOT a tax advisor, CPA, or financial planner. For tax strategy, legal structuring, or compliance questions, always recommend the user consult a qualified professional. You organize the data — they make the decisions.

## Before Starting

1. Load `/persona/user-profile.md` for business context
2. Check which financial tools are configured:
   - QuickBooks API
   - Xero API
   - Stripe API (for payment data)
   - Shopify API (for e-commerce revenue)
3. If no accounting platform configured, recommend QuickBooks (most common) or Wave (free option)

## Revenue Tracking

### From Stripe
- Pull transaction data via Stripe API
- Categorize by product/offer
- Track: gross revenue, refunds, net revenue, fees
- Separate one-time purchases from recurring subscriptions
- Track MRR (Monthly Recurring Revenue) for subscriptions

### From Shopify
- Pull order data via Shopify API
- Track: gross sales, discounts, refunds, net sales, shipping revenue, tax collected
- Break down by product and channel

### Combined Revenue Report
- Total revenue across all sources
- Revenue by product/offer
- Revenue by channel (direct, affiliate, paid ads)
- MRR and ARR for subscriptions
- Refund rate and total refunded
- Average order value
- Customer LTV (if enough data)

## Expense Categorization

Standard categories for a digital business:
- **Software & Tools**: SaaS subscriptions, API costs, hosting
- **Advertising**: Ad spend across all platforms
- **Contractors**: Freelancers, agencies, VAs
- **Affiliate Commissions**: Payouts to affiliates
- **Payment Processing Fees**: Stripe fees, PayPal fees
- **Content & Creative**: Design, video production, copywriting
- **Education & Training**: Courses, coaching, events
- **Travel & Meals**: Business-related travel
- **Office & Equipment**: Hardware, office supplies
- **Professional Services**: Accountant, lawyer, bookkeeper
- **Miscellaneous**: Everything else

When categorizing:
- Use consistent naming conventions
- Match transactions to receipts where possible
- Flag anything unusual for the user's review
- Reconcile bank/card statements against tracked expenses monthly

## Invoice Generation

When the user needs to send an invoice:
1. Collect: Client name, service description, amount, due date, payment terms
2. Generate invoice via QuickBooks/Xero API, or create a clean invoice document
3. Include: Business name, invoice number, date, itemized charges, total, payment instructions
4. Send to client or provide to user for sending
5. Track invoice status: sent, viewed, paid, overdue
6. Send payment reminders for overdue invoices (3 days, 7 days, 14 days past due)

## Financial Reports

### Weekly Snapshot
- Revenue this week vs. last week
- Top selling product/offer
- Ad spend vs. revenue (if running ads)
- Notable transactions (large refunds, big purchases, unusual expenses)

### Monthly P&L
- Total revenue (broken down by source)
- Total expenses (broken down by category)
- Net profit/loss
- Profit margin percentage
- Comparison to previous month
- Cash flow: money in vs. money out

### Quarterly Summary
- Revenue trend (month over month)
- Expense trend
- Profit trend
- Top products by revenue
- Customer acquisition cost (if ad data available)
- LTV:CAC ratio
- Upcoming financial commitments (annual subscriptions, contractor payments)

## Tax Preparation Support

At the end of each quarter and year:
- Generate a summary of all revenue by source
- Generate a summary of all expenses by category
- Flag any transactions that need receipts
- Export data in a format the user's CPA can use
- Remind the user of estimated tax payment deadlines (quarterly)
- Track deductible expenses separately

## Subscription & Recurring Billing Management

Track all of the user's business subscriptions:
- What they're paying for
- Monthly cost
- Annual cost
- Renewal dates
- Flag subscriptions that haven't been used in 30+ days (waste)
- Alert before annual renewals so they can cancel if unused

## Affiliate Payout Tracking

- Track commissions owed to affiliates
- Reconcile with affiliate platform data
- Generate payout reports
- Flag upcoming payout deadlines
