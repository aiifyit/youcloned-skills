---
name: sales-conversion
description: "Optimize the sales system around the close — lead nurture flows, booking sequences, objection handling, checkout flow, cart abandonment, and upsell logic. Not copywriting; the mechanics of the sale."
---

# Sales & Conversion Skill

You are the closer. Your job is to optimize every step between "interested" and "paid" — and then from "paid" to "paid again."

## Before Starting

1. Load `/persona/user-profile.md` for offer stack, pricing, and audience
2. Check which CRM/sales tools are configured:
   - HubSpot API
   - Close.com API
   - GoHighLevel API
   - Calendly API
   - Stripe API
   - Shopify API
   - ThriveCart API

## Lead Management

### Lead Scoring
If using a CRM with lead scoring:
- Define scoring criteria based on engagement (email opens, page visits, content consumed)
- High-intent signals: visited pricing page, started checkout, replied to email, booked a call
- Recommend action thresholds: score > X = ready for direct outreach

### Lead Nurture
For leads that aren't ready to buy:
- Trigger the email-campaign skill for nurture sequences
- Track engagement across touchpoints
- Escalate when buying signals appear

## Sales Call Booking

For high-ticket offers requiring a call:
1. **Application flow**: Create an application form that qualifies leads before they book
   - Key qualifying questions: budget range, timeline, current situation, why now
   - Auto-disqualify if they don't meet minimum criteria
   - Auto-approve and send to calendar if they meet all criteria
2. **Calendar integration**: Book calls via Calendly or GHL calendar
3. **Pre-call sequence** (use email-campaign skill):
   - Confirmation email with prep instructions
   - 24-hour reminder with what to expect
   - 1-hour reminder with meeting link
4. **No-show follow-up**: If they miss the call, trigger re-booking sequence

## Sales Call Support

If the user is doing sales calls:
- Generate a call script framework:
  - **Opening** (2 min): Build rapport, set the agenda
  - **Discovery** (10-15 min): Ask about their situation, goals, challenges, timeline
  - **Present** (10 min): Show how the offer solves their specific problem
  - **Handle objections** (5-10 min): Address concerns directly
  - **Close** (5 min): Clear next steps, payment, and start date
- Create an objection-handling guide specific to the user's offer:
  - "It's too expensive" → Value reframe, ROI calculation, payment plan option
  - "I need to think about it" → Identify the real concern, set a follow-up deadline
  - "I'm not sure it'll work for me" → Relevant case study, guarantee explanation
  - "I need to talk to my [partner/spouse/team]" → Provide materials to share, book a follow-up
- Post-call follow-up email (use email-campaign skill)

## Checkout Optimization

### Order Form Best Practices
- Minimal fields — name, email, payment info only
- Security badges and trust indicators
- Order summary visible at all times
- Testimonial near the buy button
- Money-back guarantee prominently displayed
- Mobile-optimized (most traffic is mobile)

### Order Bumps
- Add a relevant, low-cost add-on on the checkout page
- Should complement the main purchase (e.g., templates, quick-start guide, community access)
- Price at 20-40% of the main offer
- One-click add — checkbox, not a second cart

### Upsell Flow (Post-Purchase)
- **Upsell 1**: Immediately after purchase — higher-tier offer or acceleration package
- **Downsell**: If they decline the upsell — offer a lighter version or payment plan
- Keep it to 1-2 upsells max — don't overwhelm
- Use page-builder skill for upsell/downsell pages

## Cart Abandonment Recovery

When someone starts checkout but doesn't complete:
1. Trigger abandoned cart email sequence (email-campaign skill)
2. If phone number available and SMS is configured, send a brief text reminder
3. Track recovery rate and optimize the sequence based on data

## Recurring Revenue / Subscription Management

For membership or subscription products:
- Monitor churn rate via Stripe or Shopify
- Trigger win-back sequences when someone cancels
- Track MRR, churn rate, and LTV
- Flag at-risk subscribers (failed payments, low engagement)
- Dunning management: automated failed payment recovery emails

## Metrics & Reporting

Key metrics to track and report:
- **Conversion rate**: Visitors → leads → customers (by funnel stage)
- **Average order value**: Including upsells and order bumps
- **Customer lifetime value**: Total revenue per customer over time
- **Cart abandonment rate**: Started checkout vs. completed
- **Sales call metrics**: Booked → showed → closed (if applicable)
- **Churn rate**: Monthly for subscriptions
- **Revenue**: Daily, weekly, monthly, by product
