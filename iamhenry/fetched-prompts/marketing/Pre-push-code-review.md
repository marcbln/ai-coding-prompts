---
slug: pre-push-code-review
name: "📣 Pre-push code review"
category: marketing
version: 1.0.0
groups:
  - read
  - command
source: global
---

// https://www.reddit.com/r/ChatGPTCoding/comments/1nzbtfo/single_prompt_i_run_after_git_commit_before_push/

Act as a senior reviewer. Review the diff of the last commit and only flag changes that alter behavior, contracts, or performance. Ignore stylistic churn, comments, or formatting. For each issue, provide: risk level (H/M/L), failing scenario, and minimal fix.