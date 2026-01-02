```
- This is the text area within Apple Store Connect "Review Notes"
- URL: App Name > Distribution > Subscription
- Purpose: To provide the Apple team notes on how to test the paywall
- Use When: Use this template within a codebase to an LLM can answer and populate the answers for my app
```

Review Notes are only for Apple’s reviewers. Use them to remove ambiguity and speed approval by clearly describing the subscription, the flow to reach it, and how to test all states.

What to include
 • Subscription basics: Product ID, display name, group, duration, price, and whether Family Sharing is enabled. Mention any regions excluded or special tax category if not “match to parent app.”
 • What it unlocks: Precisely list the features and content gated behind the subscription (e.g., “Unlimited recipe personalization, AI meal plans, and grocery export”).
 • User flow to purchase: Step‑by‑step path in the app to the paywall and purchase sheet (screens, buttons, menus, deeplinks if applicable). Note if sign‑in is required first.
 • Test credentials: Provide a working demo account the reviewer can use (email/username and password), plus any passcodes or feature flags the app needs toggled to see the paywall or premium features.
 • Offers and eligibility logic: Free trial details, introductory offers, promotional offers, win‑back behavior, and offer code redemption locations. State who qualifies and how the app determines eligibility.
 • Restore and management: Where users can restore purchases, view status, and manage/cancel. Note any in‑app “Manage Subscription” link and expected behavior.
 • Edge cases and limitations: Device/OS requirements, country availability, offline behavior, and any temporary limitations the reviewer should know.
 • Server dependencies: If premium features require server calls or receipt validation, note expected endpoints, common delays, and anything the reviewer might need to wait for or retry.
 • Compliance notes: Confirm that the paywall and flows follow App Store guidelines (e.g., clear pricing, terms, trial messaging) and that data collection aligns with your App Privacy declarations.