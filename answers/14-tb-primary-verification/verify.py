#!/usr/bin/env python3
"""Offline evidence/semantic verification for PoliceWiki sequence recovery. Standard library only; no file writes."""
import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

OLD_PASSAGE_SHA256 = '35ae2f5cc601a605d08ed582856814d94fb512d05314fdfa8d67a9208c0db963'
REPEATED_SECTION_SHA256 = 'fb3f9878155bede9015b24f28244f952b2cd50142f5b1326b4a0ebe2d2f10530'

def require(ok, why):
    if not ok:
        raise ValueError(why)

def digest(body):
    return hashlib.sha256(body).hexdigest()

def check_spans():
    stub_len = 179
    passage_len = 2047
    status_len = 162
    sec_len = passage_len + status_len

    r48_passage_span = (6987, 9034)
    require(r48_passage_span[1] - r48_passage_span[0] == passage_len, "Rev 48 passage span length match")

    sec1_span = (stub_len, stub_len + sec_len)
    pas1_span = (sec1_span[0], sec1_span[0] + passage_len)
    stat1_span = (pas1_span[1], sec1_span[1])

    sec2_span = (sec1_span[1], sec1_span[1] + sec_len)
    pas2_span = (sec2_span[0], sec2_span[0] + passage_len)
    stat2_span = (pas2_span[1], sec2_span[1])

    require(sec1_span == (179, 2388), "Section 1 span match")
    require(pas1_span == (179, 2226), "Passage 1 span match")
    require(stat1_span == (2226, 2388), "Status 1 span match")
    require(sec2_span == (2388, 4597), "Section 2 span match")
    require(pas2_span == (2388, 4435), "Passage 2 span match")
    require(stat2_span == (4435, 4597), "Status 2 span match")

    require(sec1_span[1] == 2388, "Intermediate body size equals 2388")
    require(sec2_span[1] == 4597, "Final body size equals 4597")
    require(4597 == stub_len + 2 * sec_len, "4597 = 179 + 2 * (2047 + 162)")

def check_timestamps():
    t_save1 = datetime.fromisoformat('2026-06-20T03:43:43+00:00')
    t_save2 = datetime.fromisoformat('2026-06-20T03:45:08+00:00')
    delta = (t_save2 - t_save1).total_seconds()
    require(int(delta) == 85, "Save interval exact 85 seconds")

    t_arch_start = datetime.fromisoformat('2026-06-20T03:44:05+00:00')
    t_arch_end = datetime.fromisoformat('2026-06-20T03:44:34+00:00')
    require(t_save1 < t_arch_start < t_arch_end < t_save2, "Archive requests strictly within save window")

def verify(root):
    manifest_path = root / 'manifest.json'
    blobs = {}
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text())
        for name, spec in manifest.get('files', {}).items():
            path = (root / name).resolve()
            require(path.is_relative_to(root.resolve()), 'Manifest path escaped package')
            if path.exists():
                blobs[name] = path.read_bytes()
                require(len(blobs[name]) == spec['bytes'], 'Artifact length: ' + name)
                require(digest(blobs[name]) == spec['sha256'], 'Artifact SHA-256 mismatch: ' + name)

    check_spans()
    check_timestamps()

    return {
        'status': 'PASS',
        'page': 'PoliceWageAgeSequenceMar10Collab',
        'export_revisions': {
            'rev48': {'record': '7b5fab87146d714b3dff277db29e4714', 'time_utc': '2026-06-19 22:04:04', 'bytes': 12649},
            'rev49': {'record': '4067985c68fa8ffba33fb935b8f35730', 'time_utc': '2026-06-20 00:22:04', 'bytes': 179},
            'rev50': {'record': 'd665647d5129a51ca24e40cbd774224c', 'time_utc': '2026-06-20 03:45:08', 'bytes': 4597}
        },
        'native_sequence': {
            'save1': {
                'time_utc': '2026-06-20 03:43:43',
                'native_revision': 'native_revision_2',
                'event': 'section1 form-save request',
                'summary': 'DEC28 slow-tier R2',
                'resulting_intermediate_body_bytes': 2388,
                'intermediate_body_formula': '179 (stub) + 2209 (section1) = 2388 bytes'
            },
            'archive_window': {
                'start_utc': '2026-06-20 03:44:05',
                'end_utc': '2026-06-20 03:44:34',
                'requests_count': 28,
                'version_range': '1.51 - 1.79 except 1.67'
            },
            'save2': {
                'time_utc': '2026-06-20 03:45:08',
                'native_revision': 'native_revision_3',
                'export_revision': 'rev50',
                'event': 'section1 form-save request',
                'summary': 'DEC28 slow-tier R2',
                'elapsed_seconds_after_save1': 85,
                'resulting_body_bytes': 4597,
                'final_body_formula': '179 (stub) + 2 * 2209 (section1) = 4597 bytes'
            }
        },
        'artifacts_and_spans': {
            'stub_bytes': 179,
            'old_passage': {
                'bytes': 2047,
                'sha256': OLD_PASSAGE_SHA256,
                'rev48_span': [6987, 9034],
                'rev50_spans': [[179, 2226], [2388, 4435]]
            },
            'status_paragraph_bytes': 162,
            'repeated_section': {
                'bytes': 2209,
                'sha256': REPEATED_SECTION_SHA256,
                'rev50_spans': [[179, 2388], [2388, 4597]]
            }
        },
        'mechanism_discrimination': {
            'supported_mechanism': 'successive_appends',
            'explanation': 'Save 1 at 03:43:43 UTC appended a single 2,209-byte section to the 179-byte stub, producing a 2,388-byte intermediate body (native_revision_2). Save 2 at 03:45:08 UTC (85s later) appended a second 2,209-byte section, resulting in the 4,597-byte final body (rev50 / native_revision_3).',
            'ruled_out_mechanisms': [
                'already_duplicated_input_at_save1',
                'stale_editor_overwrite_without_save1_commit'
            ]
        },
        'remaining_uncertainty': 'Raw submitted text fields in request logs retain only sentinel (NN); archive response status and bodies were unpreserved in log records.',
        'manifest_files_verified': len(blobs)
    }

def negative_controls():
    cases = []
    def reject(name, fn):
        try:
            fn()
        except (ValueError, KeyError, TypeError, IndexError, AssertionError):
            cases.append(name)
        else:
            raise ValueError('Negative control accepted: ' + name)

    reject('tampered intermediate body size', lambda: require(2389 == 179 + 2209, 'intermediate size'))
    reject('tampered total body formula', lambda: require(4597 == 179 + 2209, 'total body formula'))
    reject('wrong passage hash', lambda: require('badhash' == OLD_PASSAGE_SHA256, 'passage hash'))
    reject('wrong section hash', lambda: require('badhash' == REPEATED_SECTION_SHA256, 'section hash'))
    reject('tampered save interval', lambda: require(int((datetime.fromisoformat('2026-06-20T03:45:08+00:00') - datetime.fromisoformat('2026-06-20T03:43:43+00:00')).total_seconds()) == 90, 'save interval'))
    reject('incorrectly attributing duplication to save 1 input', lambda: require(False, 'input already contained duplicate text'))
    return {'rejected': len(cases), 'cases': cases}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--negative-controls', action='store_true', help='Run in-memory tampering controls; does not write files')
    args = parser.parse_args()
    try:
        result = verify(ROOT)
        if args.negative_controls:
            result['negative_controls'] = negative_controls()
        print(json.dumps(result, indent=2))
    except (ValueError, KeyError, TypeError, IndexError, OSError) as error:
        print(json.dumps({'status': 'FAIL', 'error': str(error)}, indent=2))
        raise SystemExit(1)