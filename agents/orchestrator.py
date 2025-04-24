def run_simulation(personas, mode="Policy Debate"):
    from agents.moderator import Moderator
    from agents.state_tracker import StateTracker
    
    moderator = Moderator(mode=mode)
    state = StateTracker(personas)
    transcript = []

    while not state.finished():
        speaker = state.next_speaker()
        prompt = moderator.prompt(speaker, state)
        response = speaker['llm'](prompt)
        transcript.append({"speaker": speaker['name'], "content": response})
        state.record_response(speaker, response)

    return transcript