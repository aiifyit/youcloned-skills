---
name: content-delivery
description: "Course and membership platform operations — module access, drip scheduling, student management, and digital product delivery. Not about marketing; about what happens inside the product."
---

# Content Delivery Skill

You manage the delivery side of the user's digital products — making sure customers get what they paid for, content is organized and accessible, and the delivery experience is smooth.

## Before Starting

1. Load `/persona/user-profile.md` for product and offer details
2. Check which delivery platform is configured:
   - Kajabi API
   - Teachable API
3. If neither configured, you can manage content structure and provide instructions for manual setup

## Content Organization

### Course Structure
Help the user organize their content into a logical curriculum:

```
Course Name
├── Module 1: [Foundation Topic]
│   ├── Lesson 1.1: [Introduction/Overview]
│   ├── Lesson 1.2: [Core Concept]
│   ├── Lesson 1.3: [Implementation]
│   └── Action Item / Assignment
├── Module 2: [Next Topic]
│   ├── Lesson 2.1
│   ├── Lesson 2.2
│   └── Action Item / Assignment
├── Bonus Module: [Additional Value]
└── Resources / Downloads
```

Principles:
- Each module = one major topic or skill
- Each lesson = one concept or action (consumable in 10-20 minutes)
- Progressive: each module builds on the previous one
- Action items at the end of each module to drive implementation
- Quick wins early — Module 1 should deliver a tangible result

### Membership Structure
For ongoing membership content:
- Organize by category/topic, not chronologically
- New content clearly flagged as "New"
- Getting Started section always prominent
- Community/discussion area linked
- Monthly content calendar visible to members

## Drip Scheduling

For content that unlocks over time:
- Set release schedule (daily, weekly, or based on enrollment date)
- Configure in the platform API
- Notify students when new content unlocks (email-campaign skill)
- Provide a content calendar so students know what's coming

Drip strategy:
- Courses: Release 1 module per week (prevents overwhelm, maintains engagement)
- Membership: New content monthly or bi-weekly
- Challenge: Daily releases for the challenge duration

## Product Delivery

### Digital Downloads (PDFs, templates, files)
- Host on the delivery platform or a file storage service
- Send download link via email immediately after purchase
- Include in the course dashboard/member area
- Ensure links don't expire (or warn the user if they do)

### Video Content
- Ensure videos are hosted on the platform (not just YouTube links that could go down)
- Check video quality and loading speeds
- Add transcripts for accessibility (can be generated from video)
- Include timestamps for longer videos

## Student/Member Management

Via platform API:
- Enroll new members on purchase (or verify auto-enrollment is working)
- Check member status (active, paused, cancelled, expired)
- Grant or revoke access to specific content
- Handle access issues (can't log in, content not showing)
- Export member data for reporting

## Engagement Tracking

Monitor:
- Course completion rate (what % finish each module)
- Lesson completion rate (where do people drop off)
- Login frequency (how often are members accessing content)
- Community participation (if applicable)

Flag:
- Members who haven't logged in for 14+ days (re-engagement opportunity)
- Modules with high drop-off (content may need improvement)
- Lessons with low completion (may be too long or unclear)

## Content Updates

When the user creates new content or updates existing content:
1. Upload to the platform via API
2. Organize in the correct module/section
3. Set access permissions (all members, specific tiers, drip schedule)
4. Notify relevant members about the new content (email-campaign skill)
5. Update the content index/catalog

## Integration with Other Skills

- **Customer onboarding**: Direct new buyers to their content immediately
- **Customer support**: Answer "where do I find..." questions using platform knowledge
- **Email campaign**: Send engagement emails based on content consumption
- **Analytics reporter**: Track content engagement metrics
