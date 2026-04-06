# Cognitive Science Suggestion Pack
# Focus: cognition, perception, memory, reasoning

def register(engine):

    config = {
        "name": "cognitive_science_pack",
        "type": "suggestions",

        "suggestions": {
            "task": [
                "Analyze cognitive mechanisms involved.",
                "Identify relevant cognitive processes.",
            ],
            "context": [
                "Specify theoretical framework.",
                "Clarify empirical background.",
            ],
            "requirements": [
                "Include cognitive architecture elements.",
                "Reference relevant models or theories.",
            ],
        }
    }

    engine.add_suggestion_pack("cognitive_science_pack", config)