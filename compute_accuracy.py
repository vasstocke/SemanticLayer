#!/usr/bin/env python3
import argparse, csv
from collections import defaultdict

WEIGHTS = {"interpretation": .25, "query_logic": .30, "result_accuracy": .30, "presentation": .10, "transparency": .05}
TRUE={"true","1","yes","y"}; FALSE={"false","0","no","n"}

def boolean(v):
    s=(v or '').strip().lower()
    if s in TRUE: return True
    if s in FALSE: return False
    return None

def quality(row):
    vals=[]
    for k,w in WEIGHTS.items():
        try: v=float(row[k])
        except (ValueError,KeyError): raise ValueError(f"Missing/non-numeric {k} for {row.get('question_id','?')}")
        if not 0 <= v <= 100: raise ValueError(f"{k} must be 0..100")
        vals.append(v*w)
    return sum(vals)

def compute(rows):
    groups=defaultdict(list)
    for r in rows:
        r['_quality']=quality(r)
        groups[r['configuration']].append(r)
    summaries=[]
    for config, rs in sorted(groups.items()):
        n=len(rs)
        strict=sum(boolean(r.get('strict_correct')) is True and boolean(r.get('critical_error')) is not True for r in rs)
        quality_avg=sum(r['_quality'] for r in rs)/n if n else 0
        safe_rows=[r for r in rs if r.get('question_type','').lower() in {'ambiguous','unanswerable'}]
        safe=sum(boolean(r.get('safe_response')) is True for r in safe_rows)
        valid=[r for r in rs if boolean(r.get('is_valid_question')) is True]
        covered=sum(boolean(r.get('appropriately_answered')) is True for r in valid)
        intents=defaultdict(list)
        for r in rs: intents[r['intent_id']].append(r)
        consistent=sum(all(boolean(x.get('strict_correct')) is True and boolean(x.get('critical_error')) is not True for x in xs) for xs in intents.values())
        summaries.append({
            'configuration':config,'answers':n,
            'strict_accuracy_pct':round(100*strict/n,2) if n else 0,
            'weighted_quality_pct':round(quality_avg,2),
            'consistent_accuracy_pct':round(100*consistent/len(intents),2) if intents else 0,
            'safe_response_rate_pct':round(100*safe/len(safe_rows),2) if safe_rows else '',
            'coverage_pct':round(100*covered/len(valid),2) if valid else '',
        })
    return summaries

def main():
    ap=argparse.ArgumentParser(description='Compute Talk-to-Your-Data benchmark accuracy metrics')
    ap.add_argument('csv_file'); ap.add_argument('--out')
    a=ap.parse_args()
    with open(a.csv_file,newline='',encoding='utf-8-sig') as f: rows=list(csv.DictReader(f))
    result=compute(rows)
    fields=list(result[0].keys()) if result else []
    if a.out and fields:
        with open(a.out,'w',newline='',encoding='utf-8') as f:
            w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(result)
    if fields:
        print('\t'.join(fields))
        for r in result: print('\t'.join(str(r[x]) for x in fields))

if __name__=='__main__': main()
