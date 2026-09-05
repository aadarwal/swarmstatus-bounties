#!/usr/bin/env python3
"""Offline evidence/semantic verification. Standard library only; no file writes."""
import argparse
from collections import Counter
from copy import deepcopy
from datetime import datetime
import hashlib
import json
from pathlib import Path
import struct
from urllib.parse import parse_qsl, urlsplit

ROOT = Path(__file__).resolve().parent
TB = 'evidence/tb-series.json'
CONFIG = 'evidence/tb-config.json'
PNG = 'evidence/aihw-figure5-proportion.png'
TB_HASH = '465bf8370140b491c6648b5917e976e21b4f285bed6ea2b7a9025634fad0ba0e'
CONFIG_HASH = '91996caed64d2375fe68d729581c0c2ba9653cd625ed76136489804215fe800b'
PNG_HASH = 'a634c746bc2c2e78a360034a359dd1c7f07ec08490b4b173bd0a86f44366e316'
TB_PATH = '/lbd/api/v1/themes/tb/schemas/annual_mort/info/aggregate/components/'
AIHW_PATH = '/t/Public/views/AGE115_MentalhealthinAgedCare_19072024/F05-Age-specificcruderates'

def require(ok, why):
    if not ok:
        raise ValueError(why)

def digest(body):
    return hashlib.sha256(body).hexdigest()

def query(url):
    # Split first. Decoding the entire query first incorrectly promotes encoded ampersands.
    return parse_qsl(urlsplit(url).query, keep_blank_values=True)

def check_tb_url(url, year, sex='1', component='1'):
    u = urlsplit(url)
    require(u.scheme == 'https' and u.netloc == 'vizhub.healthdata.org', 'TB source host')
    require(u.path == TB_PATH + component, 'TB resource/component')
    expected = {'location_id':'66', 'measure':'mort', 'sex':sex, 'age':'10', 'stat':'mean', 'year_mort':str(year)}
    pairs = query(url)
    require(len(pairs) == 6 and dict(pairs) == expected, 'TB exact six filters')

def check_aihw_url(url, png=True):
    u = urlsplit(url)
    require(u.scheme == 'https' and u.netloc == 'viz.aihw.gov.au', 'AIHW source host')
    require(u.path == AIHW_PATH + ('.png' if png else ''), 'AIHW workbook/sheet')
    pairs = query(url)
    for name, value in [('Cohort', 'Permanent residential aged care'), ('Condition','Mood disorders')]:
        require([v for k,v in pairs if k == name] == [value], 'AIHW exact ' + name)

def check_series(obj):
    require(isinstance(obj,list) and len(obj)==1 and isinstance(obj[0],list) and len(obj[0])==54, 'TB 54-row nested series schema')
    lookup = {}
    for row in obj[0]:
        require(isinstance(row,dict) and set(row)=={'year_mort','stat','value'}, 'TB series row schema')
        require(isinstance(row['year_mort'],str) and row['year_mort'].isdigit(), 'TB year type')
        require(type(row['value']) in (int,float), 'TB numeric values')
        key = (int(row['year_mort']),row['stat'])
        require(key not in lookup, 'TB duplicate year/stat')
        lookup[key] = row['value']
    require(set(lookup)=={(y,s) for y in range(2000,2018) for s in ('lower','mean','upper')}, 'TB complete years/statistics')
    for y in range(2000,2018):
        require(lookup[y,'lower'] <= lookup[y,'mean'] <= lookup[y,'upper'], 'TB interval ordering')
    require(tuple(lookup[2000,s] for s in ('lower','mean','upper')) == (9.22879,11.438,13.6907), 'TB 2000 values')
    require(tuple(lookup[2010,s] for s in ('lower','mean','upper')) == (5.72293,7.32944,9.12279), 'TB 2010 values')
    return lookup

def check_component(obj, lookup, year):
    require(isinstance(obj,list) and len(obj)==1 and isinstance(obj[0],list) and len(obj[0])==3, 'TB component0 schema')
    require(all(isinstance(r,dict) and set(r)=={'stat','value'} for r in obj[0]), 'TB component0 row schema')
    values = {r['stat']:r['value'] for r in obj[0]}
    require(values == {s:lookup[year,s] for s in ('lower','mean','upper')}, 'TB component0 year/stat agreement')

def check_config(obj):
    require(obj['name']=='tb', 'TB config theme')
    dimensions = {d['name']:d for d in obj['dimensions']}
    options = lambda name: {r['name']:r['display_name'] for r in dimensions[name]['options']}
    require(options('sex')=={'1':'Male','2':'Female'}, 'TB sex labels')
    require(options('age')['10']=='25 - 29 years', 'TB age label')
    require(options('stat')=={'upper':'Upper (97.5% UI)','mean':'Mean','lower':'Lower (2.5% UI)'}, 'TB statistics labels')
    mortality = [s for s in obj['schemas'] if s['name']=='annual_mort']
    require(len(mortality)==1, 'TB annual_mort schema unique')
    schema = mortality[0]
    require(schema['conditions']=={'measure':['mort']}, 'TB mortality schema condition')
    require(schema['dimensions']==['measure','sex','age','stat','year_mort'], 'TB dimensions')
    require(schema['info_displays'][0]=={'type':'values','expand_dimension':'stat'}, 'TB component0 meaning')
    require(schema['info_displays'][1]=={'type':'line_chart','domain':'year_mort','area':{'line':'mean','lower':'lower','upper':'upper','expand_dimension':'stat'}}, 'TB component1 year/stat expansion')
    scales = [s for s in obj['color_scales'] if s['conditions']=={'measure':['mort']}]
    require(len(scales)==1 and scales[0]['legend_label']=='Mortality (per 100,000)', 'TB mortality units')

def check_receipt(receipt):
    require(receipt['report_url']=='https://urlquery.net/report/'+receipt['report_id'], 'Receipt source ID')
    require(receipt['json_url']==receipt['report_url']+'/json', 'Receipt JSON source')
    require(receipt['parsed_query_pairs']==[list(x) for x in query(receipt['request_url'])], 'Receipt original query parsing')
    require(receipt['report_date'] != receipt['transaction_date'], 'Distinct receipt/report clocks')
    for field in ('report_date','transaction_date'):
        require(datetime.fromisoformat(receipt[field].replace('Z','+00:00')).tzinfo is not None, 'Zoned receipt clock')

def check_malformed(receipt):
    check_receipt(receipt)
    require(query(receipt['request_url'])==[('location_id','66&measure=mort&sex=1&age=10&stat=mean&year_mort=2000')], 'Malformed request must remain one value')
    require(receipt['response_status_code']=='400' and receipt['response_bytes']==138, 'Malformed response is error HTML')

def check_hash(body, expected):
    require(digest(body)==expected, 'Artifact SHA-256 mismatch')

def verify(root):
    manifest = json.loads((root/'manifest.json').read_text())
    blobs = {}
    for name, spec in manifest['files'].items():
        path = (root/name).resolve()
        require(path.is_relative_to(root.resolve()), 'Manifest path escaped package')
        blobs[name] = path.read_bytes()
        require(len(blobs[name])==spec['bytes'], 'Artifact length: '+name)
        check_hash(blobs[name],spec['sha256'])
    read = lambda name: json.loads(blobs['evidence/'+name])
    for path, sha in [(TB,TB_HASH),(CONFIG,CONFIG_HASH),(PNG,PNG_HASH)]:
        check_hash(blobs[path],sha)
    lookup = check_series(json.loads(blobs[TB]))
    config = json.loads(blobs[CONFIG]); check_config(config)
    for y in (2000,2010):
        check_component(read('tb-%s-component0.json'%y),lookup,y)
    receipts = read('primary-receipts.json')
    require(len(receipts)==6, 'Six selected transactions')
    index = {(r['report_id'],r['transaction_index_zero_based']):r for r in receipts}
    require(len(index)==6, 'Selected receipt keys unique')
    for r in receipts: check_receipt(r)
    for rid,year in [('080803aa-5bc2-4147-9e8c-3ba881d40757',2000),('b9cdcab5-0c79-4654-acb9-bbd5a320057d',2010)]:
        r=index[rid,0]; check_tb_url(r['request_url'],year)
        require(r['request_method']=='GET' and r['response_status_code']=='200' and r['response_bytes']==2789 and r['response_sha256']==TB_HASH, 'TB historical successful body match')
        require(r['provider_body_available'] is False, 'TB body recovered independently from publisher')
    malformed=index['1f80ebe0-2cc2-40de-82a1-c415c5e4a217',0]; check_malformed(malformed)
    for i,status,size in [(4,'403',6632),(9,'200',71515),(11,'302',0)]:
        r=index['66e46234-179e-4214-ada1-fc3ed344d1ae',i]; check_aihw_url(r['request_url'])
        require((r['response_status_code'],r['response_bytes'])==(status,size), 'AIHW distinct transaction outcomes')
    r=index['66e46234-179e-4214-ada1-fc3ed344d1ae',9]
    require(r['response_sha256']==PNG_HASH and r['provider_body_available'] is False, 'AIHW historical byte match')
    require(blobs[PNG][:8]==b'\x89PNG\r\n\x1a\n' and struct.unpack('>II',blobs[PNG][16:24])==(800,550), 'AIHW image geometry')
    observation=read('aihw-mode-observation.json')
    require(observation['artifact_sha256']==PNG_HASH and observation['selected_measure']=='Proportion of people' and observation['unselected_measure']=='Age-and-sex-specific crude rate (per 1,000)' and observation['axis']=='Per cent', 'AIHW visual transcription distinguished from alternate measure')
    require(observation['independent_task_origin_publication'] is False, 'AIHW source does not establish task origin')
    acquisitions=read('acquisitions.json')
    for a in acquisitions:
        require(datetime.fromisoformat(a['acquired_at_utc']).tzinfo is not None, 'Acquisition clock timezone')
        if a['retained_form']=='unchanged bytes':
            require(digest(blobs[a['artifact_path']])==a['original_sha256'] and len(blobs[a['artifact_path']])==a['original_bytes'], 'Current acquisition bytes')
        else:
            require(a['artifact_path']=='evidence/tb-location-extract.json', 'Only location hierarchy is excerpted')
    for y in (2000,2010):
        for component,filename in [('1','tb-%s.json'%y),('0','tb-%s-component0.json'%y)]:
            found=[a for a in acquisitions if a['source_file_name']==filename]
            require(len(found)==1, 'TB acquisition mapping')
            check_tb_url(found[0]['url'],y,component=component)
    png_capture=next(a for a in acquisitions if a['artifact_path']==PNG)
    check_aihw_url(png_capture['url'],png=False)
    require(png_capture['status'] is None and png_capture['http_status_caveat'], 'UI download does not invent HTTP status')
    location=read('tb-location-extract.json')
    require(location['fields']=={'name':'Ecuador','location_id':'66','has_aggregate_data':True}, 'TB current location mapping')
    require(location['json_pointer']=='/children/7' and location['source_sha256']=='20bfc2d0abe61d29787b8d42130cc0d1f2771eca184a3f55c1d38653144bd8c4', 'Location original source anchor')
    wiki=read('wiki-claim-excerpts.json')
    require([w['id'] for w in wiki]==['20305c8f41f63092aba719f60c9e5314','d0c99878be32fc1895ac496fd7c98272'], 'Wiki exact record IDs')
    require(all(w['excerpt_is_full_body'] is False and w['time_basis']=='source_export_reqlog' for w in wiki), 'Wiki excerpt/time scope')
    require(wiki[0]['excerpt']=='Male Ecuador' and wiki[1]['excerpt']=='Data exported for Ecuador mortality rates in age 25 to 29 by sex.', 'Wiki factual claim excerpts')
    require(len(wiki[0]['literal_link_pairs'])==2, 'Wiki two sex labels')
    for pair,sex,label in zip(wiki[0]['literal_link_pairs'],['1','2'],['Male Ecuador','Female Ecuador']):
        require(pair['label']==label,'Wiki literal label'); check_tb_url(pair['url'],2000,sex=sex)
    ledger=read('historical-hash-joins.json'); counts=Counter(); keys=set()
    for r in ledger:
        key=(r['report_id'],r['transaction_index_zero_based'])
        require(key not in keys,'Duplicate historical transaction'); keys.add(key)
        require(r['response_status_code']=='200' and r['provider_body_available'] is False,'Historical hash match is recorded successful response, not retained provider body')
        require(r['report_url']=='https://urlquery.net/report/'+r['report_id'] and r['json_url']==r['report_url']+'/json','Historical locator')
        require(len(r['matching_artifact_paths'])==1,'One unique byte artifact per historical transaction')
        for path in r['matching_artifact_paths']:
            require(path in (TB,CONFIG,PNG),'Historical artifact scope')
            require(r['response_sha256']==digest(blobs[path]) and r['response_bytes']==len(blobs[path]),'Historical hash/length correspondence')
            counts[path]+=1
    require(len(keys)==203 and counts=={TB:16,CONFIG:174,PNG:13},'Historical distinct transaction counts')
    totals=read('historical-counts.json')
    require((totals['distinct_transactions'],totals['tb_series'],totals['tb_config'],totals['aihw_png'])==(203,16,174,13),'Stored counts agree ledger')
    require(totals['task_count_inference'] is None,'No request-to-task count inference')
    refs=read('aihw-referrer-urls.json')
    require(len(refs)==2 and all(r['time_utc'] is None and 'Cohort=' not in r['body'] and 'Condition=' not in r['body'] for r in refs),'Referrer URLs lack full filters/date')
    return {'status':'PASS','manifest_files':len(blobs),'tb_series_rows':54,'tb_years':[2000,2017], 'tb_mean_rates_per_100000':{'2000':lookup[2000,'mean'],'2010':lookup[2010,'mean']},'historical_unique_transactions':203,'historical_matches':dict(counts),'aihw_png_dimensions':[800,550], 'scope':'Checks packaged bytes, selected source excerpts and exported join ledger; does not reconstruct omitted full corpus, wiki bodies, location hierarchy or visual interpretation.'}, blobs, receipts, config

def negative_controls(blobs,receipts,config):
    cases=[]
    def reject(name,fn):
        try: fn()
        except (ValueError,KeyError,TypeError,IndexError): cases.append(name)
        else: raise ValueError('Negative control accepted: '+name)
    reject('tampered response bytes',lambda:check_hash(blobs[TB]+b' ',TB_HASH))
    valid=receipts[0]['request_url']
    reject('wrong sex filter',lambda:check_tb_url(valid.replace('sex=1','sex=2'),2000))
    reject('wrong requested year',lambda:check_tb_url(valid.replace('year_mort=2000','year_mort=2010'),2000))
    series=json.loads(blobs[TB]); altered=deepcopy(series); altered[0][0]['year']=altered[0][0].pop('year_mort')
    reject('wrong response schema',lambda:check_series(altered))
    altered=deepcopy(series); altered[0][0]['year_mort']='1999'
    reject('out-of-range response year',lambda:check_series(altered))
    badconfig=deepcopy(config); badconfig['color_scales'][0]['legend_label']='Mortality (per 1,000)'
    reject('wrong mortality denominator',lambda:check_config(badconfig))
    malformed=deepcopy(next(r for r in receipts if r['response_status_code']=='400'))
    malformed['request_url']=malformed['request_url'].replace('%26','&')
    malformed['parsed_query_pairs']=[list(x) for x in query(malformed['request_url'])]
    reject('encoded ampersands promoted to parameters',lambda:check_malformed(malformed))
    png=next(r['request_url'] for r in receipts if r['response_sha256']==PNG_HASH)
    reject('wrong AIHW condition',lambda:check_aihw_url(png.replace('Mood%20disorders','Anxiety%20disorders')))
    return {'rejected':len(cases),'cases':cases}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--negative-controls',action='store_true',help='Run in-memory tampering controls; does not write files')
    args=parser.parse_args()
    try:
        result,blobs,receipts,config=verify(ROOT)
        if args.negative_controls: result['negative_controls']=negative_controls(blobs,receipts,config)
        print(json.dumps(result,indent=2))
    except (ValueError,KeyError,TypeError,IndexError,OSError) as error:
        print(json.dumps({'status':'FAIL','error':str(error)},indent=2))
        raise SystemExit(1)
