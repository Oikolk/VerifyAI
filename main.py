import streamlit as st
from agents import researcher_agent, analyst_agent, judge_agent
from utils import init_session_state, check_cache, update_cache, add_to_history
import time

# Page Configuration
st.set_page_config(
    page_title="VerifyAI - The Agentic Truth Shield",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    .verdict-card {
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        border: 1px solid #333;
    }
    .verdict-true {
        background-color: rgba(0, 255, 0, 0.1);
        border-color: #00ff00;
    }
    .verdict-false {
        background-color: rgba(255, 0, 0, 0.1);
        border-color: #ff0000;
    }
    .verdict-unverified {
        background-color: rgba(255, 255, 0, 0.1);
        border-color: #ffff00;
    }
    .confidence-score {
        font-size: 24px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
init_session_state()

# Sidebar
with st.sidebar:
    st.title("🛡️ VerifyAI")
    st.markdown("### History")
    for item in st.session_state.history[:5]:
        with st.expander(f"{item['claim'][:30]}..."):
            st.write(f"**Verdict:** {item['result']['verdict']}")
            st.write(f"**Confidence:** {item['result']['confidence']}%")

# Main Content
st.title("VerifyAI: The Agentic Truth Shield")
st.markdown("""
**Instantly validate claims with the rigor of a research team but the speed of AI.**
Powered by **Gemini 2.5 Flash** and **Google Search Grounding**.
""")

# Example Claims
example_claims = [
    "The Eiffel Tower is in London.",
    "The Great Wall of China is visible from space.",
    "Honey never spoils.",
    "Humans use only 10% of their brains."
]

st.markdown("### Try an example:")
cols = st.columns(2)
for i, ex in enumerate(example_claims):
    if cols[i % 2].button(ex, use_container_width=True):
        st.session_state.claim_input = ex

# Input Area
claim = st.text_input("Enter a claim to verify:", key="claim_input", placeholder="e.g., The Eiffel Tower is in London.")

if st.button("Verify Claim", type="primary"):
    if not claim:
        st.warning("Please enter a claim.")
    else:
        # Check Cache
        cached_result = check_cache(claim)
        
        if cached_result:
            st.success("Found in cache!")
            result = cached_result
            # Simulate a slight delay for effect or just show immediately
        else:
            with st.status("Investigating...", expanded=True) as status:
                # Step 1: Researcher
                st.write("🔍 **Researcher Agent**: Scouring the web for evidence...")
                research_data = researcher_agent(claim)
                if "error" in research_data:
                    st.error(f"Error during research: {research_data['error']}")
                    st.stop()
                
                # Step 2: Analyst
                st.write("📊 **Analyst Agent**: Analyzing facts and credibility...")
                analysis = analyst_agent(claim, research_data)
                
                # Step 3: Judge
                st.write("⚖️ **Judge Agent**: Deliberating final verdict...")
                result = judge_agent(claim, analysis)
                
                # Add sources to result for display
                result["sources"] = research_data.get("grounding_metadata", {})
                
                # Update Cache and History
                update_cache(claim, result)
                add_to_history(claim, result)
                
                status.update(label="Verification Complete!", state="complete", expanded=False)

        # Display Results
        verdict_color = "verdict-unverified"
        if result['verdict'] == "TRUE":
            verdict_color = "verdict-true"
        elif result['verdict'] == "FALSE":
            verdict_color = "verdict-false"

        st.markdown(f"""
        <div class="verdict-card {verdict_color}">
            <h2>Verdict: {result['verdict']}</h2>
            <p class="confidence-score">Confidence: {result['confidence']}%</p>
            <p>{result['summary']}</p>
        </div>
        """, unsafe_allow_html=True)

        # Display Sources
        if result.get("sources") and result["sources"].grounding_chunks:
            st.subheader("Sources")
            for chunk in result["sources"].grounding_chunks:
                if chunk.web:
                    st.markdown(f"- [{chunk.web.title}]({chunk.web.uri})")
