import awarenessdynamicsmodelv33 as sim

def test_state_update_changes_values():
    state = sim.initialize_state()
    updated = sim.update_state(state, {"stimulus": 0.3})

    assert updated["awareness"] != state["awareness"]
    assert updated["energy"] != state["energy"]

def test_state_update_keeps_values_in_range():
    state = sim.initialize_state()
    updated = sim.update_state(state, {"stimulus": 10})

    for key, value in updated.items():
        assert 0 <= value <= 1
