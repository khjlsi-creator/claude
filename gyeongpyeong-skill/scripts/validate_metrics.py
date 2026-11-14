#!/usr/bin/env python3
"""JSON fact-card arithmetic/duplicate checks; NOT source truth verification."""
import json,sys
from decimal import Decimal,InvalidOperation

def validate(records):
    errors=[]; seen={}
    for i,r in enumerate(records):
        key=tuple(str(r.get(k,'')) for k in ('institution','report_year','baseline_year','comparison_year','program','population','unit'))
        if any(not x for x in key): errors.append(f'{i}: incomplete metric identity')
        try:
            a=Decimal(str(r['baseline']));b=Decimal(str(r['actual']))
            if a==0: errors.append(f'{i}: zero baseline, percent change undefined')
            elif 'change_percent' in r and abs((b-a)/a*100-Decimal(str(r['change_percent'])))>Decimal('0.11'):
                errors.append(f'{i}: percentage mismatch')
        except (KeyError,InvalidOperation): errors.append(f'{i}: invalid numeric field')
        if key in seen:
            if (r.get('baseline'),r.get('actual')) != (seen[key].get('baseline'),seen[key].get('actual')):
                errors.append(f'{i}: conflicting values for duplicate metric key')
            else: errors.append(f'{i}: duplicate provenance; count only once')
        else: seen[key]=r
    return {'metric_rows':len(records),'unique_keys':len(seen),'issues':errors,'note':'Arithmetic and identity only; source authenticity and semantics require human review.'}
if __name__=='__main__':
    data=json.load(open(sys.argv[1],encoding='utf-8'))
    print(json.dumps(validate(data),ensure_ascii=False,indent=2))
