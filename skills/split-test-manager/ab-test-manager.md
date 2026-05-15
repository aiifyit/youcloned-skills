---
name: split-test-manager
description: "Set up, run, and analyze A/B tests on pages, emails, ads, prices, or offers. Fires when the user wants to test variants — not for reporting on existing performance."
---

# Split Test Manager Skill

Testing is how you find what works. Your job is to set up tests correctly, track them accurately, and call winners based on data — not gut feelings.

## Before Starting

1. Understand what's being tested and why
2. Identify the metric that determines the winner (conversion rate, click rate, revenue per visitor, etc.)
3. Ensure there's enough traffic to get a meaningful result

## Test Types

### Page Tests
- Headline variations
- CTA button text, color, or placement
- Page layout or structure
- Long-form vs. short-form copy
- Video vs. text
- Social proof placement

### Email Tests
- Subject lines (most common and highest impact)
- Send time
- Email length
- CTA placement
- Plain text vs. HTML
- From name

### Ad Tests
- Creative (image/video)
- Headline and primary text
- Audience targeting
- CTA button
- Landing page destination

### Offer Tests
- Price points
- Bonus structure
- Guarantee terms
- Payment plan options

## Setting Up a Test

1. **Define the hypothesis**: "Changing [X] will improve [metric] because [reason]"
2. **Create the variants**:
   - **Control (A)**: The current version
   - **Variant (B)**: The changed version
   - Only change ONE thing per test. Multiple changes = unreadable results.
3. **Set the success metric**: The ONE number that determines the winner
4. **Calculate required sample size**: Use this rough guide:
   - For a 5% baseline conversion rate, you need ~400 visitors per variant to detect a 20% relative improvement
   - For a 20% baseline (like email open rates), you need ~1,000 per variant
   - For small differences, you need more traffic. For big differences, less.
5. **Set the duration**: Run for at least 7 days to account for day-of-week effects, even if you hit sample size earlier
6. **Launch**: Set up the test in the relevant platform

## Monitoring

While the test is running:
- Check daily but don't make changes until the test period ends
- Report current numbers when asked, but caveat with "not statistically significant yet" if applicable
- Watch for outlier days (holidays, technical issues) that could skew results
- If one variant is dramatically worse (50%+ difference), it's OK to call it early

## Calling a Winner

A test has a winner when:
- Both variants have reached minimum sample size
- The test has run for at least 7 days
- There's at least 95% statistical confidence in the result
- The difference is practically meaningful (not just statistically significant)

If the result is a tie (no statistical difference after adequate traffic):
- The simpler version wins (less is more)
- Or keep the original and test something else — this element may not matter much

## Statistical Significance

Simple calculation guide:
- Use a standard proportion z-test
- 95% confidence = p-value < 0.05
- Report results as: "Variant B converted at 4.2% vs. Control A at 3.1%, a 35% relative improvement. This result is statistically significant at 95% confidence."
- If not significant: "Not enough data to declare a winner yet. Need approximately [X] more visitors per variant."

## Reporting

For each active or completed test:
- Test name and hypothesis
- Variants description
- Start date and duration
- Traffic per variant
- Results per variant (metric + confidence level)
- Winner or status (running / winner declared / inconclusive)
- Recommended next test based on results

## Testing Roadmap

Help the user prioritize what to test:
1. **Highest traffic pages first** — more traffic = faster results
2. **Biggest potential impact** — test headlines before button colors
3. **Revenue-closest elements first** — checkout page > blog post
4. **Common priority order**: Headline → Offer/Price → CTA → Page layout → Email subject lines → Ad creative

Maintain a testing backlog with upcoming tests, ranked by potential impact.
