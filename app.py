"""
GTF Brand Onboarding Dashboard v2
GitHub-backed persistence + Google Calendar integration
"""

import streamlit as st
import json
from datetime import datetime, date, timedelta
from pathlib import Path

# Try GitHub-backed persistence first, fall back to local
from github_db import load_from_github, save_to_github

st.set_page_config(
    page_title="GTF Brand Onboarding",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Data Loading ──
DATA_FILE = Path(__file__).parent / "brands.json"

@st.cache_data(ttl=30)
def load_brands():
    """Load from GitHub first, fall back to local file"""
    gh_data, sha = load_from_github()
    if gh_data:
        return gh_data, sha
    # Fallback to local
    if DATA_FILE.exists():
        with open(DATA_FILE) as f:
            return json.load(f), None
    return {"brands": []}, None

def save_brands(data, sha=None, message="Update brands"):
    """Save to GitHub first, fall back to local"""
    if sha:
        success = save_to_github(data, sha, message)
        if success:
            load_brands.clear()
            return True
    # Fallback: save locally
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2, default=str)
    load_brands.clear()
    return True

data, sha = load_brands()
brands = data.get("brands", [])

# ── Calendar Functions ──
def get_brand_meetings():
    """Load meetings from GitHub-synced meetings.json (updated by Zoya every 30 mins)"""
    from github_db import get_headers, REPO, BRANCH
    import requests, base64
    try:
        headers = get_headers()
        if headers:
            url = f"https://api.github.com/repos/{REPO}/contents/meetings.json?ref={BRANCH}"
            resp = requests.get(url, headers=headers, timeout=10)
            if resp.status_code == 200:
                content = base64.b64decode(resp.json()["content"]).decode("utf-8")
                data = json.loads(content)
                return data.get("meetings", [])
    except Exception:
        pass
    # Fallback to local file
    meetings_file = Path(__file__).parent / "meetings.json"
    if meetings_file.exists():
        with open(meetings_file) as f:
            return json.load(f).get("meetings", [])
    return []

# ── Styles ──
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    .stApp { font-family: 'Inter', sans-serif; }
    .brand-name { font-size: 18px; font-weight: 700; color: #1a1a1a; }
    .stage-badge { display: inline-block; padding: 3px 10px; border-radius: 12px; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
    .stage-onboarded { background: #ecfdf5; color: #059669; }
    .stage-negotiating { background: #fff7ed; color: #ea580c; }
    .stage-in-talks { background: #eff6ff; color: #2563eb; }
    .stage-complete { background: #f0fdf4; color: #16a34a; }
    .status-tag { display: inline-block; padding: 4px 12px; border-radius: 8px; font-size: 12px; font-weight: 500; background: #fef3c7; color: #92400e; margin-top: 8px; }
    .status-overdue { background: #fee2e2; color: #991b1b; }
    .progress-bar { height: 6px; background: #e5e7eb; border-radius: 3px; margin-top: 12px; overflow: hidden; }
    .progress-fill { height: 100%; border-radius: 3px; }
    .metric-box { background: #fafafa; border: 1px solid #e5e5e5; border-radius: 10px; padding: 16px; text-align: center; }
    .metric-num { font-size: 28px; font-weight: 700; color: #1a1a1a; }
    .metric-label { font-size: 11px; color: #888; text-transform: uppercase; letter-spacing: 1px; }
    .notes-box { background: #fffbeb; border: 1px solid #fde68a; border-radius: 8px; padding: 12px; font-size: 13px; margin-top: 8px; }
    .meeting-card { background: #f0f7ff; border: 1px solid #c2deff; border-radius: 8px; padding: 12px; margin-bottom: 8px; }
    .meeting-date { font-weight: 600; color: #1565c0; }
    .meeting-title { font-weight: 600; color: #1a1a1a; }
    div[data-testid="stSidebar"] { background: #fafafa; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──
with st.sidebar:
    st.markdown("### ✨ GTF Brand Onboarding")
    st.markdown("---")
    
    total = len(brands)
    onboarded = sum(1 for b in brands if b["stage"] == "Onboarded")
    in_talks = sum(1 for b in brands if b["stage"] == "In Talks")
    negotiating = sum(1 for b in brands if b["stage"] == "Negotiating")
    
    total_items = sum(sum(1 for v in b["checklist"].values()) for b in brands)
    done_items = sum(sum(1 for v in b["checklist"].values() if v) for b in brands)
    completion = (done_items / total_items * 100) if total_items > 0 else 0
    
    col1, col2 = st.columns(2)
    col1.metric("Total Brands", total)
    col2.metric("Completion", f"{completion:.0f}%")
    
    col3, col4 = st.columns(2)
    col3.metric("Onboarded", onboarded)
    col4.metric("In Talks", in_talks + negotiating)
    
    st.markdown("---")
    
    stage_filter = st.selectbox("Filter by Stage", ["All", "Onboarded", "In Talks", "Negotiating", "Complete"])
    
    st.markdown("---")
    
    # Add new brand
    with st.expander("➕ Add New Brand"):
        new_name = st.text_input("Brand Name")
        new_stage = st.selectbox("Stage", ["In Talks", "Negotiating", "Onboarded"])
        new_commission = st.text_input("Commission", "40%")
        new_poc = st.text_input("POC Name")
        new_email = st.text_input("POC Email/Phone")
        
        if st.button("Add Brand", type="primary"):
            if new_name:
                new_brand = {
                    "id": new_name.lower().replace(" ", "_").replace("'", ""),
                    "name": new_name,
                    "stage": new_stage,
                    "commission": new_commission,
                    "poc": new_poc,
                    "poc_email": new_email,
                    "drive_folder": "",
                    "notes": "",
                    "status_tag": "New — Setup Needed",
                    "checklist": {
                        "csv_received": False,
                        "ugc_videos": False,
                        "shop_the_look": False,
                        "import_export_license": False,
                        "commission_agreed": False,
                        "brand_assets": False,
                        "proposal_sent": False
                    },
                    "last_updated": str(date.today())
                }
                brands.append(new_brand)
                data["brands"] = brands
                save_brands(data, sha, f"Add brand: {new_name}")
                st.success(f"✅ {new_name} added!")
                st.rerun()

# ── Main Content ──

# Tab navigation
tab_brands, tab_calendar, tab_scout = st.tabs(["📋 Brands", "📅 Meetings", "🔍 Brand Scout"])

# ═══════ BRANDS TAB ═══════
with tab_brands:
    st.markdown("# ✨ Brand Onboarding")
    st.markdown(f"*{total} brands · {done_items}/{total_items} checklist items complete*")
    
    # Quick stats
    col1, col2, col3, col4, col5 = st.columns(5)
    overdue_count = sum(1 for b in brands if "OVERDUE" in b.get("status_tag", ""))
    waiting_csv = sum(1 for b in brands if not b["checklist"]["csv_received"])
    waiting_ugc = sum(1 for b in brands if not b["checklist"]["ugc_videos"] and b["checklist"]["csv_received"])
    waiting_commission = sum(1 for b in brands if not b["checklist"]["commission_agreed"])
    
    col1.markdown(f'<div class="metric-box"><div class="metric-num" style="color:#dc2626;">{overdue_count}</div><div class="metric-label">Overdue</div></div>', unsafe_allow_html=True)
    col2.markdown(f'<div class="metric-box"><div class="metric-num">{waiting_csv}</div><div class="metric-label">Need CSV</div></div>', unsafe_allow_html=True)
    col3.markdown(f'<div class="metric-box"><div class="metric-num">{waiting_ugc}</div><div class="metric-label">Need UGC</div></div>', unsafe_allow_html=True)
    col4.markdown(f'<div class="metric-box"><div class="metric-num">{waiting_commission}</div><div class="metric-label">Need Commission</div></div>', unsafe_allow_html=True)
    col5.markdown(f'<div class="metric-box"><div class="metric-num" style="color:#059669;">{onboarded}</div><div class="metric-label">Onboarded</div></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Brand cards
    filtered = brands if stage_filter == "All" else [b for b in brands if b["stage"] == stage_filter]
    
    def sort_key(b):
        is_overdue = "OVERDUE" in b.get("status_tag", "")
        done = sum(1 for v in b["checklist"].values() if v)
        total_c = len(b["checklist"])
        return (not is_overdue, -done/total_c if total_c > 0 else 0)
    
    filtered.sort(key=sort_key)
    
    for idx, brand in enumerate(filtered):
        checklist = brand["checklist"]
        done = sum(1 for v in checklist.values() if v)
        total_check = len(checklist)
        pct = (done / total_check * 100) if total_check > 0 else 0
        
        stage_class = {"Onboarded": "stage-onboarded", "In Talks": "stage-in-talks", "Negotiating": "stage-negotiating", "Complete": "stage-complete"}.get(brand["stage"], "stage-in-talks")
        
        if pct >= 80: prog_color = "#059669"
        elif pct >= 50: prog_color = "#eab308"
        elif pct >= 20: prog_color = "#f97316"
        else: prog_color = "#dc2626"
        
        status_class = "status-overdue" if "OVERDUE" in brand.get("status_tag", "") else ""
        overdue_icon = "🔴 " if "OVERDUE" in brand.get("status_tag", "") else ""
        
        with st.expander(f"{overdue_icon}{brand['name']} — {brand['stage']} — {done}/{total_check} complete", expanded=False):
            col_main, col_side = st.columns([2, 1])
            
            with col_main:
                st.markdown(f'<span class="stage-badge {stage_class}">{brand["stage"]}</span> &nbsp;&nbsp;Commission: <strong>{brand["commission"]}</strong>', unsafe_allow_html=True)
                
                if brand.get("poc"):
                    st.markdown(f"**POC:** {brand['poc']} {('· ' + brand['poc_email']) if brand.get('poc_email') else ''}")
                
                if brand.get("status_tag"):
                    st.markdown(f'<div class="status-tag {status_class}">{brand["status_tag"]}</div>', unsafe_allow_html=True)
                
                st.markdown(f'<div class="progress-bar"><div class="progress-fill" style="width:{pct}%; background:{prog_color};"></div></div><div style="font-size:11px; color:#888; margin-top:4px;">{done}/{total_check} items ({pct:.0f}%)</div>', unsafe_allow_html=True)
                
                if brand.get("notes"):
                    st.markdown(f'<div class="notes-box">📝 {brand["notes"]}</div>', unsafe_allow_html=True)
                
                if brand.get("drive_folder"):
                    st.markdown(f"[📁 Google Drive Folder]({brand['drive_folder']})")
            
            with col_side:
                st.markdown("**Checklist:**")
                checklist_labels = {
                    "proposal_sent": "📋 Proposal Sent",
                    "commission_agreed": "💰 Commission Agreed",
                    "csv_received": "📊 CSV Received",
                    "ugc_videos": "🎬 UGC Videos",
                    "shop_the_look": "👗 Shop the Look",
                    "import_export_license": "📜 Import/Export License",
                    "brand_assets": "🎨 Brand Assets"
                }
                
                changed = False
                for key, label in checklist_labels.items():
                    unique_key = f"{brand['id']}_{key}_{idx}"
                    new_val = st.checkbox(label, value=checklist.get(key, False), key=unique_key)
                    if new_val != checklist.get(key, False):
                        checklist[key] = new_val
                        changed = True
                
                if changed:
                    brand["checklist"] = checklist
                    brand["last_updated"] = str(date.today())
                    if all(checklist.values()):
                        brand["stage"] = "Complete"
                        brand["status_tag"] = "✅ All Complete"
                    data["brands"] = brands
                    save_brands(data, sha, f"Update checklist: {brand['name']}")
                    st.rerun()
            
            # Edit section
            st.markdown("---")
            col_e1, col_e2, col_e3 = st.columns(3)
            
            with col_e1:
                stages = ["In Talks", "Negotiating", "Onboarded", "Complete"]
                cur_idx = stages.index(brand["stage"]) if brand["stage"] in stages else 0
                new_stage = st.selectbox("Stage", stages, index=cur_idx, key=f"stage_{brand['id']}_{idx}")
            
            with col_e2:
                status_options = ["Waiting on CSV", "Waiting on UGC Videos", "Waiting on Shop the Look", "Waiting on Commission Agreement", "Waiting on Commission Finalization", "Waiting on Import/Export License", "Waiting on All Templates", "Waiting on Final Call", "Needs Full Pitch", "Email Bounced — Need Instagram DM", "OVERDUE — Commercials Requested", "OVERDUE — Contract Pending", "Proposal Sent — Awaiting Response", "New — Setup Needed", "In Progress", "✅ All Complete", "Custom..."]
                cur_status = 0
                for i, opt in enumerate(status_options):
                    if opt == brand.get("status_tag", ""):
                        cur_status = i
                        break
                new_status = st.selectbox("Status", status_options, index=cur_status, key=f"status_{brand['id']}_{idx}")
                if new_status == "Custom...":
                    new_status = st.text_input("Custom status", key=f"cs_{brand['id']}_{idx}")
            
            with col_e3:
                new_notes = st.text_area("Notes", value=brand.get("notes", ""), height=80, key=f"notes_{brand['id']}_{idx}")
            
            if st.button("💾 Save Changes", key=f"save_{brand['id']}_{idx}"):
                brand["stage"] = new_stage
                brand["status_tag"] = new_status
                brand["notes"] = new_notes
                brand["last_updated"] = str(date.today())
                data["brands"] = brands
                save_brands(data, sha, f"Update: {brand['name']} → {new_stage}")
                st.success(f"✅ {brand['name']} updated!")
                st.rerun()

# ═══════ CALENDAR TAB ═══════
with tab_calendar:
    st.markdown("# 📅 Brand Meetings")
    st.markdown("*Upcoming meetings from Google Calendar (next 14 days)*")
    st.markdown("---")
    
    meetings = get_brand_meetings()
    
    if meetings:
        for m in meetings:
            start_time = m.get("start", "")
            # start_time already set above
            summary = m.get("summary", "Untitled")
            description = m.get("description", "")
            location = m.get("location", "")
            
            # Parse date for display
            try:
                if "T" in start_time:
                    dt = datetime.fromisoformat(start_time)
                    display_date = dt.strftime("%A, %B %d")
                    display_time = dt.strftime("%I:%M %p")
                else:
                    display_date = start_time
                    display_time = "All day"
            except Exception:
                display_date = start_time
                display_time = ""
            
            # Extract meet link from description
            meet_link = ""
            if description and "meet.google.com" in description:
                for word in description.split():
                    if "meet.google.com" in word:
                        meet_link = word if word.startswith("http") else f"https://{word}"
                        break
            
            st.markdown(f"""
            <div class="meeting-card">
                <div class="meeting-date">{display_date} · {display_time}</div>
                <div class="meeting-title">{summary}</div>
                {f'<div style="font-size:12px; color:#666; margin-top:4px;">📍 {location}</div>' if location else ''}
                {f'<div style="font-size:12px; margin-top:4px;"><a href="{meet_link}">🔗 Join Google Meet</a></div>' if meet_link else ''}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No brand meetings found in the next 14 days. Meetings with brand-related keywords in the calendar will appear here automatically.")
    
    st.markdown("---")
    st.markdown("*Meetings are pulled from atiqa@getthefit.ai calendar. Any event with brand names or keywords like 'partnership', 'onboard', 'x Get the Fit' will show here.*")

# ═══════ BRAND SCOUT TAB ═══════
with tab_scout:
    st.markdown("# 🔍 Brand Scout")
    st.markdown("*Upload Instagram screenshots of brands. Zoya will identify them and add to the tracker.*")
    st.markdown("---")
    
    # Tracker selection
    tracker_choice = st.radio("Which tracker?", ["Indian Brands", "International Brands"], horizontal=True, key="tracker_radio")
    
    # File uploader
    uploaded_files = st.file_uploader(
        "Upload Instagram screenshots (up to 10)", 
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
        key="scout_uploader"
    )
    
    if uploaded_files:
        st.markdown(f"**{len(uploaded_files)} screenshot(s) uploaded**")
        
        # Show thumbnails
        cols = st.columns(min(len(uploaded_files), 5))
        for i, f in enumerate(uploaded_files):
            with cols[i % 5]:
                st.image(f, caption=f.name, width=150)
        
        st.markdown("---")
        
        # Save screenshots to a pending folder in the data
        if st.button("🚀 Send to Zoya for identification", type="primary", key="scout_send"):
            # Save file info to a scout_queue in brands.json
            scout_queue = data.get("scout_queue", [])
            for f in uploaded_files:
                import base64
                from io import BytesIO
                try:
                    from PIL import Image
                    # Compress image to ~100KB JPEG for brand identification
                    img = Image.open(f)
                    img.thumbnail((800, 800))  # Resize to max 800px
                    buffer = BytesIO()
                    img.save(buffer, format="JPEG", quality=60)
                    compressed = buffer.getvalue()
                    thumbnail_b64 = base64.b64encode(compressed).decode()
                except Exception:
                    # Fallback: just take first 200KB raw
                    f.seek(0)
                    file_bytes = f.read()
                    thumbnail_b64 = base64.b64encode(file_bytes[:200000]).decode() if len(file_bytes) > 0 else None
                
                scout_queue.append({
                    "filename": f.name,
                    "tracker": tracker_choice,
                    "uploaded_at": str(datetime.now()),
                    "uploaded_by": "Muskaan",
                    "status": "pending",
                    "identified_brand": None,
                    "website": None,
                    "instagram": None,
                    "poc_email": None,
                    "thumbnail": thumbnail_b64
                })
                f.seek(0)  # Reset file pointer
            
            data["scout_queue"] = scout_queue
            save_brands(data, sha, f"Scout: {len(uploaded_files)} screenshots uploaded")
            st.success(f"✅ {len(uploaded_files)} screenshots sent to Zoya! She'll identify the brands and update the tracker. You'll see them appear in the Brands tab.")
            st.balloons()
    
    # Show pending identifications
    scout_queue = data.get("scout_queue", [])
    pending = [s for s in scout_queue if s["status"] == "pending"]
    identified = [s for s in scout_queue if s["status"] == "identified"]
    
    if pending:
        st.markdown("---")
        st.markdown(f"### ⏳ Pending Identification ({len(pending)})")
        for s in pending:
            st.markdown(f"- **{s['filename']}** — {s['tracker']} — uploaded {s['uploaded_at'][:16]}")
    
    if identified:
        st.markdown("---")
        st.markdown(f"### ✅ Recently Identified ({len(identified)})")
        for s in identified:
            st.markdown(f"- **{s.get('identified_brand', '?')}** — {s.get('website', '')} — [{s.get('instagram', '')}]")
    
    st.markdown("---")
    st.markdown("""
    **How it works:**
    1. Upload Instagram screenshots of brands you've found
    2. Select which tracker (Indian or International)
    3. Click 'Send to Zoya'
    4. Zoya identifies the brand name, website, and contact info
    5. Brand gets added to the correct tracker sheet automatically
    6. You then fill in POC details from your DMs
    """)

# ── Footer ──
st.markdown("---")
st.markdown('<div style="text-align:center; color:#888; font-size:11px; padding:20px;">GTF Brand Onboarding Dashboard v3 · Built by Zoya · April 2026</div>', unsafe_allow_html=True)
