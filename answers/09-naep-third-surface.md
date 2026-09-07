# Answer to #9: NAEP alias/query surface bounding and registration provenance

Exhaustive search across all 20+ shortener surfaces in the primary research corpus,
the Swarmstatus multi-platform index, and the complete wiki database (`collusion-wiki.db`)
refutes recurrence of the exact alias `nrcnaepres9983` and grade 12 science 2019 `HAOHTAIC`
query on a third surface. Recurrence is strictly bounded to `shortener:rmn.re` and `shortener:vanderbi.lt`.

Analysis of creator IPs (`64.236.176.163` vs `135.119.61.210`, both Microsoft ASN 8075),
clock calibration (Vanderbilt US/Central UTC-5 vs RMN UTC+0, true delta of 6 seconds),
and telemetry asymmetry (33 clicks vs 1 click) demonstrates that the entries are
**separate, parallel autonomous registrations**, not copied or imported database records.

See the [source-qualified answer package](09-naep-third-surface/README.md) for full
forensic comparison, raw evidence, and portable offline deterministic verification. Closes #9.
