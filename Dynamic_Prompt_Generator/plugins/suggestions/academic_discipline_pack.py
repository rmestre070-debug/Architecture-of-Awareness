# Academic Discipline Suggestion Pack
# Focus: domain-specific framing across fields

def register(engine):

    config = {
        "name": "academic_discipline_pack",
        "type": "suggestions",

        "suggestions": {
            "task": [
                "Frame the task within a specific discipline.",
                "Identify disciplinary assumptions.",
            ],
            "context": [
                "Clarify domain-specific background.",
            ],
            "requirements": [
                "Include discipline-appropriate methodology.",
            ],
        }
    }

    engine.add_suggestion_pack("academic_discipline_pack", config)