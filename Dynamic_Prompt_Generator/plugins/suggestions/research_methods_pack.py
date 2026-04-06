# Research Methods Suggestion Pack
# Focus: methodology, rigor, design

def register(engine):

    config = {
        "name": "research_methods_pack",
        "type": "suggestions",

        "suggestions": {
            "task": [
                "Specify research question.",
                "Identify methodological approach.",
            ],
            "context": [
                "Clarify data sources or evidence.",
            ],
            "requirements": [
                "Include methodological justification.",
                "Address limitations or constraints.",
            ],
            "style": [],
        }
    }

    engine.add_suggestion_pack("research_methods_pack", config)