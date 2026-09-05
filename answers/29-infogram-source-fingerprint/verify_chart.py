#!/usr/bin/env python3
"""Parse captured source HTML as inert text and verify the retained factual table."""
import argparse
import copy
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path

UUID = '55eeebff-2501-4b78-979d-1c7c1e5c4f74'
SLUG = '1h1749vqy0p0l6z'

def infographic(path):
    text = path.read_text()
    assert text.count('window.infographicData=') == 1
    return json.JSONDecoder().raw_decode(text.split('window.infographicData=', 1)[1])[0]

class Embeds(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'div' and 'infogram-embed' in attrs.get('class', '').split():
            self.ids.append(attrs['data-id'])

def verify(chart, stored):
    assert chart['path'] == stored['source_uuid'] == UUID
    assert chart['publishedURLId'] == SLUG
    assert chart['createdAt'] == stored['source_created_at']
    assert chart['updatedAt'] == stored['source_updated_at']
    tables = [v['props']['chartData']['data'][0]
              for v in chart['elements']['content']['content']['entities'].values()
              if 'chartData' in v.get('props', {})]
    assert len(tables) == 1 and tables[0] == stored['rows']
    assert len(tables[0]) == 12
    row = next(row for row in tables[0] if row[0] == '2.0')
    assert row[1:3] == ['67', '26 (Amy Jackson)']
    return {'film_rows': 11, 'derived_2_0_gap': int(row[1])-int(row[2].split()[0])}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--canonical', type=Path, required=True)
    parser.add_argument('--embed', type=Path, required=True)
    parser.add_argument('--publisher', type=Path, required=True)
    parser.add_argument('--require-capture-hashes', action='store_true', help='Require exact September 5 source bytes')
    args = parser.parse_args()
    stored = json.loads(Path(__file__).with_name('chart-table.json').read_text())
    canonical, embed = infographic(args.canonical), infographic(args.embed)
    assert canonical == embed
    result = verify(embed, stored)
    page = Embeds()
    page.feed(args.publisher.read_text())
    assert len(page.ids) == 4 and page.ids.count(UUID) == 1
    for mutation in ['id', 'cell', 'declared_date']:
        changed = copy.deepcopy(stored)
        if mutation == 'id':
            changed['source_uuid'] = '0' * 32
        elif mutation == 'cell':
            changed['rows'][8][1] = '68'
        else:
            changed['source_created_at'] = '2000-01-01T00:00:00Z'
        try:
            verify(embed, changed)
        except AssertionError:
            pass
        else:
            raise AssertionError('Altered input accepted: ' + mutation)
    result.update(canonical_embed_equal=True, publisher_embeds_exact_uuid=True,
                  publisher_chart_ids=page.ids, altered_id_and_cell_rejected=True,
                  executed_page_code=False,
                  source_sha256={name:hashlib.sha256(getattr(args,name).read_bytes()).hexdigest()
                                 for name in ['canonical','embed','publisher']})
    metadata = {r['name']:r for r in json.loads(Path(__file__).with_name('capture-metadata.json').read_text())}
    names = {'canonical':'infogram', 'embed':'infogram-embed', 'publisher':'quint'}
    result['capture_hashes_match'] = all(result['source_sha256'][k] == metadata[v]['sha256'] for k,v in names.items())
    result['source_declared_dates_checked'] = True
    result['altered_declared_date_rejected'] = True
    if args.require_capture_hashes:
        assert result['capture_hashes_match'], 'Input bytes differ from September 5 captures'
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
