---
name: voice-and-brand
description: "Review or rewrite existing content to match the user's established brand voice and tone. Called by other skills after content is drafted — not used to create new content from scratch."
---

# Voice & Brand Skill

Every word this agent produces should sound like the user, not like a robot. This skill defines and enforces the user's unique voice across all outputs.

## Voice Profile

The voice profile is built during onboarding and stored in `/persona/user-profile.md` under communication preferences. It captures:

- **Formality level**: Casual / Professional / Somewhere in between
- **Tone**: Warm, direct, funny, authoritative, empathetic, provocative, etc.
- **Vocabulary**: Words they use often, words they'd never use
- **Sentence structure**: Short and punchy? Long and flowing? Mix?
- **Personality**: Are they the straight-shooter? The storyteller? The data nerd? The motivational coach?
- **Swear tolerance**: Do they curse? How much?
- **Emoji/formatting style**: Do they use emojis? Bullet points? Headers?

## Building the Voice Profile

If the voice profile isn't detailed enough, gather more data:

1. **Ask for examples**: "Can you share 3-5 pieces of content you've written that you feel represent your voice well? Emails, social posts, sales pages — anything."
2. **Analyze the examples**: Identify patterns in:
   - Average sentence length
   - Paragraph length
   - Use of questions
   - Use of stories
   - Use of humor
   - Formality level
   - Power words and phrases they gravitate toward
   - How they open and close pieces
3. **Search the RAG**: If the knowledge base has their previous content, analyze it for voice patterns
4. **Create a voice reference sheet**: Save to `/persona/voice-guide.md`

## Voice Reference Sheet Format

```markdown
# [User Name]'s Brand Voice Guide

## In One Sentence
[How they sound in one sentence — e.g., "Like a smart friend who's been through it and gives you the straight truth over a beer."]

## Tone Attributes
- [Attribute 1]: [Description] — e.g., "Direct: Says what they mean without hedging"
- [Attribute 2]: [Description]
- [Attribute 3]: [Description]

## Do's
- [Things that sound like them]
- [Phrases they love]
- [Structures they use]

## Don'ts
- [Things that DON'T sound like them]
- [Corporate jargon to avoid]
- [Clichés they hate]

## Example Sentences
- In their voice: "[example]"
- NOT in their voice: "[contrasting example]"

## Platform Adjustments
- Email: [How they adjust for email]
- Social: [How they adjust for social]
- Sales pages: [How they adjust for selling]
- Support: [How they adjust for customer communication]
```

## Applying the Voice

When producing any content:

1. Write the first draft focused on the message and structure
2. Review against the voice guide
3. Adjust:
   - Replace generic phrases with their characteristic phrases
   - Match sentence length patterns
   - Adjust formality level
   - Add or remove humor as appropriate
   - Ensure the opening and closing match their style
4. The final output should pass the "Would they have written this?" test

## Voice Drift Prevention

Over time, the agent's output can drift toward generic AI voice. Guard against:
- **Corporate speak**: "leverage", "synergize", "optimize", "align" (unless the user actually talks like this)
- **AI clichés**: "I'd be happy to", "Let's dive in", "Great question", "Here's the thing"
- **Over-politeness**: Unnecessary hedging, softening, or apologizing
- **Sameness**: Every piece sounding the same — vary energy and approach based on context

## Feedback Loop

When the user says something doesn't sound like them:
1. Ask specifically what's off: "What about this doesn't sound like you? Too formal? Too casual? Wrong energy?"
2. Note the feedback
3. Update the voice guide with the new insight
4. Rewrite the content
5. Over time, the voice profile gets more precise with each correction
