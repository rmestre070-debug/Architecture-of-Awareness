# Hermeneutic Mode Plugin
# Focus: interpretation, meaning, context, textual depth

def register(engine):

    config = {
        "tint": (0.85, 0.55, 0.10, 1),  # warm amber

        "suggestions": {
            "context": [
                "Clarify the interpretive framework.",
                "Identify the historical or cultural background.",
            ],
            "requirements": [
                "Specify the interpretive lens being applied.",
                "Include assumptions or presuppositions.",
            ],
            "style": [
                "Emphasize nuance and layered meaning.",
            ],
        },

        "prompt_guidance": [
            "- Focus on interpretation and meaning.",
            "- Identify underlying assumptions.",
            "- Explore multiple layers of significance.",
        ],

        "refinement": [
            "- Deepen interpretive clarity.",
            "- Highlight contextual nuance.",
        ],
    }

    engine.add_mode("hermeneutic", config)