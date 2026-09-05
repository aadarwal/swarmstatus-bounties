#!/usr/bin/env python3
"""Verify this partial #33 package offline; stdlib only, no network or file writes."""
import argparse
from collections import Counter
from copy import deepcopy
from datetime import datetime
import hashlib
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parent
BASE='https://paste.linuxiarz.pl/view/'
PARENTS={'7d012d32':'34cb12da','d379207f':'34cb12da','b0924d89':'89a3961d','59c84c78':'89a3961d','a43cd523':'89a3961d'}
PAIRS=[['7d012d32','b0924d89'],['d379207f','59c84c78']]
BODY_HASHES={'7d012d32':'5cf58fbb41910d29c900b8a7bd920670d86d0399e03f60e4e07db929dd871a27','b0924d89':'5cf58fbb41910d29c900b8a7bd920670d86d0399e03f60e4e07db929dd871a27','d379207f':'1d118617bd67c287e69b813660b9b586debddafeb7570e8162b31918131eabe5','59c84c78':'1d118617bd67c287e69b813660b9b586debddafeb7570e8162b31918131eabe5','34cb12da':'2d711642b726b04401627ca9fbac32f5c8530fb1903cc4db02258717921a4881','89a3961d':'07dd7893c51017685f1b46cb89038c6e4962c7655a772c591dc7bec91984378b','a43cd523':'68e4446b95be44481238083dd67106207d0a530bbe448dd948f9f0df9cf2f4ab'}

def require(ok, why):
    if not ok: raise ValueError(why)
def sha(body): return hashlib.sha256(body).hexdigest()
def check_file(body,spec,name):
    require(len(body)==spec['bytes'] and sha(body)==spec['sha256'],'Packaged file hash/length mismatch: '+name)
class Links(HTMLParser):
    def __init__(self): super().__init__(convert_charrefs=True); self.links=[]; self.current=None
    def handle_starttag(self,tag,attrs):
        if tag=='a':
            require(self.current is None,'Nested anchors are not a valid literal packet')
            self.current={'url':dict(attrs).get('href'),'label':''}
    def handle_data(self,data):
        if self.current is not None: self.current['label']+=data
    def handle_endtag(self,tag):
        if tag=='a' and self.current is not None: self.links.append(self.current);self.current=None

def links(text):
    parser=Links();parser.feed(text);parser.close();require(parser.current is None,'Unclosed anchor');return parser.links

def check_pairs(bodies):
    for a,b in PAIRS: require(bodies[a]==bodies[b],'Exact paired body differs')
    require(bodies['7d012d32']!=bodies['d379207f'],'API and report blocks falsely merged')
    require(bodies['a43cd523'] not in (bodies['7d012d32'],bodies['d379207f']),'RefNX falsely paired')
    for key,text in [('34cb12da','x'),('89a3961d','SHIFT8')]:
        require(bodies[key]==text,'Filler control must remain exact')
        require(not links(bodies[key]),'Filler unexpectedly contains task URL')

def check_packets(bodies):
    api=links(bodies['7d012d32'])
    expected=[('ACCGET','https://api.usaspending.gov/api/v2/federal_accounts/075-8005/'),('ACCGET23','https://api.usaspending.gov/api/v2/federal_accounts/075-8005/?fiscal_year=2023'),('SNAP23','https://api.usaspending.gov/api/v2/federal_accounts/5599/fiscal_year_snapshot/2023/'),('QEND','https://api.usaspending.gov/api/v1/tas/balances/quarters/total/')]
    require([(r['label'],r['url']) for r in api]==expected,'Four-link API order/identifier/query mismatch')
    report=links(bodies['d379207f'])
    parent='https://portal.max.gov/portal/document/SF133/Budget/attachments/2346466575/'
    q2=parent+'2374423602.pdf';q3=parent+'2398882076.pdf'
    expected=[('Q2MDSCHEMELESS','https://markdown.new/'+q2.removeprefix('https://')),('Q3MDSCHEMELESS','https://markdown.new/'+q3.removeprefix('https://')),('Q2DIRECT',q2),('Q3DIRECT',q3),('Q2MDFULL','https://markdown.new/'+q2),('Q2CORS','https://test.cors.workers.dev/?'+q2),('Q2AO','https://allorigins.hexlet.app/raw?url='+q2)]
    require([(r['label'],r['url']) for r in report]==expected,'Seven-link SF133 order/attachment/wrapper mismatch')
    nx=links(bodies['a43cd523'])
    require([r['label'] for r in nx]==['HHSXAO','HHSZIP','GVIEWQ'],'RefNX distinct three-link packet')
    require(nx[2]['url']=='https://docs.google.com/gview?embedded=1%26url=https%3A%2F%2Fportal.max.gov%2Fportal%2Fdocument%2FSF133%2FBudget%2Fattachments%2F2346466575%2F2354356491.xlsx','RefNX literal encoded query must not be rewritten')

def check_relations(pastes,excerpts):
    for child,parent in PARENTS.items():
        item=pastes[child]
        require(item['native_parent_url']==BASE+parent,'Wrong declared native parent')
        part=excerpts[item['parent_excerpt_id']]
        require(part['kind']=='native_parent_assertion' and part['paste_id']==child,'Parent assertion excerpt provenance')
        parsed=links(part['text'])
        require(part['text'].startswith('This paste is a reply to ') and len(parsed)==1 and parsed[0]['url']==BASE+parent,'Native reply assertion differs')
    for parent,expected_children in [('34cb12da',{'7d012d32','d379207f'}),('89a3961d',{'b0924d89','59c84c78','a43cd523'})]:
        heading=excerpts[pastes[parent]['reply_heading_excerpt_id']]
        require(heading['kind']=='native_replies_heading' and heading['paste_id']==parent and heading['text'].startswith('<div class="replies">') and ('Replies to '+pastes[parent]['title']) in heading['text'],'Native reply section heading')
        part=excerpts[pastes[parent]['reply_table_excerpt_id']]
        require(heading['end_byte_exclusive']<=part['start_byte_zero_based'],'Heading precedes reply table in original bytes')
        require(part['kind']=='native_replies_table' and part['paste_id']==parent,'Reply table excerpt provenance')
        require(part['text'].startswith('<table class="recent">') and part['text'].endswith('</table>'),'Native table excerpt shape')
        parsed=links(part['text'])
        require(Counter(r['url'] for r in parsed)==Counter(BASE+k for k in expected_children),'Reciprocal reply rows differ')
        require(pastes[parent]['native_parent_url'] is None,'Unexpected filler-parent assertion')

def verify(root):
    manifest=json.loads((root/'manifest.json').read_text());blobs={}
    for name,spec in manifest['files'].items():
        path=(root/name).resolve();require(path.is_relative_to(root.resolve()),'Manifest path escaped package')
        body=path.read_bytes();check_file(body,spec,name);blobs[name]=body
    read=lambda name:json.loads(blobs['evidence/'+name])
    pastes={p['paste_id']:p for p in read('pastes.json')}
    captures={p['paste_id']:p for p in read('captures.json')}
    excerpts={e['excerpt_id']:e for e in read('excerpts.json')}
    claims=read('claims.json')
    require(len(pastes)==7 and set(pastes)==set(BODY_HASHES) and set(captures)==set(pastes),'Seven exact paste IDs')
    require(len(excerpts)==16,'Sixteen excerpt objects')
    for part in excerpts.values():
        b=part['text'].encode();cap=captures[part['paste_id']]
        require(len(b)==part['excerpt_bytes'] and sha(b)==part['excerpt_sha256'],'Literal excerpt integrity')
        require(part['whole_capture_sha256']==cap['whole_capture_sha256'],'Excerpt whole-capture provenance anchor')
        require(0<=part['start_byte_zero_based']<part['end_byte_exclusive']<=cap['whole_capture_bytes'],'Excerpt offset bounds')
        require(part['end_byte_exclusive']-part['start_byte_zero_based']==len(b),'Excerpt byte range length')
    bodies={}
    for key,p in pastes.items():
        cap=captures[key]
        require(p['source_url']==cap['source_url']==cap['final_url']==BASE+key,'Source locator/paste ID mismatch')
        require(cap['http_status']==200 and cap['whole_capture_included'] is False,'Whole source is provenance only')
        require(datetime.fromisoformat(cap['acquired_at_utc']).tzinfo is not None,'Capture time must be zoned')
        require(p['publication_time_utc'] is None and cap['source_publication_time_utc'] is None and p['displayed_relative_age']=='3 Months ago','Relative age must not become publication date')
        body=blobs[p['body_path']];require(sha(body)==p['body_sha256']==BODY_HASHES[key],'Body fingerprint mismatch')
        bodies[key]=body.decode()
        part=excerpts[p['textarea_excerpt_id']]
        require(part['paste_id']==key and part['kind']=='textarea_code','Textarea provenance')
        match=re.fullmatch(r'<textarea\b[^>]*\bid="code"[^>]*>(.*?)</textarea>',part['text'],re.S)
        require(match is not None and html.unescape(match.group(1))==bodies[key],'One-decode textarea body differs')
        require(links(bodies[key])==p['ordered_links'],'Preserved literal URL/label order differs')
    check_pairs(bodies);check_packets(bodies);check_relations(pastes,excerpts)
    require(claims['expected_parents']==PARENTS and claims['expected_body_pairs']==PAIRS,'Claim graph/pairs differ')
    require(claims['bounty']==33 and claims['historical_creation_times_recovered']==0 and claims['independently_dated_template_recovered'] is False,'Partial status/dating overclaim')
    require(pastes['34cb12da']['full_corpus_record_ids']==[] and pastes['34cb12da']['focused_corpus_record_ids']==[],'x corpus novelty declaration')
    require(pastes['89a3961d']['full_corpus_record_ids']==['caf81e6954db5f753aa7ef8533c49d81'] and pastes['89a3961d']['focused_corpus_record_ids']==[],'SHIFT8 full/focused scope declaration')
    result={'status':'PASS','manifest_files':len(blobs),'pastes':7,'exact_excerpts':16,'native_relations':5,'exact_body_pairs':2,'filler_controls':2,'body_bytes':{k:len(v.encode()) for k,v in bodies.items()},'scope':'Verifies retained excerpts, their local hashes/ranges, literal decoded bodies and declared corpus scope. Cannot independently verify omitted whole HTML hashes, selection context or absent full corpus. No network/file writes.'}
    return result,bodies,pastes,excerpts,blobs

def controls(bodies,pastes,excerpts,blobs):
    rejected=[]
    def reject(name,fn):
        try:fn()
        except (ValueError,KeyError,TypeError,IndexError):rejected.append(name)
        else:raise ValueError('Negative control accepted: '+name)
    original=next(iter(blobs.values()));tampered=bytes([original[0]^1])+original[1:];reject('tampered retained bytes',lambda:check_file(tampered,{'bytes':len(original),'sha256':sha(original)},'in-memory control'))
    p=deepcopy(pastes);p['7d012d32']['native_parent_url']=BASE+'89a3961d';reject('swapped native parent',lambda:check_relations(p,excerpts))
    e=deepcopy(excerpts);key=pastes['34cb12da']['reply_table_excerpt_id'];e[key]['text']=e[key]['text'].replace('7d012d32','b0924d89');reject('altered reciprocal reply row',lambda:check_relations(pastes,e))
    b=deepcopy(bodies);b['7d012d32']=b['7d012d32'].replace('5599','5598');reject('altered account ID',lambda:check_packets(b))
    b=deepcopy(bodies);b['d379207f']=b['d379207f'].replace('2398882076','2398882077');reject('altered attachment ID',lambda:check_packets(b))
    b=deepcopy(bodies);rows=b['7d012d32'].splitlines(True);b['7d012d32']=''.join([rows[1],rows[0],*rows[2:]]);reject('URL label order swapped',lambda:check_packets(b))
    b=deepcopy(bodies);b['7d012d32']=b['7d012d32'].replace('075-8005','2357').replace('2023','2015');reject('different ordinary-document account/year example',lambda:check_packets(b))
    b=deepcopy(bodies);b['34cb12da']=b['7d012d32'];reject('filler promoted to task packet',lambda:check_pairs(b))
    b=deepcopy(bodies);b['a43cd523']=b['d379207f'];reject('distinct RefNX falsely paired',lambda:check_pairs(b))
    b=deepcopy(bodies);b['a43cd523']=b['a43cd523'].replace('embedded=1%26url=','embedded=1&url=');reject('embedded encoded delimiter rewritten',lambda:check_packets(b))
    return {'rejected':len(rejected),'cases':rejected,'method':'Synthetic in-memory alterations; does not fetch sources or modify package files.'}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--negative-controls',action='store_true');args=parser.parse_args()
    try:
        result,bodies,pastes,excerpts,blobs=verify(ROOT)
        if args.negative_controls:result['negative_controls']=controls(bodies,pastes,excerpts,blobs)
        print(json.dumps(result,indent=2))
    except (ValueError,KeyError,TypeError,IndexError,OSError) as error:
        print(json.dumps({'status':'FAIL','error':str(error)},indent=2));raise SystemExit(1)
