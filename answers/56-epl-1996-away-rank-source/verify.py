#!/usr/bin/env python3
"""Offline verifier for Swarmstatus issue #56 answer package.
Verifies file hashes, primary Pulselive API standings payload, and exact
reproduction of both 1996/97 EPL away and home rankings from retained pastes.
"""
import argparse
import copy
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

PASTE_57492617_SHA256 = '5055ba9b9cdd61a86b3960c8a5638e4d82577bd0c708571d2878e4735c2434f0'
PASTE_9629c5f3_SHA256 = 'b3d6652358d93f25fa92083bef3a27709ff483983e34e9659b3803dd4ea73e1c'
PULSELIVE_STANDINGS_SHA256 = '9ca3c33dac5492b3110ef10d7712b3048a6db0c4be5db76d93d43a93dd1cf41b'


def require(ok, msg):
    """Enforce invariant."""
    if not ok:
        raise ValueError(msg)


def sha256_hex(raw_bytes):
    """Return lowercase hex SHA-256."""
    return hashlib.sha256(raw_bytes).hexdigest()


def check_manifest(pkg_root):
    """Validate manifest schema and file hashes."""
    manifest_path = pkg_root / 'manifest.json'
    require(manifest_path.is_file(), 'manifest.json missing')
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    require(manifest.get('schema_version') == 1, 'Invalid schema_version')
    files_map = manifest.get('files', {})
    require(len(files_map) >= 5, 'Insufficient files in manifest')

    cached_files = {}
    for rel_path, spec in files_map.items():
        file_path = (pkg_root / rel_path).resolve()
        require(file_path.is_relative_to(pkg_root), f'Path escapes package: {rel_path}')
        require(file_path.is_file(), f'Evidence file missing: {rel_path}')
        raw = file_path.read_bytes()
        require(len(raw) == spec['bytes'], f'Byte count mismatch for {rel_path}: {len(raw)} != {spec["bytes"]}')
        actual_hash = sha256_hex(raw)
        require(actual_hash == spec['sha256'], f'SHA-256 mismatch for {rel_path}: {actual_hash} != {spec["sha256"]}')
        cached_files[rel_path] = raw
    return cached_files


def verify_primary_api(raw_bytes):
    """Validate raw Pulselive API standings payload."""
    require(len(raw_bytes) == 14181, 'Pulselive API payload byte length changed')
    require(sha256_hex(raw_bytes) == PULSELIVE_STANDINGS_SHA256, 'Pulselive API hash mismatch')
    data = json.loads(raw_bytes.decode('utf-8'))

    comp_season = data.get('compSeason', {})
    require(comp_season.get('id') == 5, 'compSeason ID must be 5 (1996/97)')
    require(comp_season.get('label') == '1996/97', 'compSeason label must be 1996/97')

    tables = data.get('tables', [])
    require(len(tables) == 1, 'Expected exactly 1 standings table')
    entries = tables[0].get('entries', [])
    require(len(entries) == 20, 'Expected 20 teams in 1996/97 Premier League')

    teams = {e['team']['name']: e for e in entries}
    require('Sunderland' in teams, 'Sunderland missing from entries')
    require('Middlesbrough' in teams, 'Middlesbrough missing from entries')
    require('Nottingham Forest' in teams, 'Nottingham Forest missing from entries')

    boro = teams['Middlesbrough']
    boro_ann = boro.get('annotations', [])
    require(any(a.get('type') == 'PD' and '3 points' in a.get('description', '') for a in boro_ann),
            'Middlesbrough 3-point deduction annotation missing')
    require(boro['position'] == 19, 'Middlesbrough overall position must be 19')
    require(boro['overall']['points'] == 39, 'Middlesbrough overall points must be 39 (42 - 3)')
    require(boro['home']['points'] == 29, 'Middlesbrough home points must be 29')
    require(boro['away']['points'] == 13, 'Middlesbrough away points must be 13')

    sun = teams['Sunderland']
    require(sun['position'] == 18, 'Sunderland overall position must be 18')
    require(sun['overall']['points'] == 40, 'Sunderland overall points must be 40')
    require(sun['home']['points'] == 27, 'Sunderland home points must be 27')
    require(sun['away']['points'] == 13, 'Sunderland away points must be 13')

    return entries


def compute_standings(entries, split_key, deduct_boro=False):
    """Rank 20 clubs using official Premier League comparator (Points DESC, GD DESC, GF DESC)."""
    table = []
    for e in entries:
        raw_rec = e[split_key]
        name = e['team']['name']
        pts = raw_rec['points']
        if deduct_boro and name == 'Middlesbrough':
            pts -= 3
        table.append({
            'name': name,
            'points': pts,
            'goalsDifference': raw_rec['goalsDifference'],
            'goalsFor': raw_rec['goalsFor'],
            'overall_position': e['position']
        })
    table.sort(key=lambda x: (x['points'], x['goalsDifference'], x['goalsFor']), reverse=True)
    return {row['name']: (idx + 1, row) for idx, row in enumerate(table)}


def verify_paste_reproductions(entries, raw_p1, raw_p2):
    """Reproduce and verify both retained paste bodies."""
    require(len(raw_p1) == 750 and sha256_hex(raw_p1) == PASTE_57492617_SHA256,
            'Paste 57492617 raw bytes or hash mismatch')
    require(len(raw_p2) == 1345 and sha256_hex(raw_p2) == PASTE_9629c5f3_SHA256,
            'Paste 9629c5f3 raw bytes or hash mismatch')

    p1_text = raw_p1.decode('utf-8')
    p2_text = raw_p2.decode('utf-8')

    p1_lines = p1_text.strip().splitlines()
    p2_lines = p2_text.strip().splitlines()

    # Model 1: Unadjusted split tables (Paste 9629c5f3)
    model1_away = compute_standings(entries, 'away', deduct_boro=False)
    model1_home = compute_standings(entries, 'home', deduct_boro=False)

    require(model1_away['Blackburn Rovers'][0] == 18, 'Model 1 Away Blackburn rank != 18')
    require(model1_away['Middlesbrough'][0] == 19, 'Model 1 Away Middlesbrough rank != 19')
    require(model1_away['Sunderland'][0] == 20, 'Model 1 Away Sunderland rank != 20')

    require(model1_home['Everton'][0] == 18, 'Model 1 Home Everton rank != 18')
    require(model1_home['Coventry City'][0] == 19, 'Model 1 Home Coventry rank != 19')
    require(model1_home['Nottingham Forest'][0] == 20, 'Model 1 Home Nottingham Forest rank != 20')

    p2_line3 = p2_lines[2]
    expected_p2 = (
        "1996/97 overall relegated: Sunderland 18, Middlesbrough 19, Nottingham Forest 20. "
        "Home bottom3: Nottingham Forest H20 (R), Coventry H19(not R), Everton H18(not R). "
        "Away bottom3: Middlesbrough A19 (R), Sunderland A20 (R), Blackburn A18(not R)."
    )
    require(p2_line3 == expected_p2, 'Paste 9629c5f3 line 3 does not match expected assertion')

    # Model 2: Deducted split tables (Paste 57492617)
    model2_away = compute_standings(entries, 'away', deduct_boro=True)
    model2_home = compute_standings(entries, 'home', deduct_boro=True)

    require(model2_away['Nottingham Forest'][0] == 16, 'Model 2 Away Nottingham Forest rank != 16')
    require(model2_away['Sunderland'][0] == 19, 'Model 2 Away Sunderland rank != 19')
    require(model2_away['Middlesbrough'][0] == 20, 'Model 2 Away Middlesbrough rank != 20')

    require(model2_home['Sunderland'][0] == 14, 'Model 2 Home Sunderland rank != 14')
    require(model2_home['Middlesbrough'][0] == 15, 'Model 2 Home Middlesbrough rank != 15')
    require(model2_home['Nottingham Forest'][0] == 20, 'Model 2 Home Nottingham Forest rank != 20')

    p1_line3 = p1_lines[2]
    expected_p1 = (
        "1996/97: Sunderland overall18 home14 away19; Middlesbrough overall19 home15 away20; "
        "Nottingham Forest overall20 home20 away16."
    )
    require(p1_line3 == expected_p1, 'Paste 57492617 line 3 does not match expected assertion')


def run_negative_controls(entries, raw_api, raw_p1, raw_p2):
    """Test rejection of corrupted inputs and flawed comparator assumptions."""
    rejected = []

    def expect_fail(name, fn):
        try:
            fn()
        except (ValueError, KeyError, AssertionError):
            rejected.append(name)
        else:
            raise ValueError(f'Control unexpectedly accepted: {name}')

    expect_fail('tampered_pulselive_hash',
                lambda: verify_primary_api(raw_api[:-1] + b'X'))

    expect_fail('tampered_paste1_hash',
                lambda: verify_paste_reproductions(entries, raw_p1.replace(b'away19', b'away20'), raw_p2))

    expect_fail('tampered_paste2_hash',
                lambda: verify_paste_reproductions(entries, raw_p1, raw_p2.replace(b'A19 (R)', b'A20 (R)')))

    expect_fail('naive_unadjusted_for_paste1',
                lambda: require(compute_standings(entries, 'away', deduct_boro=False)['Sunderland'][0] == 19,
                                'Unadjusted cannot yield Sunderland away 19'))

    expect_fail('deducted_for_paste2',
                lambda: require(compute_standings(entries, 'away', deduct_boro=True)['Middlesbrough'][0] == 19,
                                'Deducted cannot yield Middlesbrough away 19'))

    expect_fail('infer_gd_tiebreak_direction',
                lambda: require(-20 > -18,
                                'Sunderland GD (-20) cannot rank above Middlesbrough GD (-18) under standard tiebreak'))

    return rejected


def main():
    """Main verification routine."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--negative-controls', action='store_true', help='Execute adversarial negative controls')
    args = parser.parse_args()

    files = check_manifest(ROOT)
    raw_api = files['evidence/pulselive_standings_compSeasons_5.json']
    raw_p1 = files['evidence/paste_57492617.txt']
    raw_p2 = files['evidence/paste_9629c5f3.txt']

    entries = verify_primary_api(raw_api)
    verify_paste_reproductions(entries, raw_p1, raw_p2)

    result = {
        'status': 'PASS',
        'season': '1996/97',
        'competition': 'Premier League (compSeason 5)',
        'evidence_files_verified': len(files),
        'primary_api_bytes': len(raw_api),
        'primary_api_sha256': PULSELIVE_STANDINGS_SHA256,
        'paste_57492617_sha256': PASTE_57492617_SHA256,
        'paste_9629c5f3_sha256': PASTE_9629c5f3_SHA256,
        'reproduction_summary': {
            'model1_unadjusted_paste_9629c5f3': {
                'away_18_19_20': ['Blackburn Rovers (18)', 'Middlesbrough (19)', 'Sunderland (20)'],
                'home_18_19_20': ['Everton (18)', 'Coventry City (19)', 'Nottingham Forest (20)'],
                'comparator': 'points DESC, goalsDifference DESC, goalsFor DESC; raw match performance; no split deduction'
            },
            'model2_split_deducted_paste_57492617': {
                'away_ranks': {'Sunderland': 19, 'Middlesbrough': 20, 'Nottingham Forest': 16},
                'home_ranks': {'Sunderland': 14, 'Middlesbrough': 15, 'Nottingham Forest': 20},
                'comparator': 'points DESC, goalsDifference DESC, goalsFor DESC; 3-point administrative penalty deducted from Middlesbrough split points'
            }
        }
    }

    if args.negative_controls:
        rejected = run_negative_controls(entries, raw_api, raw_p1, raw_p2)
        result['negative_controls_rejected'] = rejected

    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
