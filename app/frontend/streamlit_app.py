import streamlit as st
import requests
import pandas as pd
import os
import sys

# Add project root to sys.path to support fallback in-process inference
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

# Configure page to use the full horizontal screen width
st.set_page_config(
    page_title="Support Ticket Intelligence Hub",
    page_icon="🎫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom layout styles for high-end aesthetics
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Background override for full-width app layout */
    .main .block-container {
        max-width: 96% !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #090d16 !important;
        border-right: 1px solid #1e293b !important;
    }
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1 {
        font-family: 'Outfit', sans-serif !important;
        font-size: 1.8rem !important;
        color: #f8fafc !important;
    }

    /* Container Cards (st.container(border=True)) */
    div[data-testid="stVerticalBlock"] > div[style*="border-style: solid"] {
        background-color: #0f172a !important;
        border: 1.5px solid #1e293b !important;
        border-radius: 16px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3) !important;
        padding: 28px !important;
        margin-bottom: 15px !important;
    }
    
    /* Form Cards */
    div[data-testid="stForm"] {
        background-color: #0f172a !important;
        border: 1.5px solid #1e293b !important;
        border-radius: 16px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3) !important;
        padding: 28px !important;
    }

    /* Metrics Styling */
    div[data-testid="stMetric"] {
        background-color: #1e293b !important;
        border: 1.5px solid #334155 !important;
        border-radius: 12px !important;
        padding: 16px 24px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15) !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25) !important;
    }
    div[data-testid="stMetricValue"] {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 800 !important;
        font-size: 2.2rem !important;
        color: #f8fafc !important;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 0.85rem !important;
        color: #94a3b8 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.8px !important;
        font-weight: 700 !important;
    }

    /* Buttons Styling */
    div[data-testid="stFormSubmitButton"] button, button[kind="primary"] {
        background: linear-gradient(135deg, #f97316 0%, #ea580c 100%) !important;
        color: white !important;
        border: none !important;
        padding: 12px 28px !important;
        border-radius: 10px !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 15px rgba(249, 115, 22, 0.35) !important;
        width: 100% !important;
    }
    div[data-testid="stFormSubmitButton"] button:hover, button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(249, 115, 22, 0.5) !important;
        background: linear-gradient(135deg, #fb923c 0%, #f97316 100%) !important;
    }

    /* Tabs Styling */
    button[data-baseweb="tab"] {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        color: #94a3b8 !important;
        padding: 12px 24px !important;
        border-bottom-width: 3px !important;
        transition: all 0.2s ease !important;
    }
    button[data-baseweb="tab"]:hover {
        color: #f97316 !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #f97316 !important;
        border-bottom-color: #f97316 !important;
    }
    
    /* Input Fields (TextInput, TextArea) */
    div[data-testid="stTextInput"] input, div[data-testid="stTextArea"] textarea {
        background-color: #1e293b !important;
        border: 1.5px solid #334155 !important;
        border-radius: 10px !important;
        color: #f8fafc !important;
        font-size: 1rem !important;
    }
    div[data-testid="stTextInput"] input:focus, div[data-testid="stTextArea"] textarea:focus {
        border-color: #f97316 !important;
        box-shadow: 0 0 0 2px rgba(249, 115, 22, 0.2) !important;
    }
    
    /* Expander Panel */
    div[data-testid="stExpander"] {
        border: 1px solid #1e293b !important;
        border-radius: 12px !important;
        background-color: #0f172a !important;
    }
    
    /* Success, Warning, Error & Info Alerts */
    .stAlert {
        border-radius: 12px !important;
        border: 1.5px solid rgba(255, 255, 255, 0.05) !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15) !important;
        padding: 16px 20px !important;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

@st.cache_resource
def load_model_assets():
    import joblib
    MODELS_DIR = os.path.join(PROJECT_ROOT, "models")
    assets = {
        "tt_clf": joblib.load(os.path.join(MODELS_DIR, "ticket_type_model.pkl")),
        "tt_vec": joblib.load(os.path.join(MODELS_DIR, "ticket_type_tfidf.pkl")),
        "tt_le": joblib.load(os.path.join(MODELS_DIR, "ticket_type_encoder.pkl")),
        "tp_clf": joblib.load(os.path.join(MODELS_DIR, "ticket_priority_model.pkl")),
        "tp_vec": joblib.load(os.path.join(MODELS_DIR, "ticket_priority_tfidf.pkl")),
        "tp_le": joblib.load(os.path.join(MODELS_DIR, "ticket_priority_encoder.pkl")),
        "ret_vec": joblib.load(os.path.join(MODELS_DIR, "retrieval_tfidf.pkl")),
        "ret_mat": joblib.load(os.path.join(MODELS_DIR, "retrieval_matrix.pkl")),
        "ret_df": joblib.load(os.path.join(MODELS_DIR, "retrieval_tickets.pkl")),
    }
    return assets

def get_local_pipeline():
    try:
        import importlib
        import app.api.inference as inference
        # Reload the inference module to pick up code changes
        importlib.reload(inference)
        
        # Inject cached model assets into reloaded module's global variables
        assets = load_model_assets()
        inference.tt_clf = assets["tt_clf"]
        inference.tt_vec = assets["tt_vec"]
        inference.tt_le = assets["tt_le"]
        inference.tp_clf = assets["tp_clf"]
        inference.tp_vec = assets["tp_vec"]
        inference.tp_le = assets["tp_le"]
        inference.ret_vec = assets["ret_vec"]
        inference.ret_mat = assets["ret_mat"]
        inference.ret_df = assets["ret_df"]
        
        return inference.predict_ticket
    except Exception as e:
        st.error(f"Failed to load local pipeline fallback: {e}")
        return None

# Initialize persistent session states
if "subject" not in st.session_state:
    st.session_state.subject = ""
if "description" not in st.session_state:
    st.session_state.description = ""
if "results" not in st.session_state:
    st.session_state.results = None

# Sidebar Controls & API Status
with st.sidebar:
    st.title("⚙️ Control Panel")
    
    # Check Backend Health Status
    try:
        response = requests.get(f"{API_URL}/health", timeout=2)
        if response.status_code == 200:
            st.success("🟢 API Service Connected")
            use_api = True
        else:
            st.warning("🟡 Service Offline, local execution")
            use_api = False
    except Exception:
        st.info("ℹ️ Running in Sandbox (Offline-First)")
        use_api = False
        
    st.markdown("---")
    st.markdown("### 📸 LinkedIn Post Capture Mode")
    st.write("Toggle specific views below to isolate panels for clean screenshots:")
    screenshot_mode = st.radio(
        "Select Visible Section:",
        ["Show All Sections", "Part 1: Ticket Classification", "Part 2: Explainability Factors", "Part 3: Historical Resolutions"]
    )
    
    # If in screenshot mode, render input forms in sidebar for edits
    submitted_sidebar = False
    if screenshot_mode != "Show All Sections":
        st.markdown("---")
        st.markdown("### 📝 Modify Inputs")
        sb_subject = st.text_input("Ticket Subject", value=st.session_state.subject, key="sb_subj")
        sb_description = st.text_area("Ticket Description", value=st.session_state.description, height=150, key="sb_desc")
        
        st.session_state.subject = sb_subject
        st.session_state.description = sb_description
        submitted_sidebar = st.button("Run Intelligence Engine", type="primary", key="sb_submit")

# Header Banner (only displayed if not isolating a part for clean screenshotting)
if screenshot_mode == "Show All Sections":
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #f97316 0%, #d97706 100%);
        padding: 30px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 6px 20px rgba(249, 115, 22, 0.25);
        border: 1px solid #ea580c;
    ">
        <h1 style="color: white; margin: 0; font-size: 2.6rem; font-weight: 800; font-family: 'Outfit', 'Plus Jakarta Sans', sans-serif; letter-spacing: -0.5px;">🎫 Support Ticket Intelligence System</h1>
        <p style="color: #ffedd5; margin: 10px 0 0 0; font-size: 1.15rem; font-weight: 400; font-family: 'Plus Jakarta Sans', sans-serif;">Real-time Natural Language Processing for Automated Classification, Explanations, and Similarity Matching</p>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

# Main Page Inputs (only if "Show All Sections" is active)
submitted_main = False
if screenshot_mode == "Show All Sections":
    st.subheader("📥 Input Support Request Details")
    with st.form("ticket_input_form"):
        main_subject = st.text_input("Ticket Subject", value=st.session_state.subject, key="main_subj", placeholder="e.g., Cannot login to my account")
        main_description = st.text_area("Ticket Description", value=st.session_state.description, key="main_desc", placeholder="e.g., I've tried resetting but no email is arriving.", height=120)
        submitted_main = st.form_submit_button("Run Intelligence Engine")
        
    if submitted_main:
        st.session_state.subject = main_subject
        st.session_state.description = main_description

# Run Inference Pipeline
should_run = submitted_main or submitted_sidebar or (st.session_state.results is None and st.session_state.subject and st.session_state.description)

if should_run:
    sub = st.session_state.subject
    desc = st.session_state.description
    
    if not sub.strip() or not desc.strip():
        st.warning("Please enter a ticket subject and description.")
    else:
        results = None
        if use_api:
            try:
                payload = {"subject": sub, "description": desc}
                response = requests.post(f"{API_URL}/predict", json=payload, timeout=5)
                if response.status_code == 200:
                    results = response.json()
            except Exception:
                pass
                
        if results is None:
            local_pipeline = get_local_pipeline()
            if local_pipeline:
                results = local_pipeline(sub, desc)
                
        if results:
            st.session_state.results = results

# Render Results
if st.session_state.results:
    res_data = st.session_state.results
    
    # Render Collapsible Ticket Context
    if screenshot_mode != "Show All Sections" and st.session_state.subject:
        with st.expander("📝 View Input Ticket Context", expanded=False):
            st.info(f"**Subject:** {st.session_state.subject}\n\n**Description:** {st.session_state.description}")
    
    # PART 1: CLASSIFICATION (Show if "Show All" or "Part 1" selected)
    if screenshot_mode in ["Show All Sections", "Part 1: Ticket Classification"]:
        with st.container(border=True):
            st.markdown("### 🎯 Part 1: Automated Ticket Categorization & Urgency")
            
            # Compute Sentiment and SLA Response Target dynamically
            prio = res_data["priority"]
            clean_lower = (st.session_state.subject + " " + st.session_state.description).lower()
            
            if prio.lower() == "critical" or any(w in clean_lower for w in ["angry", "frustrated", "terrible", "worst", "unacceptable"]):
                sentiment = "🔴 Extremely Frustrated"
                sla = "15 Mins"
            elif prio.lower() == "high" or "cancel" in clean_lower:
                sentiment = "🟡 Frustrated / Churn Risk"
                sla = "1 Hour"
            elif prio.lower() == "medium":
                sentiment = "🟡 Neutral / Calm"
                sla = "4 Hours"
            else:
                sentiment = "🟢 Satisfied / Calm"
                sla = "12 Hours"
                
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown("**Predicted Category:**")
                st.info(f"📁 **{res_data['type']}**")
                
            with col2:
                st.markdown("**Assessed Urgency:**")
                if prio.lower() == "critical":
                    st.error(f"🚨 **{prio}**")
                elif prio.lower() == "high":
                    st.warning(f"⚠️ **{prio}**")
                elif prio.lower() == "medium":
                    st.info(f"⚡ **{prio}**")
                else:
                    st.success(f"🟢 **{prio}**")
                    
            with col3:
                st.markdown("**Customer Sentiment:**")
                if "🔴" in sentiment:
                    st.error(f"**{sentiment}**")
                elif "🟡" in sentiment:
                    st.warning(f"**{sentiment}**")
                else:
                    st.success(f"**{sentiment}**")
                    
            with col4:
                st.metric(label="SLA Response Target", value=sla)
                
        # Recommended Support Playbook Card
        with st.container(border=True):
            st.markdown("### 📋 Support Playbook & Recommended Next Steps")
            category = res_data["type"]
            if category == "Cancellation request":
                steps = [
                    "1. **Flag CRM Account**: Mark user profile as high churn risk in the account system.",
                    "2. **Identify Pain Points**: Check conversation tags to note key reasons for leaving.",
                    "3. **Offer Incentive**: Suggest a discounted tier or credit to save the account.",
                    "4. **Graceful Offboarding**: Send a checklist if they decide to proceed."
                ]
            elif category == "Refund request":
                steps = [
                    "1. **Audit Stripe Transaction**: Locate the duplicate charge in payment history.",
                    "2. **Verify Refund Eligibility**: Confirm payment date falls within refund terms.",
                    "3. **Issue Credit/Refund**: Initiate standard credit card return via dashboard.",
                    "4. **Confirmation**: Email automated refund confirmation code to user."
                ]
            elif category == "Billing inquiry":
                steps = [
                    "1. **Ledger Review**: Pull user's active billing invoices and billing cycles.",
                    "2. **Payment Card Status**: Verify expiration dates or authorization issues.",
                    "3. **Customer Portal**: Share self-service billing links for safe updates."
                ]
            elif category == "Technical issue":
                steps = [
                    "1. **Server Logs**: Query ELK dashboard for error stacktraces matching the user's ID.",
                    "2. **Environment Diagnostics**: Check device details or local system specifications.",
                    "3. **Tier-2 Escalation**: Transfer thread if database/installer crash persists."
                ]
            else: # Product inquiry
                steps = [
                    "1. **Docs Search**: Retrieve help documentation links matching query topics.",
                    "2. **Response Draft**: Populate pre-composed walkthrough email template.",
                    "3. **Close Loop**: Archive ticket upon user confirmation of resolution."
                ]
            for step in steps:
                st.markdown(step)
        st.write("") # Spacer

    # PART 2: EXPLAINABILITY (Show if "Show All" or "Part 2" selected)
    if screenshot_mode in ["Show All Sections", "Part 2: Explainability Factors"]:
        with st.container(border=True):
            st.markdown("### 💡 Part 2: Local Feature Contributions (Explainable AI)")
            
            col_type, col_prio = st.columns(2)
            
            with col_type:
                st.markdown("#### Category Selection Drivers")
                exp_type = res_data["type_exp"]
                if exp_type:
                    df_type = pd.DataFrame({
                        "Token": list(exp_type.keys()),
                        "Weight": list(exp_type.values())
                    }).sort_values(by="Weight", ascending=True)
                    st.bar_chart(df_type, x="Token", y="Weight", horizontal=True, use_container_width=True, height=200)
                else:
                    st.info("No explainability features identified.")
                    
            with col_prio:
                st.markdown("#### Priority Selection Drivers")
                exp_prio = res_data["prio_exp"]
                if exp_prio:
                    df_prio = pd.DataFrame({
                        "Token": list(exp_prio.keys()),
                        "Weight": list(exp_prio.values())
                    }).sort_values(by="Weight", ascending=True)
                    st.bar_chart(df_prio, x="Token", y="Weight", horizontal=True, use_container_width=True, height=200)
                else:
                    st.info("No explainability features identified.")
        st.write("") # Spacer
        
    # PART 3: RESOLUTIONS (Show if "Show All" or "Part 3" selected)
    if screenshot_mode in ["Show All Sections", "Part 3: Historical Resolutions"]:
        with st.container(border=True):
            st.markdown("### 🔍 Part 3: Recommended Resolutions from Ticket Archives")
            
            col_rec1, col_rec2, col_rec3 = st.columns(3)
            cols = [col_rec1, col_rec2, col_rec3]
            badges = ["🥇 Best Match", "🥈 Second Match", "🥉 Third Match"]
            
            for idx, res in enumerate(res_data["resolutions"]):
                with cols[idx]:
                    st.markdown(f"#### {badges[idx]}")
                    with st.container(border=True):
                        st.success(f"Similarity Score: {res['similarity']*100:.1f}%")
                        st.markdown(f"**Archive Subject:** {res['subject']}")
                        # Truncate description slightly for elegant fit in columns
                        desc_text = res['description']
                        if len(desc_text) > 130:
                            desc_text = desc_text[:130] + "..."
                        st.markdown(f"**Description:** {desc_text}")
                        st.info(f"💡 **Suggested Resolution:**\n{res['resolution']}")
