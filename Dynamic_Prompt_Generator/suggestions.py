# ============================================================
# suggestions.py — Adaptive Suggestion Engine (Phase 1)
# ============================================================

"""
This module provides adaptive, lightweight suggestions for the
Scholarly Prompt Studio. It is intentionally offline, fast, and
modular. It will later integrate with:

- Awareness Engine (Phase 2)
- Plugin System (Phase 3)
- Hybrid AI (Phase 5)

For now, it provides:
- Field-specific suggestions
- Engagement tracking
- Adaptive suggestion count
- Hooks for future cognitive modes
"""

from textwrap import dedent


class SuggestionEngine:

    def __init__(self):
        # Engagement score increases when user taps suggestions
        # and decreases when ignored.
        self.engagement_score = 0

        # Range: 0 (minimal) → 10 (high assist)
        self.min_suggestions = 1
        self.max_suggestions = 5

    # ------------------------------------------------------------
    # PUBLIC API
    # ------------------------------------------------------------

    def get_suggestions(self, field, text, mode="default"):
        """
        Returns a list of suggestions for a given field.
        Adaptive count based on engagement.
        """
        base = []

        if field == "task":
            base = self._task_suggestions(text, mode)
        elif field == "context":
            base = self._context_suggestions(text, mode)
        elif field == "requirements":
            base = self._requirements_suggestions(text, mode)
        elif field == "style":
            base = self._style_suggestions(text, mode)

        # Adaptive count
        count = self._adaptive_count()
        return base[:count]

    def register_engagement(self):
        """Called when user taps a suggestion chip."""
        self.engagement_score = min(10, self.engagement_score + 1)

    def register_ignore(self):
        """Called when user ignores suggestions for a while."""
        self.engagement_score = max(0, self.engagement_score - 1)

    # ------------------------------------------------------------
    # ADAPTIVE LOGIC
    # ------------------------------------------------------------

    def _adaptive_count(self):
        """
        Engagement score determines how many suggestions to show.
        0–2 → 1 suggestion
        3–5 → 2 suggestions
        6–8 → 3 suggestions
        9–10 → 5 suggestions
        """
        s = self.engagement_score

        if s <= 2:
            return 1
        if s <= 5:
            return 2
        if s <= 8:
            return 3
        return 5

    # ------------------------------------------------------------
    # SUGGESTION LOGIC (Phase 1 — heuristic only)
    # ------------------------------------------------------------

    def _task_suggestions(self, text, mode):
        t = text.lower()

        suggestions = []

        if "awareness" in t:
            suggestions.append("Frame awareness as a multi-layer cognitive process.")
            suggestions.append("Consider phenomenological vs functional perspectives.")
            suggestions.append("Explore awareness as an emergent system property.")

        if "architecture" in t:
            suggestions.append("Break the system into modules and flows.")
            suggestions.append("Identify constraints and interfaces.")
            suggestions.append("Map information-processing pathways.")

        if "research" in t:
            suggestions.append("Define the research question explicitly.")
            suggestions.append("Identify methods or frameworks to apply.")
            suggestions.append("Clarify expected contributions or outcomes.")

        # Generic fallback
        if not suggestions:
            suggestions.append("Clarify the core objective of the task.")
            suggestions.append("Identify the domain or discipline involved.")
            suggestions.append("Specify the intended audience or purpose.")

        return suggestions

    def _context_suggestions(self, text, mode):
        return [
            "Provide background so the prompt stands alone.",
            "Identify assumptions or constraints.",
            "Describe the environment or system involved.",
            "Clarify the scope and boundaries.",
        ]

    def _requirements_suggestions(self, text, mode):
        return [
            "Ensure clarity and precision.",
            "Use structured, academic language.",
            "Include reasoning steps or justification.",
            "Highlight constraints or evaluation criteria.",
        ]

    def _style_suggestions(self, text, mode):
        return [
            "Use a formal, scholarly tone.",
            "Aim for conceptual density.",
            "Maintain clarity and coherence.",
            "Adopt a reflective or analytical voice.",
        ]