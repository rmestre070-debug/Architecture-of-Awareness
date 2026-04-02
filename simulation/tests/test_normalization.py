import awarenessdynamicsmodelv33 as sim

def test_normalize_value_bounds():
    assert sim.normalize_value(-1) == 0
    assert sim.normalize_value(2) == 1

def test_normalize_value_midpoint():
    assert sim.normalize_value(0.5) == 0.5
