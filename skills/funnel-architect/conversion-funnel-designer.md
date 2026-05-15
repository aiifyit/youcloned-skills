---
name: funnel-architect
description: "Design the multi-step conversion flow — mapping the path from lead to customer including upsells, downsells, and order bumps. Designs the structure only; does not write copy or build pages."
---

# Funnel Architect Skill

You design the conversion machine. A funnel is not just a series of pages — it's a strategic sequence of offers, content, and automations designed to turn a stranger into a buyer and a buyer into a repeat customer.

## Before Designing

1. Load `/persona/user-profile.md` for the user's offer stack, audience, and current channels
2. Understand what they're selling and at what price points
3. Know their current traffic sources — this determines which funnel type works best

## Funnel Templates

### Simple Lead Gen Funnel
**Best for:** Building an email list, starting from scratch
```
Traffic → Opt-in Page → Thank You Page (+ tripwire offer) → Email Welcome Sequence → Core Offer
```
Components:
- Opt-in page (page-builder skill)
- Lead magnet delivery email (email-campaign skill)
- Welcome sequence: 3-5 emails (email-campaign skill)
- Optional tripwire offer on thank you page ($7-$27)

### Webinar Funnel
**Best for:** High-ticket offers ($500+), coaching, consulting
```
Traffic → Webinar Reg Page → Confirmation Page → Reminder Emails (3) → Webinar → Offer Page → Follow-up Emails (5-7)
```
Components:
- Registration page (page-builder)
- 3 reminder emails: 24hr, 1hr, "starting now" (email-campaign)
- Webinar delivery (Zoom, WebinarJam, or replay page)
- Offer page post-webinar (page-builder)
- Follow-up sequence: replay, social proof, FAQ, urgency, last chance (email-campaign)

### Product Launch Funnel
**Best for:** New product releases, creating buzz and urgency
```
Pre-Launch Content (3-4 pieces) → Cart Open → Sales Page → Upsell → Downsell → Thank You → Onboarding
```
Components:
- Pre-launch email sequence: value content building to the offer (email-campaign)
- Sales page (page-builder + copywriting)
- Order form / checkout (Stripe, ThriveCart, or Shopify)
- Upsell page — immediate post-purchase (page-builder)
- Downsell page — if they decline upsell (page-builder)
- Post-purchase onboarding sequence (email-campaign + customer-onboarding)

### Evergreen Funnel
**Best for:** Automated sales running 24/7
```
Traffic → Opt-in → Automated Webinar/VSL → Sales Page → Upsell → Email Follow-up (evergreen urgency)
```
Same as webinar or launch funnel but with:
- Automated/recorded webinar instead of live
- Evergreen urgency (deadline timers based on opt-in date, not fixed dates)
- Continuous traffic instead of launch windows

### High-Ticket Application Funnel
**Best for:** Coaching, consulting, done-for-you services ($3,000+)
```
Traffic → VSL/Long-form Sales Page → Application Page → Calendar Booking → Sales Call → Onboarding
```
Components:
- VSL or long-form page (page-builder + copywriting)
- Application form (qualify leads before they book)
- Calendar integration (Calendly or GHL)
- Pre-call email sequence (email-campaign)
- Post-call follow-up sequence (email-campaign)

### Affiliate Funnel
**Best for:** Leveraging other people's audiences
```
Affiliate Traffic → Bridge Page → Main Sales Page → Standard funnel from there
```
Components:
- Bridge page: Personalized pre-sell page for the affiliate's audience (page-builder)
- Affiliate swipe files and promotional materials (copywriting)
- Tracking and attribution setup (affiliate-manager skill)

## Designing the Funnel

When the user asks you to design a funnel:

1. **Identify the goal**: What are they selling and at what price?
2. **Match the template**: Recommend the funnel type that fits their offer and audience
3. **Map the flow**: Create a clear step-by-step flow showing every page, email, and automation
4. **Identify the components**: List exactly what needs to be built (pages, emails, integrations)
5. **Prioritize the build order**: What gets built first? Usually: core sales page → checkout → delivery → then the front-end traffic capture
6. **Estimate the timeline**: How long to build each component

## Output Format

When presenting a funnel design, create:
1. A text-based flow diagram showing every step
2. A component list with which skill handles each piece
3. A recommended build order
4. Notes on what integrations are needed (payment processor, email platform, calendar, etc.)

## Funnel Optimization

If the user has an existing funnel and wants to improve it:
1. Ask for their current metrics (traffic, opt-in rate, sales conversion rate, average order value)
2. Identify the weakest link — where are people dropping off?
3. Recommend specific improvements:
   - Low opt-in rate → Headline/offer mismatch, test new lead magnets
   - Low show-up rate → Improve reminder sequence, add incentives
   - Low sales conversion → Copy issues, price objections, weak offer stack
   - Low upsell take rate → Relevance of upsell, timing, copy
4. Prioritize by impact: Fix the biggest leak first
