# Conceptual Mapper Plugin
# Focus: structure, relationships, conceptual clarity

def register(engine):

    config = {
        "name": "conceptual_mapper",
        "type": "refinement",

        "refine": [
            "- Identify key concepts.",
            "- Map relationships between ideas.",
            "- Highlight structural dependencies.",
            "- Clarify conceptual hierarchy.",
        ]
    }

    engine.add_refinement("conceptual_mapper", config)