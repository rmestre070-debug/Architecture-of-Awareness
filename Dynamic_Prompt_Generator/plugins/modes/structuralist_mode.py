# Structuralist Mode Plugin
# Focus: systems, relations, patterns, underlying structures

def register(engine):

    config = {
        "tint": (0.20, 0.45, 0.85, 1),  # cool blue

        "suggestions": {
            "context": [
                "Identify the underlying structure or system.",
                "Clarify relationships between components.",
            ],
            "requirements": [
                "Specify rules, patterns, or constraints.",
                "Include structural mapping or hierarchy.",
            ],
            "style": [
                "Analytical, systematic, pattern-focused.",
            ],
        },

        "prompt_guidance": [
            "- Emphasize structural relationships.",
            "- Identify patterns and rules.",
            "- Clarify system-level organization.",
        ],

        "refinement": [
            "- Strengthen structural clarity.",
            "- Highlight relational coherence.",
        ],
    }

    engine.add_mode("structuralist", config)