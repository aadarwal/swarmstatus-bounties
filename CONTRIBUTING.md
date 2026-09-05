# Contributing to Swarmstatus

This is a current, first-party Swarmstatus research invitation. Participation is optional and must stay within your own authorization. Contributor announcements and reviewed updates are current project activity, kept separate from the historical evidence corpus.

**Public credit for accepted evidence is the only incentive currently offered.** There is no payment, reserved claim, exclusivity, or guarantee of acceptance. Announcing an attempt does not earn credit or resolve a question.

## Choose and announce scoped work

Choose a question on the [public board](https://swarmstatus.com/bounties) or in the [GitHub tracker](https://github.com/aadarwal/swarmstatus-bounties/issues). Read its retained evidence and acceptance criteria. State which missing result you will investigate; do not treat a broad topic match as an answer.

To announce an attempt, post an issue comment containing only:

```text
/attempt
```

Put your intended scope in a separate comment. The announcement helps coordination; it does not assign or reserve the issue, verify active work, or exclude other contributors. Edit or remove that comment to withdraw the announcement.

## Submit reviewable evidence

Submit a PR adding `answers/<issue-number>-<short-name>.md`, using the [README answer template](README.md#answer-template). Address each acceptance criterion separately and include:

- The bounded result: supported, refuted, or inconclusive, with the exact part of the question answered.
- Public primary evidence URLs, record IDs or revision locators, and the fields or excerpts that support each claim. Existing public records can be cited as `https://swarmstatus.com/api/record?id=<record-id>`.
- Capture times in UTC and SHA-256 hashes of the retained source bytes. Keep publication/edit times, capture times, data periods, and inferred timezone conversions separate. Preserve unresolved or relative source clocks as such.
- Reproduction inputs, comparison rules, expected outputs, and limitations. Distinguish complete-string matches from decoded or normalized matches, posted requests from observed responses, and copies from independent evidence.

Submit scripts as text for review. Scripts and captured code or request payloads are inert until reviewed; supplying a script does not authorize its execution. Do not replay archived commands, proxy targets, counters, or mutation requests. Use ordinary authorized public reads, and keep credentials, private communications, and personal-identity speculation out of public submissions. Shared text or a self-applied label does not authenticate an actor, model, or provider.

## Review, credit, and closure

Partial evidence is welcome: identify the remaining gaps and use `Refs #<issue-number>` without a closing keyword. A partial answer may be accepted and credited while the question stays open.

For an answer addressing every acceptance criterion, use `Closes #<issue-number>` in the PR description and request review. The keyword is not acceptance: maintainers review the evidence and decide whether the question is resolved. Only a reviewed full answer closes the issue. An inconclusive result qualifies only if it meets the issue's stated criteria; unanswered criteria remain open. Neither an attempt declaration nor an open PR guarantees acceptance.

## Site links and status

The GitHub issue and PR are the canonical places to announce work and submit evidence. [Choose a scoped question](https://swarmstatus.com/contribute), read its linked contribution page, or browse the [full public board](https://swarmstatus.com/bounties). The [question catalog](https://swarmstatus.com/bounties.json) is available as JSON. [Updates](https://swarmstatus.com/updates) lists accepted evidence and site milestones with credit and remaining limits. These describe current contributions, not new historical incident evidence.
