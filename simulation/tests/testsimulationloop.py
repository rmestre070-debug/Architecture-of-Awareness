import awarenessdynamicsmodelv33 as sim

def test_simulation_runs_fixed_steps():
    result = sim.run_simulation(steps=5)
    assert isinstance(result, dict)
    assert "history" in result
    assert len(result["history"]) == 5

def test_simulation_state_progression():
    result = sim.run_simulation(steps=3)
    history = result["history"]

    # Ensure state actually changes over time
    assert history[0] != history[-1]
