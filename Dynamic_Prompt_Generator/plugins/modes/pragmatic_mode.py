# Pragmatic Mode Plugin
# Focus: usefulness, application, real-world outcomes

def register(engine):

    config = {
        "tint": (0.10, 0.60, 0.10, 1),  # green

        "suggestions": {
            "context": [
                "Clarify the practical setting or use case.",
                "Identify constraints or real-world conditions.",
            ],
            "requirements": [
                "Specify measurable outcomes.",
                "Include actionable steps.",
            ],
            "style": [
                "Direct, concise, outcome-oriented.",
            ],
        },

        "prompt_guidance": [
            "- Emphasize practical consequences.",
            "- Focus on actionable insights.",
            "- Prioritize clarity and utility.",
        ],

        "refinement": [
            "- Increase practical relevance.",
            "- Strengthen clarity of outcomes.",
        ],
    }

    engine.add_mode("pragmatic", config)