# Markdown Formatter Plugin
# Focus: clean, structured markdown output

def register(engine):

    config = {
        "name": "markdown_formatter",
        "type": "output",

        "format": [
            "- Use clear headings.",
            "- Use bullet lists for structure.",
            "- Use code blocks for examples.",
            "- Maintain consistent markdown style.",
        ]
    }

    engine.add_output("markdown_formatter", config)