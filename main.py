import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from crewai import Crew, Process
from agents import AutomatedOutreachAgents
from tasks import AutomatedOutreachTasks
import re

# --- UI Configuration ---
st.set_page_config(layout="wide", page_title="🤖 Automated Outreach | Query Station")

# Custom CSS for Cyberpunk/Dark Theme
st.markdown("""
<style>
    /* Global Background */
    .stApp {
        background-color: #0E1117;
        color: #e0e0e0;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #00F2FF !important;
        font-family: 'Courier New', Courier, monospace;
        text-shadow: 0 0 10px #00F2FF;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #161B22;
        border-right: 1px solid #30363D;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #1F6FEB;
        color: white;
        border: 1px solid #1F6FEB;
        box-shadow: 0 0 10px #1F6FEB;
    }
    .stButton>button:hover {
        background-color: #00F2FF;
        color: black;
        box-shadow: 0 0 20px #00F2FF;
    }
    
    /* Cards/Containers */
    .lead-card {
        background-color: #161B22;
        border: 1px solid #30363D;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    
    /* Confidence Meters */
    .conf-green { color: #2EA043; font-weight: bold; }
    .conf-yellow { color: #D29922; font-weight: bold; }
    .conf-red { color: #F85149; font-weight: bold; }
    
</style>
""", unsafe_allow_html=True)

# --- Session State ---
if 'leads_data' not in st.session_state:
    st.session_state.leads_data = []  # List of dicts: {name, url, hook, confidence, email_draft}
if 'explanation_data' not in st.session_state:
    st.session_state.explanation_data = ""
if 'search_performed' not in st.session_state:
    st.session_state.search_performed = False

# --- Sidebar ---
st.sidebar.title("Query Station")
st.sidebar.markdown("---")
target_topic = st.sidebar.text_input("Target Tech Topic", "React Performance")
problem_context = st.sidebar.text_area("Problem Context", "e.g. High latency on mobile devices")
search_depth = st.sidebar.slider("Search Depth", 1, 10, 5)
launch_btn = st.sidebar.button("INITIATE SEQUENCE")

# --- Main Workspace ---
st.title("🤖 AUTOMATED OUTREACH")

if launch_btn and target_topic:
    with st.spinner("Agents Deploying... Scouring the Network..."):
        # Initialize Agents & Tasks
        agents = AutomatedOutreachAgents()
        tasks = AutomatedOutreachTasks()
        
        scout = agents.technical_scout()
        ghost = agents.ghostwriter()
        
        # Crew 1: Scout
        # We run them sequentially or as a single process, but to parse intermediate output 
        # ideally we act on the scout's output. For simplicity, let's run a full crew.
        
        task1 = tasks.find_leads_task(scout, target_topic, search_depth)
        
        crew = Crew(
            agents=[scout],
            tasks=[task1],
            verbose=True
        )
        
        scout_result = crew.kickoff()
        
        # Parse Scout Result (Mocking parsing logic for the demo if LLM output is unstructured)
        # In a real robust app, we'd use Pydantic models for structured output. 
        # Here we will do a simple text pass to the Ghostwriter.
        
        task2 = tasks.draft_email_task(ghost, scout_result)
        
        crew2 = Crew(
            agents=[ghost],
            tasks=[task2],
            verbose=True
        )
        
        email_results = crew2.kickoff()

        # Task 3: Solution Explanation (Independent)
        task3 = tasks.explain_solution_task(ghost, target_topic, problem_context)
        crew3 = Crew(
            agents=[ghost],
            tasks=[task3],
            verbose=True
        )
        explanation_result = crew3.kickoff()
            
        # Store results in Session State (Simplified parsing)
        # We will just display the raw text for now if parsing is complex, 
        # but let's try to structure it minimally.
        
        st.session_state.leads_data = [
            # Dummy structure for visualization if parsing fails, 
            # ideally we parse `scout_result` which is a string.
            {'raw_scout': str(scout_result), 'raw_email': str(email_results)}
        ]
        st.session_state.explanation_data = str(explanation_result)
        st.session_state.search_performed = True

# --- Results Display ---
if st.session_state.search_performed:
    st.subheader("Mission Report")
    
    # Since we didn't strictly force JSON output (CrewAI can be unpredictable with exact JSON),
    # We will display the agent outputs in our Review Deck.
    
    data = st.session_state.leads_data[0]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"### 📡 Scout Intel")
        st.info("Raw Intelligence gathered from the field:")
        st.markdown(f"```\n{data['raw_scout']}\n```")
        
        # Simulated Confidence Meter based on text analysis
        if "Green" in data['raw_scout']:
            st.markdown('<p class="conf-green"> Confidence: HIGH (Specific Problem Found)</p>', unsafe_allow_html=True)
        elif "Yellow" in data['raw_scout']:
            st.markdown('<p class="conf-yellow"> Confidence: MEDIUM (Inferred Stack)</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p class="conf-red"> Confidence: LOW (Generic Signal)</p>', unsafe_allow_html=True)

    with col2:
        st.markdown(f"### 📝 Draft Protocol")
        st.success("Ghostwriter generated outreach:")
        st.text_area("Email Draft", value=data['raw_email'], height=400)

    # --- Explanation Section ---
    st.markdown("---")
    st.subheader("💡 Suggested Solutions")
    st.markdown(st.session_state.explanation_data)
        
else:
    st.info("Awaiting Mission Start... Enter a topic in the sidebar.")

# --- Footer ---
st.markdown("---")
st.markdown("*System Status: ONLINE | v1.0.0*")
