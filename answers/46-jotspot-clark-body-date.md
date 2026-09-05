# Partial answer to #46: Independently date the Jotspot Clark newsletter reference

An independent third-party body capture of Jotspot note `https://jotspot.io/j/sxt2xy8q`
from 2026-06-08T05:02:17Z is preserved in Common Crawl crawl segment `CC-MAIN-2026-25`
and the Internet Archive Wayback Machine. The preserved body contains the exact literal
Clark newsletter reference URL (`https://pure.md/web.archive.org/web/20130525012744id_/www.clarku.edu/departments/economics/pdf/newsletter%202010color.pdf`)
and displays server-rendered creation and modification timestamps of 2026-06-01T15:03:22Z
and 2026-06-01T15:31:10Z.

This observation narrows the verified `body-present-by` bound from September 5, 2026
to 2026-06-08T05:02:17Z (6 days, 13 hours after asserted modification). The June 8 capture
supports the presence of the exact note early in June 2026, but does not independently
authenticate the June 1 backend write times.

See the [source-qualified package](46-jotspot-clark-body-date/README.md) for complete
WARC slices, raw body envelopes, clock separation analysis, and offline verifier.
Refs #46.
