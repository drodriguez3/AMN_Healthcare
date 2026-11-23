"""IronGate Cortex AI experience: offline, transparent synthetic simulations."""
from pathlib import Path
import re
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
st.set_page_config(page_title='Healthcare Workforce Intelligence | IronGate', page_icon='◆', layout='wide')
st.markdown('''<style>.block-container{padding-top:1.4rem;max-width:1150px}.hero{background:linear-gradient(110deg,#10243a,#12657a);color:white;padding:28px 32px;border-radius:16px}.hero h1{color:white;margin:0}.hero p{color:#dbeaf2;margin:8px 0 0}.note{background:#fff4dd;padding:11px;border-left:4px solid #df9d25;border-radius:5px;margin:12px 0}.answer{background:#eaf6f3;border:1px solid #b7ded6;border-radius:13px;padding:22px 26px;margin:12px 0}.answer h3{margin-top:0;color:#123e40}.eyebrow{letter-spacing:.12em;text-transform:uppercase;color:#0b7974;font-weight:700;font-size:.8rem}.mini{background:#f1f5fa;border-radius:10px;padding:16px}</style>''',unsafe_allow_html=True)
st.markdown('<div class="hero"><h1>◆ Healthcare Workforce Intelligence | IronGate</h1><p>Ask a question. Get a sourced answer. Turn insight into an action plan.</p></div>',unsafe_allow_html=True)
st.markdown('<div class="note"><b>Offline concept demo.</b> All records and documents are fictional. Analyst, Search, and Agent behavior is simulated locally using deterministic logic; no live Snowflake Cortex, LLM, AMN systems, or real candidate data are connected.</div>',unsafe_allow_html=True)

@st.cache_data
def load():
    m = pd.read_csv(ROOT/'data/market_snapshot.csv')
    c = pd.read_csv(ROOT/'data/synthetic_candidates.csv')
    d = pd.read_csv(ROOT/'data/synthetic_knowledge.csv')
    m['gap'] = (m.open_requests-m.available_candidates).clip(lower=0)
    m['fill_rate'] = (100*m.filled_last_90d/m.requests_last_90d).round(1)
    return m,c,d
market,candidates,docs=load()

def filtered(market_name,specialty):
    x=market.copy()
    if market_name!='All':x=x[x.market.eq(market_name)]
    if specialty!='All':x=x[x.specialty.eq(specialty)]
    return x

def search_docs(query,kind='All'):
    terms=set(re.findall(r'[a-z0-9]+',query.lower()))-{'the','and','for','with','what','are','how','can','our','about','does'}
    d=docs if kind=='All' else docs[docs.doc_type.eq(kind)]
    scored=[]
    for _,row in d.iterrows():
        title=str(row.title).lower(); body=str(row.content).lower(); tags=str(row.tags).lower()
        score=sum(4*(t in title)+2*(t in tags)+(t in body) for t in terms)
        if score:scored.append((score,row))
    return sorted(scored,key=lambda v:v[0],reverse=True)[:5]

with st.sidebar:
    st.header('Demo controls')
    st.caption('Every example uses synthetic workforce data and fictional knowledge documents.')
    st.markdown('**Proposed Snowflake services**')
    st.write('• Cortex Analyst: governed questions → SQL')
    st.write('• Cortex Search: semantic / hybrid retrieval')
    st.write('• Cortex Agents: tool orchestration')
    st.caption('These are production integration targets, not connected services in this app.')

t1,t2,t3,t4=st.tabs(['01 · Ask your data','02 · Ask your documents','03 · AI recruiting copilot','04 · How it works'])
with t1:
    st.header('Ask questions about staffing operations')
    st.write('**Business scenario:** An operations leader asks a question in plain English. In production, Cortex Analyst would generate governed SQL against a Snowflake semantic view.')
    question=st.selectbox('Example business question',[
        'Where is the largest staffing shortfall?',
        'Which specialties are taking longest to fill?',
        'Where are historical fill rates lowest?',
        'Which markets have the most open requests?'])
    c1,c2=st.columns(2)
    m=c1.selectbox('Market',['All']+sorted(market.market.unique()),key='analyst_market')
    s=c2.selectbox('Specialty',['All']+sorted(market.specialty.unique()),key='analyst_specialty')
    x=filtered(m,s)
    if x.empty:st.warning('No rows match those filters.')
    else:
        if 'shortfall' in question:
            result=x.sort_values('gap',ascending=False)[['market','specialty','open_requests','available_candidates','gap']].head(8)
            answer=f"The largest illustrated gap is {result.iloc[0]['market']} / {result.iloc[0]['specialty']}: {int(result.iloc[0]['gap'])} positions."
            sql='SELECT market, specialty, open_requests, available_candidates, GREATEST(open_requests - available_candidates, 0) AS gap FROM WORKFORCE_SEMANTIC_VIEW ORDER BY gap DESC LIMIT 8;'
        elif 'longest' in question:
            result=x.sort_values('median_days_to_fill',ascending=False)[['market','specialty','median_days_to_fill']].head(8)
            answer=f"The longest illustrated median time to fill is {result.iloc[0]['median_days_to_fill']} days for {result.iloc[0]['specialty']} in {result.iloc[0]['market']}."
            sql='SELECT market, specialty, median_days_to_fill FROM WORKFORCE_SEMANTIC_VIEW ORDER BY median_days_to_fill DESC LIMIT 8;'
        elif 'lowest' in question:
            result=x.sort_values('fill_rate')[['market','specialty','fill_rate']].head(8)
            answer=f"The lowest illustrated historical fill rate is {result.iloc[0]['fill_rate']}% in {result.iloc[0]['market']} / {result.iloc[0]['specialty']}."
            sql='SELECT market, specialty, fill_rate FROM WORKFORCE_SEMANTIC_VIEW ORDER BY fill_rate ASC LIMIT 8;'
        else:
            result=x.sort_values('open_requests',ascending=False)[['market','specialty','open_requests']].head(8)
            answer=f"The largest illustrated open-request count is {int(result.iloc[0]['open_requests'])} in {result.iloc[0]['market']} / {result.iloc[0]['specialty']}."
            sql='SELECT market, specialty, open_requests FROM WORKFORCE_SEMANTIC_VIEW ORDER BY open_requests DESC LIMIT 8;'
        st.success(answer)
        st.dataframe(result,hide_index=True,use_container_width=True)
        with st.expander('Show illustrative SQL and explanation'):
            st.code(sql,language='sql')
            st.caption('SQL is an illustrative template, not generated by Cortex Analyst or executed against Snowflake. The demo calculates answers in pandas.')
def cite_doc(row):
    return f"[{row.doc_id}] {row.title}"

def answer_from_evidence(query,hits):
    """Deterministic evidence-based response, not an LLM or live RAG."""
    if not hits:
        return None, []
    q=query.lower()
    chosen=[row for _,row in hits[:3]]
    # Answer only what the fictional documents actually support.
    if ('icu' in q or 'intensive' in q) and any(r.doc_id=='DOC-101' for r in chosen):
        chosen=[next(r for _,r in hits if r.doc_id=='DOC-101')]+[r for r in chosen if r.doc_id!='DOC-101']
        message=("For the **fictional ICU RN role**, the checklist calls for an active state RN license, "
                 "BLS and ACLS documentation, and a review of recent ICU experience **[DOC-101]**. "
                 "For the San Antonio night-shift example, the role brief also calls for confirming "
                 "shift availability and any facility-specific requirements with the account owner **[DOC-106]**. "
                 "**Next step:** have an authorized credentialing specialist verify current documents before submission. "
                 "These example requirements are not a final eligibility determination.")
        extra=next((r for _,r in hits if r.doc_id=='DOC-106'),None)
        if extra is not None and all(r.doc_id != 'DOC-106' for r in chosen):
            chosen.append(extra)
    elif any(word in q for word in ['contact','outreach','approve','approval','submit']):
        policy=next((r for _,r in hits if r.doc_id=='DOC-105'),None)
        if policy:
            chosen=[policy]+[r for r in chosen if r.doc_id!=policy.doc_id]
            message=("The fictional recruiting policy requires a recruiter to review qualifications and "
                     "obtain appropriate approval **before outreach or assignment-status changes [DOC-105]**. "
                     "The assistant can prepare a recommended next step, but it cannot send messages or update records. "
                     "**Next step:** request recruiter review and approval.")
        else:message=f"The closest fictional source is **{chosen[0].title} [ {chosen[0].doc_id} ]**. Review the passage below; the corpus does not establish a complete answer."
    elif any(word in q for word in ['available','availability','travel']):
        policy=next((r for _,r in hits if r.doc_id=='DOC-104'),None)
        if policy:
            chosen=[policy]+[r for r in chosen if r.doc_id!=policy.doc_id]
            message=("Candidate availability is **self-reported and must be reconfirmed** before outreach or submission "
                     "**[DOC-104]**. Willingness to travel alone does not establish eligibility. "
                     "**Next step:** ask a recruiter to verify dates, preferences, and role requirements.")
        else:message=f"The most relevant fictional document is **{chosen[0].title} [{chosen[0].doc_id}]**. Review its source text below; no definitive answer is supported."
    else:
        message=(f"The strongest match is **{chosen[0].title} [{chosen[0].doc_id}]**. "
                 "Its documented guidance is: " + str(chosen[0].content) + " "
                 "**Next step:** verify applicability with the appropriate team; this is a limited fictional document set.")
    # Limit visible sources to those cited by the composed answer.
    cited=[r for r in chosen if f'[{r.doc_id}]' in message]
    return message, cited or chosen[:1]

with t2:
    st.markdown('<div class="eyebrow">Cortex Search + RAG experience</div>',unsafe_allow_html=True)
    st.header('An answer, not a list of documents')
    st.write('**Executive moment:** A recruiter asks one question and gets a clear, source-backed response with a recommended next step. No hunting through policy PDFs.')
    examples=['What certifications are needed for ICU nurses?',
              'Can we contact candidates before approval?',
              'How should we confirm candidate availability?',
              'What does the ER RN checklist require?']
    selected=st.selectbox('Try a real recruiting question',examples)
    query=st.text_input('Or enter your own question',value=selected,key='rag_question')
    if st.button('Get answer from knowledge',type='primary',key='rag_go'):
        st.session_state['rag_query']=query
    if 'rag_query' in st.session_state:
        q=st.session_state['rag_query']
        hits=search_docs(q)
        answer,sources=answer_from_evidence(q,hits)
        if not answer:st.warning('I could not find supporting information in the sample knowledge base. Try a sample question; I will not invent an answer.')
        else:
            st.markdown('<div class="eyebrow">Illustrative AI answer · evidence-grounded simulation</div>',unsafe_allow_html=True)
            st.markdown('<div class="answer"><h3>Here is what the approved guidance says</h3></div>',unsafe_allow_html=True)
            st.markdown(answer)
            st.markdown('**Sources used in this answer**')
            for row in sources:
                with st.expander(f'📄 {cite_doc(row)} · {row.doc_type}'):
                    st.write(row.content)
                    st.caption('Fictional demo source; not AMN policy or verified clinical guidance.')
            with st.expander('How this would work in Snowflake'):
                st.write('Cortex Search retrieves relevant passages from authorized documents; a grounded LLM composes a concise answer with citations. This offline version uses keyword retrieval and rule-based response composition, not a live LLM or Cortex Search service.')

with t3:
    st.markdown('<div class="eyebrow">Cortex Agents experience</div>',unsafe_allow_html=True)
    st.header('From staffing problem to recommended action')
    st.write('**Executive moment:** Ask the copilot to investigate an unfilled role. It brings together demand, candidate availability, and credentialing guidance—and returns an actionable briefing.')
    a,b=st.columns(2)
    loc=a.selectbox('Market',sorted(market.market.unique()),key='agent_market')
    spec=b.selectbox('Specialty',sorted(market[market.market.eq(loc)].specialty.unique()),key='agent_spec')
    st.markdown(f'**Your request:** “Investigate our {spec} staffing situation in {loc}. What should my team do next?”')
    if st.button('Generate executive briefing',type='primary',key='agent_go'):
        st.session_state['agent_run']=(loc,spec)
    if 'agent_run' in st.session_state:
        loc,spec=st.session_state['agent_run']
        r=market[(market.market.eq(loc))&(market.specialty.eq(spec))].iloc[0]
        available=candidates[(candidates.market.eq(loc))&(candidates.specialty.eq(spec))&(candidates.available_in_days.le(14))]
        hits=search_docs(spec+' credential requirements')
        doclist=[row for _,row in hits[:2]]
        gap=int(r.gap)
        rate=float(r.fill_rate)
        n=len(available)
        urgency='High' if gap>=10 or rate<55 else ('Elevated' if gap>0 else 'Monitor')
        st.markdown('<div class="eyebrow">Illustrative agent response · synthetic scenario</div>',unsafe_allow_html=True)
        st.markdown(f'<div class="answer"><h3>{"🔴" if urgency=="High" else "🟠" if urgency=="Elevated" else "🟢"} {urgency} priority: {loc} · {spec}</h3><p>Here is the staffing picture and the next best action for your recruiting team.</p></div>',unsafe_allow_html=True)
        st.markdown(f'**What I found**  \nThere are **{int(r.open_requests)} open requests** and **{int(r.available_candidates)} candidates in the snapshot**, giving an illustrative **{gap}-position supply gap**. The historical 90-day fill rate is **{rate:.1f}%**. In the separate fictional candidate list, **{n} profiles** in this market and specialty indicate availability within 14 days. These are not verified matches.')
        st.markdown('**What I recommend**')
        if gap>0:
            st.markdown(f'**1. Prioritize this recruiting queue.** Ask the {loc} account owner to confirm which of the {int(r.open_requests)} open requests are urgent and still active.')
        else:
            st.markdown('**1. Validate demand before escalating.** The snapshot does not show a positive supply gap.')
        st.markdown(f'**2. Review {n} near-term profiles.** Have recruiters verify actual availability, shift preference, experience, licenses, and client-specific fit. Do not treat the prefilter as a hiring recommendation.')
        if doclist:
            st.markdown(f'**3. Check required documentation.** The fictional knowledge base includes **{doclist[0].title} [{doclist[0].doc_id}]**. Confirm requirements with credentialing before submission.')
        else:
            st.markdown('**3. Escalate credentialing requirements.** No suitable fictional guidance was retrieved; ask an authorized specialist.')
        st.markdown('**4. Request approval.** Prepare a recruiter review queue; do not contact candidates, change records, or make employment decisions automatically.')
        st.markdown('**Decision for leadership:** Assign an account owner to validate urgent demand and a recruiting lead to review near-term profiles. Recheck the gap after verification.')
        st.caption('Evidence: synthetic market_snapshot.csv; synthetic_candidates.csv; fictional documents cited below. Counts are illustrative, not AMN performance metrics.')
        with st.expander('Show the evidence behind this recommendation'):
            st.markdown('**Workforce data · Analyst-like step**')
            st.dataframe(pd.DataFrame([{'Market':loc,'Specialty':spec,'Open requests':int(r.open_requests),'Snapshot candidate supply':int(r.available_candidates),'Gap':gap,'90-day fill rate':f'{rate:.1f}%'}]),hide_index=True,use_container_width=True)
            st.markdown('**Candidate shortlist · approved data lookup**')
            if n:st.dataframe(available[['candidate_id','years_experience','certifications','available_in_days','preferred_shift']].head(8),hide_index=True,use_container_width=True)
            else:st.write('No profiles matched the 14-day prefilter.')
            st.markdown('**Relevant knowledge · Search-like step**')
            for row in doclist:st.markdown(f'**[{row.doc_id}] {row.title}:** {row.content}')
        with st.expander('What the AI agent would do in production'):
            st.write('A real Cortex Agent would call governed tools to query staffing data, retrieve role briefs and policies, and assemble a grounded briefing. Human reviewers would approve outreach and any consequential action. This offline demo executes local calculations and a scripted response template; it does not call Cortex Agents or autonomously reason.')
        st.info('Suggested next step: **Review priority requests with the account owner**. No messages have been sent and no records have been changed.')
with t4:
    st.header('How this becomes a real Snowflake Cortex solution')
    st.code('Approved staffing tables ──> Snowflake semantic view ──> Cortex Analyst ──┐\n                                                                    │\nApproved role briefs / policies ──> Cortex Search service ───────────┼──> Cortex Agent ──> Streamlit interface\n                                                                    │\nApproved workflow APIs (read-only first) ──> governed tools ─────────┘\n                                                    ↓\n                                    Audit logs · RBAC · evaluations · human approval',language='text')
    st.markdown('**Production requirements:** governed semantic definitions, document-level access controls, relevance and SQL accuracy evaluations, cost limits, prompt-injection defenses, least-privilege tool access, candidate privacy, fairness review, and approval gates for consequential decisions.')
    st.markdown('**Suggested pilot:** one recruiting team, 1–2 specialties, a small approved document corpus, 10–15 validated questions, and a read-only agent workflow. Measure answer correctness, citation quality, recruiter time saved, and escalation accuracy.')
    st.markdown('**Important distinction:** This app is a self-contained *experience prototype*. Cortex Analyst, Cortex Search, and Cortex Agents are architectural targets. Real Snowflake integration requires credentials, permissions, services, evaluation, and approved data.')
