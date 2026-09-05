#!/usr/bin/env python3
"""Verify selected public metadata offline; complete originals are not included."""
import copy
import datetime as dt
import hashlib
import json
from pathlib import Path
import sys
from urllib.parse import parse_qsl, urlsplit

BASE = Path(__file__).resolve().parent
EMPTY_SHA256 = hashlib.sha256(b'').hexdigest()
MANIFEST_SOURCE_SHA256 = 'c93d0cafc03e6fd804fc41813696202742e3cb9f2094108de531968422d979fa'
WORKFLOW_MEANING = ('Recorded local acquisition-workflow start before cache check/request waiting; '
                    'not exact HTTP-send, completion, source publication, or incident time.')
COLUMNS = 'CIP6 ID,CIP6,Year,Completions,Top Completions'
# Full-source hashes below are reviewed provenance assertions, not computed here.
# Their association with these exact reports was checked against held originals.
EXPECTED = {'b658f273-fd60-4191-b496-d244d47d5531': {'university': '153658',
                                          'gender': '1',
                                          'record_id': 'c48f36885e8aafa875814dd27550b006',
                                          'source_sha256': '4aad92b58f03715d433029ee2b1ccbb441eb0f114d3710490887c2d7ba3351f2',
                                          'source_bytes': 7800,
                                          'event': '2026-05-28T00:35:26.339Z',
                                          'report': '2026-05-28T00:35:47Z',
                                          'response_date': 'Thu, 28 May 2026 00:35:26 GMT',
                                          'workflow_start': '2026-09-05T17:29:44.659553+00:00',
                                          'manifest_pointer': '/results/1144',
                                          'delta_ms': 20661},
 'dd6c4784-2a86-49d8-8418-431ed781f0b7': {'university': '153658',
                                          'gender': '2',
                                          'record_id': 'd7c5059620fb8c8fd43b1e8f9e670023',
                                          'source_sha256': '9255cbc45222f46a0e62b21cd7eb7cbd233511220cf8563b4682ac6bded2d94c',
                                          'source_bytes': 7800,
                                          'event': '2026-05-28T00:35:30.424Z',
                                          'report': '2026-05-28T00:35:51Z',
                                          'response_date': 'Thu, 28 May 2026 00:35:30 GMT',
                                          'workflow_start': '2026-09-05T17:30:09.653089+00:00',
                                          'manifest_pointer': '/results/1266',
                                          'delta_ms': 20576},
 '65144082-bcc5-4e7d-96b9-556f35d63872': {'university': '215062',
                                          'gender': '2',
                                          'record_id': 'd45867666a1a1b000d92c3b157dd5fb6',
                                          'source_sha256': '82e62ae8f9d4e34004c981b8b00f8ccf8ecbd8d184ac1d10023df2ad753ea666',
                                          'source_bytes': 7560,
                                          'event': '2026-05-28T00:35:40.750Z',
                                          'report': '2026-05-28T00:36:02Z',
                                          'response_date': 'Thu, 28 May 2026 00:35:41 GMT',
                                          'workflow_start': '2026-09-05T17:30:02.567143+00:00',
                                          'manifest_pointer': '/results/1232',
                                          'delta_ms': 21250},
 'fabdcd45-6f13-49c8-8823-8650a9905622': {'university': '215062',
                                          'gender': '1',
                                          'record_id': 'fff2a044abeaf9371068a949799765a6',
                                          'source_sha256': '0908f5dda535a478261609e93f51bda46676927dfdfc94f2ad3da49c08349337',
                                          'source_bytes': 7800,
                                          'event': '2026-05-28T00:35:44.570Z',
                                          'report': '2026-05-28T00:36:05Z',
                                          'response_date': 'Thu, 28 May 2026 00:35:44 GMT',
                                          'workflow_start': '2026-09-05T17:30:58.919280+00:00',
                                          'manifest_pointer': '/results/1494',
                                          'delta_ms': 20430}}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'Duplicate JSON key: ' + key)
        result[key] = value
    return result


def read_json(name):
    return json.loads((BASE / name).read_text(encoding='utf-8'), object_pairs_hook=unique_object)


def parse_time(value):
    parsed = dt.datetime.fromisoformat(value.replace('Z', '+00:00'))
    require(parsed.utcoffset() == dt.timedelta(0), 'Expected explicit UTC time')
    return parsed


def validate_evidence(document):
    require(set(document) == {'schema_version', 'issue', 'scope', 'records'}, 'Unexpected document fields')
    require(document['schema_version'] == 1 and document['issue'] == 16, 'Wrong schema or issue')
    records = document['records']
    require(len(records) == 4, 'Expected exactly four selected reports')
    ids = [record['report_id'] for record in records]
    require(len(set(ids)) == 4 and set(ids) == set(EXPECTED), 'Wrong or repeated report IDs')
    deltas = {}
    for record in records:
        require(set(record) == {'report_id', 'canonical_acquisition_record_id', 'full_source',
                'json_pointer_values', 'raw_string_line_excerpts', 'acquisition_workflow_start'},
                'Unexpected record fields')
        rid = record['report_id']
        e = EXPECTED[rid]
        require(record['canonical_acquisition_record_id'] == e['record_id'], 'Changed canonical source mapping')
        source = record['full_source']
        require(source == {
            'url': 'https://urlquery.net/report/' + rid + '/json',
            'uncompressed_json_sha256': e['source_sha256'],
            'uncompressed_json_bytes': e['source_bytes'],
            'included_in_package': False,
        }, 'Changed full-source provenance mapping')
        parameters = [('cube', 'ipeds_completions'), ('drilldowns', 'Year,CIP6'),
                      ('measures', 'Completions'),
                      ('include', 'University:' + e['university'] + ';Gender:' + e['gender']),
                      ('top', '5.Year.Completions.desc')]
        addr = 'api.datausa.io/tesseract/data.jsonrecords?' + '&'.join(k + '=' + v for k, v in parameters)
        values = record['json_pointer_values']
        expected_values = {
            '/report_id': rid,
            '/submit/url/schema': 'https', '/submit/url/addr': addr,
            '/http/0/url/schema': 'https', '/http/0/url/addr': addr,
            '/date': e['report'], '/http/0/date': e['event'],
            '/http/0/response/status_code': '200', '/http/0/response/headers': None,
            '/http/0/response/data/data': None, '/http/0/response/data/size_decoded': 0,
            '/http/0/response/data/sha256': EMPTY_SHA256,
        }
        require(values == expected_values, 'Changed pointer, query identity, body marker or clock')
        for prefix in ('/submit/url/', '/http/0/url/'):
            url = values[prefix + 'schema'] + '://' + values[prefix + 'addr']
            parsed = urlsplit(url)
            require(parsed.scheme == 'https' and parsed.netloc == 'api.datausa.io' and
                    parsed.path == '/tesseract/data.jsonrecords' and not parsed.fragment,
                    'Wrong resource identifier')
            require(parse_qsl(parsed.query, keep_blank_values=True) == parameters,
                    'Changed, extra, duplicated or reordered analytical parameter')
        raw = record['raw_string_line_excerpts']
        expected_lines = [
            {'pointer': '/http/0/request/raw', 'line_1_based': 1,
             'text': 'GET /' + addr.split('/', 1)[1] + ' HTTP/1.1'},
            {'pointer': '/http/0/response/raw', 'line_1_based': 3,
             'text': 'Date: ' + e['response_date']},
            {'pointer': '/http/0/response/raw', 'line_1_based': 8,
             'text': 'x-tesseract-columns: ' + COLUMNS},
            {'pointer': '/http/0/response/raw', 'line_1_based': 9,
             'text': 'x-tesseract-queryrows: 60'},
            {'pointer': '/http/0/response/raw', 'line_1_based': 10,
             'text': 'x-tesseract-totalrows: 60'},
        ]
        require(raw == expected_lines, 'Changed raw-header/request line, position or clock')
        workflow = record['acquisition_workflow_start']
        require(workflow == {
            'source_document': 'fetch_manifest.json',
            'source_sha256': MANIFEST_SOURCE_SHA256,
            'json_pointer': e['manifest_pointer'] + '/attempted_at_utc',
            'value': e['workflow_start'], 'meaning': WORKFLOW_MEANING,
        }, 'Changed acquisition source mapping, clock value or meaning')
        event, report = parse_time(e['event']), parse_time(e['report'])
        milliseconds = round((report - event).total_seconds() * 1000)
        require(milliseconds == e['delta_ms'], 'Wrong event/report arithmetic')
        parse_time(workflow['value'])
        deltas[rid] = milliseconds
    return deltas


def negative_controls(document):
    def fields(d):
        return d['records'][0]['json_pointer_values']

    def line(d, index, text):
        d['records'][0]['raw_string_line_excerpts'][index]['text'] = text

    def source_swap(d):
        d['records'][0]['full_source']['uncompressed_json_sha256'] = d['records'][1]['full_source']['uncompressed_json_sha256']

    cases = [
        ('changed_count', lambda d: line(d, 3, 'x-tesseract-queryrows: 5')),
        ('changed_schema', lambda d: line(d, 2, 'x-tesseract-columns: CIP6,Year,Completions')),
        ('swapped_source_hash', source_swap),
        ('event_replaced_by_report', lambda d: fields(d).__setitem__('/http/0/date', fields(d)['/date'])),
        ('response_date_replaced_by_event', lambda d: line(d, 1, 'Date: ' + fields(d)['/http/0/date'])),
        ('workflow_replaced_by_report', lambda d: d['records'][0]['acquisition_workflow_start'].__setitem__('value', fields(d)['/date'])),
        ('workflow_mislabeled_completion', lambda d: d['records'][0]['acquisition_workflow_start'].__setitem__('meaning', 'Acquisition completion time')),
        ('added_year_filter', lambda d: fields(d).__setitem__('/http/0/url/addr', fields(d)['/http/0/url/addr'] + '&Year=2016,2017,2018')),
        ('changed_manifest_source_pointer', lambda d: d['records'][0]['acquisition_workflow_start'].__setitem__('json_pointer', '/results/1266/attempted_at_utc')),
    ]
    rejected = []
    # Semantic checks run on mutated copies, independently of file-hash failure.
    for name, mutate in cases:
        altered = copy.deepcopy(document)
        mutate(altered)
        try:
            validate_evidence(altered)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('Negative control accepted: ' + name)
    return rejected


def main():
    manifest = read_json('manifest.json')
    require(manifest['schema_version'] == 1 and manifest['issue'] == 16, 'Wrong manifest')
    files = manifest['files']
    require(set(files) == {'README.md', 'selected-evidence.json', 'review-provenance.json', 'verify.py'},
            'Unexpected manifest file inventory')
    for name, pin in files.items():
        payload = (BASE / name).read_bytes()
        require(pin == {'bytes': len(payload), 'sha256': hashlib.sha256(payload).hexdigest()},
                'Package hash/size mismatch: ' + name)
    evidence = read_json('selected-evidence.json')
    deltas = validate_evidence(evidence)
    for record in evidence['records']:
        require(record['full_source']['uncompressed_json_sha256'] != files['selected-evidence.json']['sha256'],
                'Selected excerpt digest confused with full-source digest')
    review = read_json('review-provenance.json')
    require(review['source_review']['private_envelopes_and_review_inputs_included'] is False,
            'Incorrect original-source inclusion claim')
    rejected = negative_controls(evidence)
    print(json.dumps({
        'result': 'PASS', 'selected_reports_checked': 4, 'payload_files_checked': len(files),
        'negative_controls_rejected': rejected, 'report_minus_event_milliseconds': deltas,
        'network_requests': 0, 'full_source_hashes_recomputed': False,
        'scope': 'Portable selected-excerpt integrity and pinned consistency only; original-source verification is a separate reviewed provenance assertion.',
    }, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError) as error:
        print('FAIL: ' + str(error), file=sys.stderr)
        sys.exit(1)
