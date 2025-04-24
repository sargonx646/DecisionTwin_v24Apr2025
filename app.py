import streamlit as st
from agents.extractor import extract_decision_structure
from agents.persona_builder import build_personas
from agents.orchestrator import run_simulation
from agents.summarizer import summarize_transcript
from utils.visualizer import show_heatmap, show_network_graph

st.set_page_config(page_title="DecisionTwin", layout="wide")
st.title("🤖 DecisionTwin - AI Decision Simulation")

st.sidebar.header("Simulation Control")
mode = st.sidebar.selectbox("Simulation Mode", ["Policy Debate", "Budget Allocation", "Crisis Response"])
step = st.sidebar.radio("Step", ["1. Input Dilemma", "2. Extract Structure", "3. Generate Personas", "4. Simulate", "5. Summary"])

if step == "1. Input Dilemma":
    st.subheader("Define Your Dilemma")
    user_input = st.text_area("Describe a policy or strategic dilemma:", "The government must decide how to allocate a limited budget across healthcare, defense, and climate resilience.")
    st.session_state['dilemma'] = user_input

if step == "2. Extract Structure":
    if 'dilemma' in st.session_state:
        structure = extract_decision_structure(st.session_state['dilemma'])
        st.session_state['structure'] = structure
        st.json(structure)

if step == "3. Generate Personas":
    if 'structure' in st.session_state:
        personas = build_personas(st.session_state['structure'])
        st.session_state['personas'] = personas
        for p in personas:
            st.markdown(f"**{p['name']}** — *{p['role']}* \nBias: {p['bias']} | Tone: {p['tone']}")

if step == "4. Simulate":
    if 'personas' in st.session_state:
        transcript = run_simulation(st.session_state['personas'], mode=mode)
        st.session_state['transcript'] = transcript
        for line in transcript:
            st.markdown(f"**{line['speaker']}**: {line['content']}")

if step == "5. Summary":
    if 'transcript' in st.session_state:
        summary = summarize_transcript(st.session_state['transcript'])
        st.write("### Key Takeaways")
        st.write(summary['summary'])
        show_heatmap(summary['heatmap'])
        show_network_graph(summary['graph'])