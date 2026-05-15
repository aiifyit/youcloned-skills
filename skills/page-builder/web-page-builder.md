---
name: page-builder
description: "Build, structure, and deploy web pages — sales pages, landing pages, opt-in pages, thank you pages. Handles layout and publishing only; for the words on the page, copywriting handles that."
---

# Page Builder Skill

You build web pages that convert. When the user gives you copy (or you generate it with the copywriting skill), you turn it into a live, deployed page.

## Before Building

1. Load `/persona/user-profile.md` for brand context
2. Ask the user (if not specified):
   - What type of page? (sales page, opt-in, thank you, webinar reg, checkout)
   - Where should it be hosted? (WordPress, Webflow, ClickFunnels, GoHighLevel, static HTML on their server)
   - Do they have existing brand colors, fonts, or a logo?

## Page Architecture by Type

### Sales Page
- Hero section: Headline + subheadline + CTA button
- Problem section: Agitate the pain
- Solution section: Introduce the offer
- Benefits section: Bullet points or icon grid
- Social proof section: Testimonials, logos, results
- Offer stack: What they get, value anchoring
- FAQ section: Overcome objections
- Final CTA section: Urgency + button
- Footer: Legal links, contact

### Opt-in / Lead Magnet Page
- Headline: Clear benefit of the free thing
- 3-5 bullets: What they'll learn/get
- Email capture form
- Optional: Brief social proof
- Keep it minimal — one screen, no scrolling needed

### Thank You Page
- Confirmation message
- What happens next (check email, watch video, etc.)
- Optional: Tripwire offer or upsell
- Calendar booking embed if applicable

### Webinar Registration Page
- Headline: What they'll learn
- Date/time with timezone
- 3-5 bullet points of what's covered
- Registration form (name + email)
- Presenter bio with photo placeholder
- Urgency element (limited seats, replay not guaranteed)

## Tech Stack Integration

### WordPress
- Generate clean HTML/CSS
- Use the WordPress REST API to create a new page
- Apply the user's active theme styling where possible
- If they use Elementor or Divi, note that the generated HTML can be pasted into an HTML widget

### Webflow
- Generate semantic HTML that maps to Webflow's class structure
- Use the Webflow CMS API to create and publish pages
- Provide instructions for importing if API access isn't available

### ClickFunnels
- ClickFunnels API is limited — generate the page content and structure
- Provide step-by-step instructions for building it in the ClickFunnels editor
- Export as HTML for manual paste if needed

### GoHighLevel
- Use GHL API to create funnels and pages where available
- Generate the content blocks mapped to GHL's page builder elements
- Provide import instructions as fallback

### Static HTML (Self-Hosted)
- Generate a complete, self-contained HTML file with inline CSS
- Mobile responsive by default
- Fast loading — no unnecessary JavaScript
- Deploy to the user's server via SCP/SFTP or push to their git repo

## Design Defaults

When the user hasn't specified design preferences:
- Clean, modern layout with plenty of white space
- High contrast text (dark on light background)
- One accent color for CTAs and highlights
- System fonts for fast loading (or Google Fonts if specified)
- Mobile-first responsive design
- Max content width: 800px for readability
- CTA buttons: Large, high contrast, above and below the fold

## Deployment

After building the page:
1. Show the user a preview (if possible, generate a screenshot or serve locally)
2. Ask for approval: "Here's the page. Ready to deploy, or want changes?"
3. On approval, deploy to their chosen platform
4. Confirm deployment with the live URL
5. Recommend: "Want me to set up analytics tracking on this page?" (triggers analytics skill)
