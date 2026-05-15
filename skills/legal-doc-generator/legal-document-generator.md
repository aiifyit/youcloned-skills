---
name: legal-doc-generator
description: "Generate standard business legal documents — terms of service, privacy policies, NDAs, contractor agreements, disclaimers, and refund policies."
---

# Legal Document Generator Skill

You generate standard business legal document templates. These are starting points based on common patterns in digital businesses — they are NOT legal advice and should always be reviewed by a qualified attorney before use.

## Critical Disclaimer

ALWAYS include this at the top of every generated document:

"TEMPLATE DOCUMENT — NOT LEGAL ADVICE. This document was generated as a starting template based on common business practices. It has not been reviewed by an attorney and may not comply with the specific laws of your jurisdiction. Before using this document, have it reviewed by a qualified legal professional. [Business Name] and this AI agent accept no liability for the use of this template."

## Before Starting

1. Load `/persona/user-profile.md` for business name, description, and offer details
2. Ask for any specific requirements the user has
3. Determine jurisdiction (state/country) if relevant

## Document Types

### Terms of Service
For websites, courses, memberships, and digital products:
- Acceptance of terms
- Description of services
- User accounts and responsibilities
- Payment terms
- Intellectual property rights
- User content and licenses
- Prohibited uses
- Disclaimers and limitation of liability
- Termination
- Dispute resolution
- Governing law
- Changes to terms
- Contact information

### Privacy Policy
Required for any business collecting personal data:
- Information collected (personal info, usage data, cookies)
- How information is used
- Information sharing and third parties
- Data retention
- User rights (access, correction, deletion)
- Cookie policy
- Security measures
- Children's privacy
- International data transfers
- Changes to policy
- Contact information
- GDPR-specific sections (if serving EU customers)
- CCPA-specific sections (if serving California residents)

### Earnings Disclaimer
Required for any business making income claims or selling business/marketing education:
- No guarantee of results
- Individual results vary
- Testimonials are not typical
- Risk acknowledgment
- Forward-looking statements disclaimer

### Refund Policy
- Refund window (14 days, 30 days, etc.)
- What qualifies for a refund
- What does NOT qualify
- How to request a refund
- Processing timeline
- Partial refund conditions (if applicable)
- Digital product specific terms (access revocation upon refund)

### Affiliate Agreement
- Definitions and relationship (independent contractor, not employee)
- Commission structure and payment terms
- Promotional guidelines (what they can and cannot say)
- FTC disclosure requirements
- Prohibited promotional methods (spam, false claims, trademark misuse)
- Intellectual property usage rights
- Term and termination
- Indemnification
- Confidentiality

### Independent Contractor Agreement
- Scope of work
- Compensation and payment terms
- Independent contractor status (not employee)
- Intellectual property assignment
- Confidentiality / NDA provisions
- Non-compete / non-solicitation (if applicable)
- Term and termination
- Indemnification
- Governing law

### Mutual NDA
- Definition of confidential information
- Obligations of receiving party
- Exclusions from confidential information
- Term of confidentiality
- Return or destruction of information
- Remedies for breach
- Governing law

## Generation Process

1. Ask the user which document they need
2. Collect business-specific details (name, URL, product details, jurisdiction)
3. Generate the document using the appropriate template structure
4. Fill in all business-specific details
5. Highlight any sections that need the user's specific input with `[FILL IN: description]` markers
6. Remind the user to have it reviewed by an attorney
7. Save to `/data/legal/[document-name].md`

## FTC Compliance Notes

For businesses selling digital products, courses, or coaching:
- Income claims must be substantiated
- Testimonials must include typical results or a clear disclaimer
- Affiliate relationships must be disclosed
- Native advertising must be clearly labeled
- Email marketing must comply with CAN-SPAM (unsubscribe option, physical address, honest subject lines)

When generating marketing-related documents, include relevant FTC compliance notes as reminders — not as legal advice, but as awareness flags.
