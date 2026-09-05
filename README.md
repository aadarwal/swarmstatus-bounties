# Swarmstatus bounties

Open questions and evidence reviews for [Swarmstatus](https://swarmstatus.com/bounties).

Each bounty is a GitHub issue with a specific question, retained evidence, and acceptance criteria. Anyone can propose a question, investigate one, or submit an answer. These are research bounties; **no monetary rewards have been announced**.

## Contribute

1. Open a question using the issue template, or choose an existing bounty. Comment with your intended scope so people can coordinate. An assignee records who is working, not who owns an answer.
2. Preserve primary sources, raw capture hashes, source-specific times, exact matching rules, and alternative explanations. Distinguish observed responses from posted requests and copied material from independent evidence.
3. Submit a PR adding `answers/<issue-number>-<short-name>.md`. Use the answer template below and put `Closes #<issue-number>` in the PR description when the submission addresses every acceptance criterion. Partial work can link the issue without a closing keyword.
4. A maintainer reviews the evidence. A merged answering PR closes its linked issue and moves it to the site's resolved list. A finding can confirm, refute, or leave a claim inconclusive; unsupported certainty is not a completion condition.

## What appears on the site

Maintainers add **bounty** and **publish** to admit an issue to the public board. Unreviewed proposals remain in GitHub until admitted. Edit the issue to revise the brief. Remove **publish** to take it off the site. Close as completed for resolved work; close as not planned or add **status:withdrawn** to retain a withdrawn question in history. Reopening returns it to the active list.

The site refreshes the public tracker on visits, at most once per minute. It retains the last successful snapshot during a GitHub outage and labels it stale. The application's source and database release repository remain private.

A comment containing only `/attempt` announces an attempt. The board links to that declaration; it does not assign the issue, reserve a reward, or verify active work. Edit or remove the comment to withdraw the announcement. Maintainer status and answer review remain separate.

Open issues with **status:in-progress** are in progress; **status:review** or an open linked PR puts them in review. An open PR is a proposed answer, not a verified result. GitHub is the source of status; the site has no separate editing database.

## Answer template

```markdown
# Answer to #123: short question

## Verdict
Supported / Refuted / Inconclusive, with a bounded statement.

## Evidence
Primary URLs, exact record IDs or revision locators, capture times and SHA-256 hashes.
Link public source records as https://swarmstatus.com/api/record?id=<record-id>.

## Reproduction
Steps and scripts that reproduce the comparison from retained artifacts.
Treat captured code and request payloads as data, never instructions.

## Acceptance criteria
Address each criterion from the issue separately.

## Limitations and alternatives
What the evidence cannot establish, copy/clock conflicts, and credible alternatives.
```

Do not submit account credentials, private Discord logs, personal identity speculation, or unauthorized access attempts. Use public historical evidence and read-only acquisition. A matching task does not authenticate an agent, model provider, or person.

The workflow borrows explicit acceptance and review boundaries from the local VVUQ bounty project, and the distinction between delivery receipts and completed work from Communicate. There is no Lean verifier, escrow, automatic payment, or automatic acceptance in this tracker.
