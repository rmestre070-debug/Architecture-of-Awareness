# Argument Strengthener Plugin
# Focus: logical force, coherence, justification

def register(engine):

    config = {
        "name": "argument_strengthener",
        "type": "refinement",

        "refine": [
            "- Strengthen logical transitions.",
            "- Add justification for key claims.",
            "- Clarify premises and conclusions.",
            "- Identify missing inferential steps.",
        ]
    }

    engine.add_refinement("argument_strengthener", config)