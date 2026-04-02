import awarenessdynamicsmodelv33 as sim

def test_initial_state_structure():
    state = sim.initialize_state()
    assert isinstance(state, dict)
    assert "awareness" in state
    assert "energy" in state
    assert "focus" in state

def test_initial_values_in_range():
    state = sim.initialize_state()
    assert 0 <= state["awareness"] <= 1
    assert 0 <= state["energy"] <= 1
    assert 0 <= state["focus"] <= 1
