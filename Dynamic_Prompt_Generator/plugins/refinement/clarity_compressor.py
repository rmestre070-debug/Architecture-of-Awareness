# Clarity Compressor Plugin
# Focus: concision, precision, readability

def register(engine):

    config = {
        "name": "clarity_compressor",
        "type": "refinement",

        "refine": [
            "- Remove redundancy.",
            "- Tighten phrasing.",
            "- Increase clarity and precision.",
            "- Simplify complex sentences.",
        ]
    }

    engine.add_refinement("clarity_compressor", config)