# Iowa named-recipient reply evidence (#34)

Status: **partial**. This package does not close the issue.

## Question

Can an exact Iowa paste request and its claimed answer be joined by a retained parent/reply relation, an explicit source link, or independent read/acknowledgement evidence?

## Finding

No exact request-to-answer join is established from the retained evidence. `IowaReply0227` and `IowaCacheReply` are both addressed to the displayed recipient `agent-0227` and cite cache `eb7e28bd`, but neither retains a provider-stored parent/reply relation or an exact link to the request object. The separately addressed thanks/post-Q5 paste is only a candidate acknowledgement; it does not prove who read which earlier paste.

## Evidence

- `IowaReply0227`: https://paste.linuxiarz.pl/view/11d30c3f, sha256 `570051f593cd4ebd1e572cd77e44fb46634bccd48d19ceb5722050cf276230cb`, retained record `25194b724b3fc7ea94dc26bbf0fb0bba`.
- `IowaCacheReply`: https://paste.linuxiarz.pl/view/1ad7edc4, sha256 `33c42767e95a708a78c3c02380d8e1142fdc86d236d824292e91d9d78ab8d81b`, retained record `bffc285e8e4b206ae385c314525320c9`.
- `ThanksPostQ5`: https://paste.linuxiarz.pl/view/28c3155e, sha256 `06215ba7ebf9a6ef4020a38e0d41288dd8acba35e9a4f8c0d7ad8950cf65a50d`, retained record prefix `073`.

All three source timestamps are raw `2 Months ago.` with basis `relative_age`.

## Join matrix

| Evidence | Present |
| --- | --- |
| Named recipient | yes |
| Cache citation | yes |
| Q5 wording claim | yes |
| Provider-stored parent/reply relation | no |
| Exact source link to request object | no |
| Independent read/acknowledgement | no |

## Limits

- The exact request paste object is not retained in this package.
- Relative ages are not converted to absolute timestamps.
- The acknowledgement candidate is separately addressed and is not proof of delivery or reading.
- No operator or model identity is authenticated.

Run `python3 verify.py` from this directory or `python3 answers/34-iowa-named-recipient-reply-evidence/verify.py` from the repository root.
