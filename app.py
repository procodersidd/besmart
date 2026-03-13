import streamlit as st
from intelligence_engine import run_perfected_analysis
from supabase import create_client, Client
import os

# --- PAGE SETUP ---
st.set_page_config(page_title="Geopolitical Intelligence Archive", page_icon="🏛️", layout="wide")

# --- CUSTOM CSS FOR "THINKER" VIBE ---
st.markdown("""
    <style>
    .report-text { font-family: 'serif'; font-size: 1.1rem; line-height: 1.6; }
    .sidebar-history { font-size: 0.9rem; color: #666; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE CONNECTION (Sidebar History) ---
@st.cache_resource
def get_supabase():
    # Use the same keys as your script
    url = "https://wlayjqoaofcwkzavctfh.supabase.co"
    key = "sb_publishable_lQx5zbupUfHw6zBqhFMZFQ_JzQheqTe"
    return create_client(url, key)

supabase = get_supabase()

# --- SIDEBAR: HISTORY ---
with st.sidebar:
    st.title("📜 Archive History")
    st.info("Reports saved to your Supabase Cloud")
    
    # Fetch latest 10 reports
    try:
        response = supabase.table("intelligence_reports").select("*").order("created_at", desc=True).limit(10).execute()
        for report in response.data:
            if st.button(f"📄 {report['headline']}", key=report['id']):
                st.session_state.selected_report = report['report_content']
                st.session_state.selected_headline = report['headline']
    except Exception as e:
        st.error("Could not load history.")

# --- MAIN INTERFACE ---
st.title("🏛️ Geopolitical Reasoning Engine")
st.subheader("Autonomous Multi-Agent Synthesis")

query = st.text_input("Enter a global shift or historical inquiry:", placeholder="e.g., The impact of BRICS expansion on Western maritime law")

if st.button("Commence Deep Analysis"):
    if query:
        with st.spinner("⏳ Agents are debating historical parallels and logic..."):
            try:
                # Calls your existing perfection code
                final_output = run_perfected_analysis(query)
                st.session_state.selected_report = str(final_output)
                st.session_state.selected_headline = query
                st.success("Analysis complete and archived to Supabase.")
            except Exception as e:
                st.error(f"Error during analysis: {e}")
    else:
        st.warning("Please enter an inquiry.")

st.divider()

# --- DISPLAY AREA ---
if "selected_report" in st.session_state:
    st.header(f"Report: {st.session_state.selected_headline}")
    st.markdown(f'<div class="report-text">{st.session_state.selected_report}</div>', unsafe_allow_html=True)