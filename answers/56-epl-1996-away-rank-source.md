# Answer to #56: Reconciliation of Opposite 1996/97 EPL Away Ranks

The opposite 1996/97 Premier League away ranks in retained pastes `57492617` (Sunderland A19, Middlesbrough A20) and `9629c5f3` (Middlesbrough A19, Sunderland A20) are reconciled by two distinct, reproducible split-table sorting definitions applied to the primary Pulselive API standings payload:

1. **Paste `9629c5f3`** sorts split records strictly by match performance (`Points DESC`, `Goal Difference DESC`, `Goals For DESC`) without propagating administrative point deductions into split tables. Middlesbrough and Sunderland both earned 13 points away; Middlesbrough's -18 goal difference places them 19th, while Sunderland's -20 goal difference places them 20th.
2. **Paste `57492617`** applies Middlesbrough's 3-point administrative penalty deduction (imposed for failing to fulfill their away fixture against Blackburn Rovers) directly to Middlesbrough's points total in split tables. Middlesbrough's away points are reduced from 13 to 10, resulting in Sunderland A19 and Middlesbrough A20. Deducting 3 points from Middlesbrough's home points (29 to 26) simultaneously accounts for Sunderland H14 and Middlesbrough H15.

See the complete [answer package](56-epl-1996-away-rank-source/README.md) for retained primary API payloads, byte-exact paste texts, manifest verification, and portable offline reproduction.

Closes #56.
