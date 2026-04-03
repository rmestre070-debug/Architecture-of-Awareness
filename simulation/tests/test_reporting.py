import awarenessdynamicsmodelv33 as sim

def test_generate_report_structure():
    state = sim.initialize_state()
    report = sim.generate_report(state)

    assert isinstance(report, dict)
    assert "summary" in report
    assert "awareness_level" in report

def test_generate_report_values():
    state = {"awareness": 0.8, "energy": 0.6, "focus": 0.7}
    report = sim.generate_report(state)

    assert report["awareness_level"] == "high"
