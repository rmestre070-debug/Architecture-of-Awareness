# Narrative Mode Plugin
# Focus: storytelling, flow, coherence, human-centered framing

def register(engine):

    config = {
        "tint": (0.55, 0.30, 0.85, 1),  # violet

        "suggestions": {
            "context": [
                "Identify the central character or agent.",
                "Clarify the narrative setting.",
            ],
            "requirements": [
                "Include narrative arc or progression.",
                "Specify emotional or experiential tone.",
            ],
            "style": [
                "Emphasize flow, pacing, and voice.",
            ],
        },

        "prompt_guidance": [
            "- Focus on narrative coherence.",
            "- Highlight character, setting, and arc.",
            "- Maintain emotional or experiential continuity.",
        ],

        "refinement": [
            "- Improve narrative flow.",
            "- Strengthen pacing and transitions.",
        ],
    }

    engine.add_mode("narrative", config)