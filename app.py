"""
GTF Brand Onboarding Dashboard v1
Track brand onboarding progress, checklists, files, and status
"""

import streamlit as st
import json
from datetime import datetime, date
from pathlib import Path

st.set_page_config(
    page_title="GTF Brand Onboarding",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Data ──
DATA_FILE = Path(__file__).parent / "brands.json"

def load_brands():
    if DATA_FILE.exists():
        with open(DATA_FILE) as f:
            return json.load(f)
    return {"brands": []}

def save_brands(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2, default=str)

data = load_brands()
brands = data.get("brands", [])

# ── Styles ──
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp { font-family: 'Inter', sans-serif; }
    
    .brand-card {
        background: white;
        border: 1px solid #e5e5e5;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
        transition: box-shadow 0.2s;
    }
    .brand-card:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
    
    .brand-name { font-size: 18px; font-weight: 700; color: #1a1a1a; margin-bottom: 4px; }
    
    .stage-badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .stage-onboarded { background: #ecfdf5; color: #059669; }
    .stage-negotiating { background: #fff7ed; color: #ea580c; }
    .stage-in-talks { background: #eff6ff; color: #2563eb; }
    .stage-complete { background: #f0fdf4; color: #16a34a; }
    
    .status-tag {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 8px;
        font-size: 12px;
        font-weight: 500;
        background: #fef3c7;
        color: #92400e;
        margin-top: 8px;
    }
    .status-overdue { background: #fee2e2; color: #991b1b; }
    
    .checklist-item { padding: 4px 0; font-size: 14px; }
    .check-done { color: #059669; } 
    .check-pending { color: #9ca3af; }
    
    .progress-bar {
        height: 6px;
        background: #e5e7eb;
        border-radius: 3px;
        margin-top: 12px;
        overflow: hidden;
    }
    .progress-fill {
        height: 100%;
        border-radius: 3px;
        transition: width 0.3s;
    }
    
    .metric-box {
        background: #fafafa;
        border: 1px solid #e5e5e5;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
    }
    .metric-num { font-size: 28px; font-weight: 700; color: #1a1a1a; }
    .metric-label { font-size: 11px; color: #888; text-transform: uppercase; letter-spacing: 1px; }
    
    div[data-testid="stSidebar"] { background: #fafafa; }
    
    .notes-box {
        background: #fffbeb;
        border: 1px solid #fde68a;
        border-radius: 8px;
        padding: 12px;
        font-size: 13px;
        margin-top: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──
with st.sidebar:
    st.markdown("### ✨ GTF Brand Onboarding")
    st.markdown("---")
    
    # Summary metrics
    total = len(brands)
    onboarded = sum(1 for b in brands if b["stage"] == "Onboarded")
    in_talks = sum(1 for b in brands if b["stage"] == "In Talks")
    negotiating = sum(1 for b in brands if b["stage"] == "Negotiating")
    
    # Checklist completion
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
    
    # Filter
    stage_filter = st.selectbox("Filter by Stage", ["All", "Onboarded", "In Talks", "Negotiating", "Complete"])
    
    st.markdown("---")
    
    # Add new brand
    with st.expander("➕ Add New Brand"):
        new_name = st.text_input("Brand Name")
        new_stage = st.selectbox("Stage", ["In Talks", "Negotiating", "Onboarded"])
        new_commission = st.text_input("Commission", "40%")
        new_poc = st.text_input("POC Name")
        new_email = st.text_input("POC Email")
        
        if st.button("Add Brand", type="primary"):
            if new_name:
                new_brand = {
                    "id": new_name.lower().replace(" ", "_"),
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
                save_brands(data)
                st.success(f"✅ {new_name} added!")
                st.rerun()

# ── Main Content ──
st.markdown("# ✨ Brand Onboarding Dashboard")
st.markdown(f"*{total} brands · {done_items}/{total_items} checklist items complete · Last updated: {datetime.now().strftime('%B %d, %Y')}*")

# Quick stats row
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

# ── Brand Cards ──
filtered = brands if stage_filter == "All" else [b for b in brands if b["stage"] == stage_filter]

# Sort: overdue first, then by completion
def sort_key(b):
    is_overdue = "OVERDUE" in b.get("status_tag", "")
    done = sum(1 for v in b["checklist"].values() if v)
    total = len(b["checklist"])
    return (not is_overdue, -done/total if total > 0 else 0)

filtered.sort(key=sort_key)

for idx, brand in enumerate(filtered):
    checklist = brand["checklist"]
    done = sum(1 for v in checklist.values() if v)
    total_check = len(checklist)
    pct = (done / total_check * 100) if total_check > 0 else 0
    
    # Stage badge class
    stage_class = {
        "Onboarded": "stage-onboarded",
        "In Talks": "stage-in-talks", 
        "Negotiating": "stage-negotiating",
        "Complete": "stage-complete"
    }.get(brand["stage"], "stage-in-talks")
    
    # Progress color
    if pct >= 80: prog_color = "#059669"
    elif pct >= 50: prog_color = "#eab308"
    elif pct >= 20: prog_color = "#f97316"
    else: prog_color = "#dc2626"
    
    status_class = "status-overdue" if "OVERDUE" in brand.get("status_tag", "") else ""
    
    with st.expander(f"{'🔴 ' if 'OVERDUE' in brand.get('status_tag', '') else ''}{brand['name']} — {brand['stage']} — {done}/{total_check} complete", expanded=False):
        
        col_main, col_side = st.columns([2, 1])
        
        with col_main:
            # Stage + Commission
            st.markdown(f"""
            <span class="stage-badge {stage_class}">{brand['stage']}</span>
            &nbsp;&nbsp;Commission: <strong>{brand['commission']}</strong>
            """, unsafe_allow_html=True)
            
            if brand.get("poc"):
                st.markdown(f"**POC:** {brand['poc']} {('· ' + brand['poc_email']) if brand.get('poc_email') else ''}")
            
            # Status tag
            if brand.get("status_tag"):
                st.markdown(f'<div class="status-tag {status_class}">{brand["status_tag"]}</div>', unsafe_allow_html=True)
            
            # Progress bar
            st.markdown(f"""
            <div class="progress-bar">
                <div class="progress-fill" style="width:{pct}%; background:{prog_color};"></div>
            </div>
            <div style="font-size:11px; color:#888; margin-top:4px;">{done}/{total_check} items complete ({pct:.0f}%)</div>
            """, unsafe_allow_html=True)
            
            # Notes
            if brand.get("notes"):
                st.markdown(f'<div class="notes-box">📝 {brand["notes"]}</div>', unsafe_allow_html=True)
            
            # Drive folder link
            if brand.get("drive_folder"):
                st.markdown(f"[📁 Open Google Drive Folder]({brand['drive_folder']})")
        
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
                
                # Check if all done
                if all(checklist.values()):
                    brand["stage"] = "Complete"
                    brand["status_tag"] = "✅ All Complete"
                
                data["brands"] = brands
                save_brands(data)
                st.rerun()
        
        # Edit section
        st.markdown("---")
        col_edit1, col_edit2, col_edit3 = st.columns(3)
        
        with col_edit1:
            new_stage = st.selectbox("Update Stage", ["In Talks", "Negotiating", "Onboarded", "Complete"], 
                                     index=["In Talks", "Negotiating", "Onboarded", "Complete"].index(brand["stage"]) if brand["stage"] in ["In Talks", "Negotiating", "Onboarded", "Complete"] else 0,
                                     key=f"stage_{brand['id']}_{idx}")
        
        with col_edit2:
            status_options = [
                "Waiting on CSV",
                "Waiting on UGC Videos", 
                "Waiting on Shop the Look",
                "Waiting on Commission Agreement",
                "Waiting on Commission Finalization",
                "Waiting on Import/Export License",
                "Waiting on All Templates",
                "Waiting on Final Call",
                "Needs Full Pitch",
                "Email Bounced — Need Instagram DM",
                "OVERDUE — Commercials Requested",
                "OVERDUE — Contract Pending",
                "Proposal Sent — Awaiting Response",
                "In Progress",
                "✅ All Complete",
                "Custom..."
            ]
            current_idx = 0
            for i, opt in enumerate(status_options):
                if opt == brand.get("status_tag", ""):
                    current_idx = i
                    break
            new_status = st.selectbox("Status", status_options, index=current_idx, key=f"status_{brand['id']}_{idx}")
            if new_status == "Custom...":
                new_status = st.text_input("Custom status", key=f"custom_status_{brand['id']}_{idx}")
        
        with col_edit3:
            new_notes = st.text_area("Notes", value=brand.get("notes", ""), height=80, key=f"notes_{brand['id']}_{idx}")
        
        if st.button("💾 Save Changes", key=f"save_{brand['id']}_{idx}"):
            brand["stage"] = new_stage
            brand["status_tag"] = new_status
            brand["notes"] = new_notes
            brand["last_updated"] = str(date.today())
            data["brands"] = brands
            save_brands(data)
            st.success(f"✅ {brand['name']} updated!")
            st.rerun()

# ── Footer ──
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#888; font-size:11px; padding:20px;">
    GTF Brand Onboarding Dashboard · Built by Zoya · April 2026
</div>
""", unsafe_allow_html=True)
