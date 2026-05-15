---
name: email-campaign
description: "Email marketing infrastructure — sequences, automations, broadcasts, list management, and campaign architecture. For writing the actual email copy, copywriting handles that."
---

# Email Campaign Skill

Email is the most valuable asset in a digital business. You manage the user's email marketing — from writing sequences to deploying them, managing lists, and monitoring performance.

## Before Starting

1. Load `/persona/user-profile.md` for voice, audience, and offer context
2. Check which email platform is configured:
   - ConvertKit (Kit) API key in `.env`
   - ActiveCampaign API key in `.env`
   - Mailchimp API key in `.env`
   - Beehiiv API key in `.env`
   - Instantly API key in `.env` (cold outreach only)
3. If no platform is configured, recommend one based on their needs:
   - Solopreneur starting out → ConvertKit (simple, creator-focused)
   - Advanced automations needed → ActiveCampaign
   - Newsletter-focused → Beehiiv
   - Cold outreach → Instantly

## Email Sequence Types

### Welcome Sequence (3-5 emails)
Trigger: New subscriber opts in
- **Email 1** (immediate): Deliver the lead magnet + introduce yourself. Set expectations.
- **Email 2** (Day 1): Share your origin story or a key insight. Build connection.
- **Email 3** (Day 2): Provide value — a quick win, tip, or framework. Demonstrate expertise.
- **Email 4** (Day 3): Social proof — a case study or testimonial. Build trust.
- **Email 5** (Day 4): Soft pitch to the core offer. Bridge from the free content to the paid solution.

### Launch Sequence (7-10 emails over 7-14 days)
- **Pre-launch (3-4 emails)**: Build anticipation, share behind-the-scenes, drop hints
- **Cart open (1 email)**: Announce the offer, full details, clear CTA
- **Social proof (1-2 emails)**: Testimonials, case studies, results
- **FAQ / Objection handling (1 email)**: Address the top 3-5 reasons people don't buy
- **Urgency (1 email)**: Deadline reminder, bonuses expiring, limited spots
- **Last chance (1 email)**: Final email, hard deadline, emotional close

### Nurture Sequence (ongoing)
- Weekly or bi-weekly value emails
- Mix of: stories, lessons, case studies, curated content, behind-the-scenes
- Every 3rd or 4th email includes a soft CTA to an offer
- Goal: Stay top of mind, build authority, warm up for future launches

### Abandoned Cart Sequence (3 emails)
- **Email 1** (1 hour): "Did something go wrong?" — reminder with link back
- **Email 2** (24 hours): Address the #1 objection, add social proof
- **Email 3** (48 hours): Urgency or incentive — limited time discount, bonus, or scarcity

### Re-engagement Sequence (3 emails)
Target: Subscribers who haven't opened in 60+ days
- **Email 1**: "Are you still there?" — curiosity-driven subject line, ask what they need
- **Email 2**: Best content recap — your top 3 pieces of value
- **Email 3**: "Should I remove you?" — unsubscribe prompt (cleans the list, improves deliverability)

### Post-Purchase Sequence (3-5 emails)
- **Email 1** (immediate): Order confirmation + what to do next + access details
- **Email 2** (Day 1): Quick start guide — get them their first win
- **Email 3** (Day 3): Check-in — how's it going? Need help?
- **Email 4** (Day 7): Deeper resource or bonus content
- **Email 5** (Day 14): Ask for a testimonial + introduce the next offer (upsell)

## Writing Emails

For each email, produce:
- **Subject line** + 2 alternates for split testing
- **Preview text** (the snippet that shows in the inbox)
- **Body copy** — written in the user's voice (from profile)
- **CTA** — one clear call to action per email
- **P.S. line** — often the most-read part of the email; use it for urgency or a second hook

Keep emails:
- Short paragraphs (1-3 sentences max)
- Conversational tone (unless user prefers formal)
- Mobile-friendly (no wide images or complex layouts)
- One CTA per email — don't split attention

## Platform Integration

### ConvertKit (Kit)
- Create sequences via API
- Set up tags and automations
- Manage subscribers and segments
- Create forms and landing pages

### ActiveCampaign
- Create automations and campaigns
- Set up deal pipelines (CRM integration)
- Manage tags, lists, and segments
- Set up conditional logic in sequences

### Mailchimp
- Create campaigns and automations
- Manage audiences and segments
- Set up journey builder flows

### Beehiiv
- Create and schedule newsletters
- Manage subscriber growth
- Set up referral programs

### Instantly
- Cold outreach campaigns only
- Multi-account sending setup
- Follow-up sequences
- Lead list management

## List Hygiene

Periodically recommend:
- Removing unengaged subscribers (no opens in 90 days) after re-engagement attempt
- Segmenting by engagement level (active, warm, cold)
- Checking deliverability metrics (open rate, click rate, spam rate, bounce rate)
- If open rates drop below 20%, flag it and recommend a deliverability audit

## Reporting

When asked about email performance:
- Pull metrics from the connected platform API
- Report: open rate, click rate, unsubscribe rate, revenue attributed
- Compare against benchmarks (20%+ open rate is healthy, 2-5% click rate is solid)
- Recommend specific actions based on what the numbers show
