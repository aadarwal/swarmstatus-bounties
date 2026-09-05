#!/usr/bin/env python3
"""Offline retained-artifact checks; no network, private database or file writes."""
import argparse
from copy import deepcopy
from datetime import datetime
import hashlib
import json
from pathlib import Path
import struct
from urllib.parse import parse_qsl,urlsplit

ROOT=Path(__file__).resolve().parent
WORKBOOK='PBS-dashboard-AgeGroup-Monthly-date-20241128'
SHEET='PBSdashboard'
PNG_HASH='df10488dd47b56217f41afdab375dcda011bf24f3ecf018312e301c62078a680'

def require(ok,why):
    if not ok:raise ValueError(why)
def digest(b):return hashlib.sha256(b).hexdigest()
def check_file(body,spec):
    require(len(body)==spec['bytes'] and digest(body)==spec['sha256'],'Artifact hash/length mismatch')
def check_observations(obs):
    require(obs['workbook']==WORKBOOK and obs['sheet']==SHEET,'Exact old workbook/sheet')
    expected={'State/Territory':'Victoria','LGA':'Wodonga','ATC Level 1':'Dermatologicals'}
    require(obs['requested_query_values']==expected,'Exact requested filter values')
    for field in ['navigation_url','observed_final_view_url','historical_csv_request_url']:
        parsed=urlsplit(obs[field]);suffix='.csv' if field=='historical_csv_request_url' else ''
        require(parsed.scheme=='https' and parsed.netloc=='viz.aihw.gov.au' and parsed.path=='/t/Public/views/'+WORKBOOK+'/'+SHEET+suffix,'Exact first-party resource URL')
        pairs=parse_qsl(parsed.query,keep_blank_values=True)
        for key,value in expected.items():require([v for k,v in pairs if k==key]==[value],'Unchanged literal query constraint')
    require(obs['initial_visible_controls']=={'state_label':'Select State/Territory:','state':'Australia','lga_label':'Select an LGA:','lga':'All','years':'All years','measure':'Monthly data','atc1_medicine':'(All PBS prescriptions)'},'Initial UI transcription scope')
    require(obs['initial_export_visible_controls']['atc1_medicine']=='None' and obs['initial_export_visible_controls']['state']=='Australia' and obs['initial_export_visible_controls']['lga']=='All','Export transcription kept distinct from UI')
    require(obs['manual_selection_observation']['state']=='Victoria' and obs['manual_selection_observation']['lga']=='Wodonga' and obs['manual_selection_observation']['atc1_open_menu']=='No Items.','Manual UI observation scope')
    for key in ['workbook_name_date_is_publication_or_data_period','legacy_url_filters_visibly_honored','filter_processing_mechanism_known','dermatologicals_selected_or_exported','data_period_recovered','numeric_response_recovered','historical_response_bytes_recovered','cross_version_field_equivalence_proven','independent_historical_publication_recovered']:
        require(obs[key] is False,'Unsupported completion assertion: '+key)
    require(obs['status']=='partial; keep open' and obs['bounty']==15,'Partial bounty state')

def verify(root):
    manifest=json.loads((root/'manifest.json').read_text());blobs={}
    for name,spec in manifest['files'].items():
        path=(root/name).resolve();require(path.is_relative_to(root.resolve()),'Manifest escaped package')
        blobs[name]=path.read_bytes();check_file(blobs[name],spec)
    require(len(blobs)==9,'Nine retained evidence files')
    for name in ['initial-query.jpg','manual-victoria-wodonga-empty-medicine.jpg']:
        require(blobs['evidence/'+name][:3]==b'\xff\xd8\xff','Viewport screenshots must be JPEG bytes')
    obs=json.loads(blobs['evidence/observations.json']);check_observations(obs)
    image=blobs['evidence/pbs-default-export.png']
    require(image[:8]==b'\x89PNG\r\n\x1a\n' and struct.unpack('>II',image[16:24])==(800,1830),'Publisher PNG format/dimensions')
    require(digest(image)==PNG_HASH and len(image)==98272,'Publisher PNG pinned bytes')
    initial=blobs['evidence/initial-query.ax.txt'].decode();manual=blobs['evidence/manual-victoria-wodonga-empty-medicine.ax.txt'].decode();menu=blobs['evidence/victoria-lga-menu.ax.txt'].decode()
    require(WORKBOOK in initial and obs['observed_final_view_url'] in initial,'AX preserves exact source URL')
    for literal in ['Description: Select State/Territory: Australia','Description: Select an LGA: All','radio button All years, Value: 1','radio button Monthly data, Value: 1','Data is suppressed for this measure/geography combination']:
        require(literal in initial,'Initial AX value missing: '+literal)
    for literal in ['Description: Select State/Territory: Victoria','Description: Select a Victoria LGA: Wodonga','text No Items.','Data is suppressed for this measure/geography combination']:
        require(literal in manual,'Manual AX value missing: '+literal)
    require('text Ballarat' in menu and 'text Wodonga' in menu and 'Select a Victoria LGA:' in menu,'State-specific menu options')
    captures=json.loads(blobs['evidence/acquisitions.json']);require(len(captures)==6,'Six observed artifacts')
    for cap in captures:
        b=blobs[cap['artifact']];check_file(b,cap)
        require(cap['response_http_status'] is None,'Do not invent UI HTTP status')
        if cap['acquired_at_utc'] is not None:require(datetime.fromisoformat(cap['acquired_at_utc'].replace('Z','+00:00')).tzinfo is not None,'Acquisition clock timezone')
        else:require(cap['acquisition_interval_utc']==[obs['current_observation_times']['initial_observed_at_utc'],obs['current_observation_times']['final_observed_at_utc']],'Bounded menu clock')
    return {'status':'PASS','manifest_files':9,'publisher_png_bytes':98272,'publisher_png_dimensions':[800,1830],'exact_workbook':WORKBOOK,'selected_legacy_filters_verified':False,'historical_values_or_period_recovered':False,'issue_15':'keep open','scope':'Verifies packaged integrity, literal AX text, preserved query constraints and explicit observation limits. Visual PNG/control interpretation is an observer transcription, not OCR or independent historical authentication.'},obs,blobs

def negative_controls(obs,blobs):
    rejected=[]
    def reject(name,fn):
        try:fn()
        except (ValueError,KeyError,TypeError,IndexError):rejected.append(name)
        else:raise ValueError('Accepted negative control: '+name)
    b=blobs['evidence/pbs-default-export.png'];bad=bytes([b[0]^1])+b[1:]
    reject('tampered same-length image',lambda:check_file(bad,{'bytes':len(b),'sha256':digest(b)}))
    changed=deepcopy(obs);changed['workbook']=WORKBOOK.replace('20241128','20250430');reject('wrong workbook version',lambda:check_observations(changed))
    changed=deepcopy(obs);changed['requested_query_values']['LGA']='Ballarat';reject('wrong requested LGA',lambda:check_observations(changed))
    changed=deepcopy(obs);changed['legacy_url_filters_visibly_honored']=True;reject('unsupported filter success',lambda:check_observations(changed))
    changed=deepcopy(obs);changed['data_period_recovered']=True;reject('unsupported historical data period',lambda:check_observations(changed))
    return {'rejected':len(rejected),'cases':rejected}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--negative-controls',action='store_true');args=parser.parse_args()
    try:
        result,obs,blobs=verify(ROOT)
        if args.negative_controls:result['negative_controls']=negative_controls(obs,blobs)
        print(json.dumps(result,indent=2))
    except (ValueError,KeyError,TypeError,IndexError,OSError) as error:
        print(json.dumps({'status':'FAIL','error':str(error)},indent=2));raise SystemExit(1)
