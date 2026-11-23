"""Deterministic, fictional workforce data for demonstration only."""
from pathlib import Path
import csv, random, datetime
R=random.Random(42); ROOT=Path(__file__).parent; D=ROOT/'data'; D.mkdir(exist_ok=True)
markets=['San Antonio','Dallas–Fort Worth','Houston','Austin','Phoenix','Atlanta']
specialties=['ICU RN','ER RN','OR RN','Med-Surg RN','Respiratory Therapist','Physical Therapist']
rows=[]
for mi,m in enumerate(markets):
 for si,s in enumerate(specialties):
  demand=R.randint(14,85); supply=R.randint(7,75); filled=R.randint(10,90)
  rows.append(dict(market=m,specialty=s,open_requests=demand,available_candidates=supply,filled_last_90d=filled,requests_last_90d=filled+R.randint(3,35),median_days_to_fill=R.randint(12,49),avg_bill_rate=R.randint(90,175),avg_pay_rate=R.randint(55,120)))
with (D/'market_snapshot.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
certs={'ICU RN':'BLS;ACLS;CCRN','ER RN':'BLS;ACLS;PALS','OR RN':'BLS;CNOR','Med-Surg RN':'BLS','Respiratory Therapist':'BLS;RRT','Physical Therapist':'BLS;PT License'}
people=[]
for i in range(180):
 m=R.choice(markets);s=R.choice(specialties)
 people.append(dict(candidate_id=f'DEMO-{i+1:04}',market=m,specialty=s,years_experience=R.randint(1,18),certifications=certs[s],available_in_days=R.choice([0,7,14,21,30,45]),preferred_shift=R.choice(['Day','Night','Flexible']),willing_to_travel=R.choice(['Yes','No'])))
with (D/'synthetic_candidates.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=people[0]);w.writeheader();w.writerows(people)
