# Outline Generator Plugin
# Focus: hierarchical structure, academic outlines

def register(engine):

    config = {
        "name": "outline_generator",
        "type": "output",

        "format": [
            "- Provide hierarchical outline.",
            "- Use numbered sections.",
            "- Include subpoints and structure.",
            "- Maintain academic clarity.",
        ]
    }

    engine.add_output("outline_generator", config)