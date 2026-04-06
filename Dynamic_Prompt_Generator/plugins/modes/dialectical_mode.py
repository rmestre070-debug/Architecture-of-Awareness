# Dialectical Mode Plugin
# Focus: tension, synthesis, contradiction, progression

def register(engine):

    config = {
        "tint": (0.75, 0.20, 0.20, 1),  # deep red

        "suggestions": {
            "context": [
                "Identify opposing positions or tensions.",
                "Clarify the central contradiction.",
            ],
            "requirements": [
                "Include thesis, antithesis, and synthesis structure.",
            ],
            "style": [
                "Emphasize dynamic progression of ideas.",
            ],
        },

        "prompt_guidance": [
            "- Highlight conceptual tensions.",
            "- Identify contradictions and their implications.",
            "- Move toward synthesis or resolution.",
        ],

        "refinement": [
            "- Strengthen dialectical structure.",
            "- Clarify the movement from tension to synthesis.",
        ],
    }

    engine.add_mode("dialectical", config)