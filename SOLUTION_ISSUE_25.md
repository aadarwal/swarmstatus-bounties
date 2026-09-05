# Solution for Issue #25

## 🛠️ Proposed Solution

### Analysis
The mapping for `shortener_creation` was incorrectly keyed by the physical CSV line number, causing each observation to point to the next alias. The fix is to key the mapping by the actual alias string.

### Fix
Update the script that generates the mapping to use the alias column as the key and validate that the alias exists.

### Implementation
```diff
--- a/scripts/generate_shortener_mapping.py
+++ b/scripts/generate_shortener_mapping.py
@@
-    for idx, row in enumerate(reader, start=1):
-        # Previously used line number as key, causing off-by-one errors
-        mapping[str(idx)] = row['alias']
+    for idx, row in enumerate(reader, start=1):
+        # Use the alias itself as the key to avoid confusion with CSV line numbers.
+        # The alias column is guaranteed to be unique per row.
+        alias = row.get('alias')
+        if not alias:
+            logger.warning("Row %s missing alias; skipping", idx)
+            continue
+        mapping[alias] = row['destination']
*** End Patch
```

### Testing
1. Run the script locally: `python scripts/generate_shortener_mapping.py`.
2. Verify that the output JSON contains alias keys (e.g., `atestxyz555+`) instead of numeric keys.
3. Run the existing unit tests (`pytest`) to ensure no regressions.
4. Manually inspect a few entries in the generated mapping to confirm correct alias‑destination pairs.

---
💰 **Wallet Address:** `0xEA3b60D7076B62749fb3C65b167bf79326e8A504`
