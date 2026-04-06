# studio_engine.py
#
# Core engine for Scholarly Prompt Studio.
# Handles modes, suggestion packs, refinement plugins, and output formatters.


class _KernelState:
    def __init__(self, engine):
        self.engine = engine
        self.mode = engine.active_mode

    def update_mode(self, mode_name: str):
        self.mode = mode_name
        self.engine.active_mode = mode_name
        self.engine.current_mode = mode_name


class _Kernel:
    def __init__(self, engine):
        self.engine = engine
        self.state = _KernelState(engine)

    def summary(self):
        return {
            "mode": self.engine.current_mode,
            "plugins_active": (
                len(self.engine.modes)
                + len(self.engine.suggestion_packs)
                + len(self.engine.refinement_plugins)
                + len(self.engine.output_plugins)
            ),
            "suggestion_density": 1.0,
            "refinement_depth": self.engine.refinement_depth,
            "output_complexity": 1.0,
        }


class StudioEngine:
    """
    Core engine for Scholarly Prompt Studio.
    Manages:
      - cognitive modes
      - suggestion packs
      - refinement plugins
      - output formatters
    """

    def __init__(self):
        # -----------------------------
        # Registries
        # -----------------------------
        self.modes = {}
        self.suggestion_packs = {}
        self.refinement_plugins = {}
        self.output_plugins = {}

        # -----------------------------
        # Active state
        # -----------------------------
        self.active_mode = "default"
        # Backwards-compatible alias
        self.current_mode = self.active_mode
        self.refinement_depth = 1

        # Suggestion usage metrics
        self.suggestions_used = 0
        self.suggestions_ignored = 0

        # Default tint (indigo-ish)
        self.tint = (0.25, 0.32, 0.71, 1)

        # Minimal kernel object for controller
        self.kernel = _Kernel(self)

    # ------------------------------------------------------------
    # MODE REGISTRATION
    # ------------------------------------------------------------
    def add_mode(self, name, config):
        """
        Register a cognitive mode plugin.
        Expected config keys:
          - tint
          - suggestions
          - prompt_guidance
          - refinement
        """
        self.modes[name] = config

    # ------------------------------------------------------------
    # SUGGESTION PACK REGISTRATION
    # ------------------------------------------------------------
    def add_suggestion_pack(self, name, config):
        """
        Register a suggestion pack plugin.
        Expected config keys:
          - suggestions: { "task": [...], "context": [...], ... }
        """
        self.suggestion_packs[name] = config

    # ------------------------------------------------------------
    # REFINEMENT PLUGIN REGISTRATION
    # ------------------------------------------------------------
    def add_refinement(self, name, config):
        """
        Register a refinement plugin.
        Expected config keys:
          - refine: [list of refinement guidance strings]
        """
        self.refinement_plugins[name] = config

    # ------------------------------------------------------------
    # OUTPUT FORMATTER REGISTRATION
    # ------------------------------------------------------------
    def add_output(self, name, config):
        """
        Register an output formatting plugin.
        Expected config keys:
          - format: [list of formatting guidance strings]
        """
        self.output_plugins[name] = config

    # ------------------------------------------------------------
    # MODE ACTIVATION
    # ------------------------------------------------------------
    def activate_mode(self, name):
        """
        Switch to a registered mode and update tint.
        """
        if name in self.modes:
            self.active_mode = name
            self.current_mode = name
            mode = self.modes[name]

            if "tint" in mode:
                self.tint = mode["tint"]

    # ------------------------------------------------------------
    # SUGGESTION AGGREGATION (INTERNAL)
    # ------------------------------------------------------------
    def _aggregate_suggestions(self):
        """
        Merge suggestions from:
          - all suggestion packs
          - the active mode (if it defines suggestions)
        Returns a dict with keys:
          - task, context, requirements, style
        """
        merged = {
            "task": [],
            "context": [],
            "requirements": [],
            "style": [],
        }

        # From suggestion packs
        for pack in self.suggestion_packs.values():
            suggestions = pack.get("suggestions", {})
            for key, items in suggestions.items():
                if key in merged:
                    merged[key].extend(items)

        # From active mode
        mode = self.modes.get(self.active_mode, {})
        mode_suggestions = mode.get("suggestions", {})
        for key, items in mode_suggestions.items():
            if key in merged:
                merged[key].extend(items)

        return merged

    # ------------------------------------------------------------
    # PUBLIC SUGGESTION API (controller expects this)
    # ------------------------------------------------------------
    def get_suggestions(self, field, text):
        """
        Controller calls: get_suggestions(field, text)
        We ignore `text` for now and just return suggestions
        relevant to the given field.
        """
        all_suggestions = self._aggregate_suggestions()
        return all_suggestions.get(field, [])

    def register_suggestion_used(self):
        self.suggestions_used += 1

    def register_suggestion_ignored(self):
        self.suggestions_ignored += 1

    # ------------------------------------------------------------
    # PROMPT GENERATION (CORE)
    # ------------------------------------------------------------
    def generate_prompt(self, task, context, requirements, style):
        """
        Build a structured prompt from the four main fields
        plus active mode guidance (if available).
        """
        lines = []

        if task:
            lines.append(f"Task:\n{task.strip()}")
        if context:
            lines.append(f"Context:\n{context.strip()}")
        if requirements:
            lines.append(f"Requirements:\n{requirements.strip()}")
        if style:
            lines.append(f"Style:\n{style.strip()}")

        # Mode-specific prompt guidance
        mode = self.modes.get(self.active_mode, {})
        guidance = mode.get("prompt_guidance", [])
        if guidance:
            lines.append("Mode Guidance:")
            for g in guidance:
                lines.append(g)

        return "\n\n".join(lines)

    # ------------------------------------------------------------
    # REFINEMENT PIPELINE (CORE)
    # ------------------------------------------------------------
    def refine_text(self, text):
        """
        Apply refinement plugins as guidance.
        For now, this appends refinement rules as meta-guidance.
        """
        refined = text

        for plugin in self.refinement_plugins.values():
            rules = plugin.get("refine", [])
            if rules:
                refined += "\n\nRefinement Guidance:"
                for rule in rules:
                    refined += f"\n{rule}"

        return refined

    # ------------------------------------------------------------
    # OUTPUT FORMATTING (CORE)
    # ------------------------------------------------------------
    def format_output(self, text):
        """
        Apply output formatting plugins as guidance.
        For now, this appends formatting rules.
        """
        formatted = text

        for plugin in self.output_plugins.values():
            rules = plugin.get("format", [])
            if rules:
                formatted += "\n\nOutput Formatting:"
                for rule in rules:
                    formatted += f"\n{rule}"

        return formatted

    # ------------------------------------------------------------
    # CONTROLLER-COMPATIBLE API
    # ------------------------------------------------------------
    def generate(self, task, context, requirements, source, style):
        """
        Controller calls this from on_generate().
        `source` is currently unused but kept for future expansion.
        """
        base = self.generate_prompt(task, context, requirements, style)
        return self.format_output(base)

    def refine(self, original, notes, target_style):
        """
        Controller calls this from on_refine().
        For now we just combine inputs and run through refinement + formatting.
        """
        lines = [original]
        if notes:
            lines.append(f"Refinement Notes:\n{notes.strip()}")
        if target_style:
            lines.append(f"Target Style:\n{target_style.strip()}")

        combined = "\n\n".join(lines)
        refined = self.refine_text(combined)
        return self.format_output(refined)