# Maintainer verification

Verified on 5 September 2026 before merge. The reviewer ran the committed offline verifier with all negative controls and the original downloaded provider JSON, then checked every manifest entry against local bytes.

All 25 rows, three slice boundaries, source-order checks, unit conversions, primary and retained-body hashes, and exact selected receipt fields pass. All three altered-input controls are rejected. The source-qualified cache remains one head-only body with a conflicting source clock.

This resolves issue #26 as stated. It does not resolve #13 (historical body/provider capture semantics), #1 (JSON Hero contents), or #4 (the anomalous county code). No monetary reward is associated with this review.

Reproduction:

```sh
python3 answers/26-sec-primary-verification/verify_sec_primary.py --negative-controls --raw-receipt /path/to/0873ec25-2bff-4610-b7c0-6cbd5bb31933.json.gz
```
