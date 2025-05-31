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
step = st.sidebar.radio("Step", ["1. Input Dilemma", "2. Extract Structure", "3. Generate Personas", "4. Simulate", "5. Summary"], key="step_selection")

st.sidebar.markdown("---") # Adds a horizontal rule for separation
if st.sidebar.button("Reset Simulation"):
    keys_to_clear = ['dilemma', 'structure', 'personas', 'transcript', 'summary', 'step_selection']
    for key_to_del in keys_to_clear: # Renamed 'key' to 'key_to_del' to avoid conflict with 'key' parameter in radio
        if key_to_del in st.session_state:
            del st.session_state[key_to_del]
    # To ensure the step selection resets, we might need to explicitly reset
    # the radio button's state if it's tied to session_state or just rerun.
    # Forcing a rerun is usually the most straightforward way to reset the view.
    st.experimental_rerun()

if step == "1. Input Dilemma":
    st.subheader("Step 1: Define Your Dilemma")
    user_input = st.text_area("Describe a policy or strategic dilemma:", "The government must decide how to allocate a limited budget across healthcare, defense, and climate resilience.", height=150)
    st.caption("Clearly define the problem, the main parties involved, and the core conflict or decision to be made.")
    st.session_state['dilemma'] = user_input

if step == "2. Extract Structure":
    st.subheader("Step 2: Extracted Decision Structure")
    if 'dilemma' in st.session_state:
        with st.spinner("Extracting structure..."):
            try:
                structure = extract_decision_structure(st.session_state['dilemma'])
                st.session_state['structure'] = structure
                st.markdown("The extracted structure below outlines the key components of your dilemma, such as stakeholders, their initial positions, and the central conflict. This forms the basis for persona generation.")
                st.json(structure)
            except Exception as e:
                st.error(f"Failed to extract structure. Please check the dilemma input or try again later. Error: {e}")
    else:
        st.info("Please define a dilemma in Step 1.")

if step == "3. Generate Personas":
    st.subheader("Step 3: Generated AI Personas")
    if 'structure' in st.session_state:
        with st.spinner("Generating personas..."):
            try:
                personas = build_personas(st.session_state['structure'])
                st.session_state['personas'] = personas
                st.markdown("Based on the extracted structure, AI-generated personas representing different stakeholders are created below. Expand each to see their details.")
                for p in personas:
                    with st.expander(f"{p['name']} ({p['role']})"):
                        st.markdown(f"**Bias:** {p['bias']}  \n**Tone:** {p['tone']}")
                        # Add other persona details if available, e.g.
                        if 'details' in p:
                            st.markdown(f"**Details:** {p['details']}")
            except Exception as e:
                st.error(f"Failed to generate personas. Please ensure the structure was extracted correctly. Error: {e}")
    else:
        st.info("Please extract the structure in Step 2 first.")

if step == "4. Simulate":
    st.subheader(f"Step 4: {mode} Simulation")
    if 'personas' in st.session_state:
        st.markdown(f"The simulation will now run based on the generated personas and the selected '{mode}' mode. Observe the debate or interaction below.")
        with st.spinner(f"Running {mode} simulation..."):
            try:
                transcript = run_simulation(st.session_state['personas'], mode=mode, dilemma=st.session_state.get('dilemma', ''))
                st.session_state['transcript'] = transcript
                with st.container(height=400): # Or another appropriate height
                    for line in transcript:
                        st.markdown(f"**{line['speaker']}**: {line['content']}")
            except Exception as e:
                st.error(f"Simulation failed. Please try again later or with different personas/settings. Error: {e}")
    else:
        st.info("Please generate personas in Step 3 first.")

if step == "5. Summary":
    st.subheader("Step 5: Simulation Summary & Analysis")
    if 'transcript' in st.session_state:
        summary_data = None # Initialize summary_data
        with st.spinner("Generating summary..."):
            try:
                summary_data = summarize_transcript(st.session_state['transcript'])
                st.session_state['summary'] = summary_data # Save to session state if needed
            except Exception as e:
                st.error(f"Failed to generate summary. Please ensure the simulation ran correctly. Error: {e}")

        if summary_data:
            tab1, tab2, tab3 = st.tabs(["Key Takeaways", "Sentiment Heatmap", "Interaction Graph"])

            with tab1:
                st.write("### Detailed Summary")
                st.write(summary_data.get('summary', "No summary content available."))

            with tab2:
                st.write("### Sentiment Heatmap")
                if 'heatmap' in summary_data:
                    show_heatmap(summary_data['heatmap'])
                else:
                    st.warning("Heatmap data not available in the summary.")

            with tab3:
                st.write("### Interaction Graph")
                if 'graph' in summary_data:
                    show_network_graph(summary_data['graph'])
                else:
                    st.warning("Interaction graph data not available in the summary.")
        else:
            st.warning("No summary could be generated. Please ensure the simulation ran successfully.")
    else:
        st.info("Please run a simulation in Step 4 first.")