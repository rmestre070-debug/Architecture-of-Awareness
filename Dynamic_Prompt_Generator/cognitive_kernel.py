# ============================================================
# Cognitive Kernel (Phase 4)
# Architecture-of-Awareness — Scholarly Prompt Studio
# ============================================================

from dataclasses import dataclass, field
from typing import List, Dict, Callable


@dataclass
class CognitiveState:
    """Tracks the evolving internal state of the engine."""
    mode: str = "default"
    last_action: str = None
    last_plugins: List[str] = field(default_factory=list)
    suggestion_density: float = 1.0
    refinement_depth: int = 1
    output_complexity: float = 1.0
    user_interaction_count: int = 0
    mode_switch_count: int = 0

    def update_mode(self, new_mode: str):
        if new_mode != self.mode:
            self.mode_switch_count += 1
        self.mode = new_mode


@dataclass
class CognitiveKernel:
    """Orchestrates plugins, resolves conflicts, and adapts behavior."""
    state: CognitiveState = field(default_factory=CognitiveState)

    # Plugin registries
    suggestion_plugins: List[Callable] = field(default_factory=list)
    refinement_plugins: List[Callable] = field(default_factory=list)
    output_plugins: List[Callable] = field(default_factory=list)

    # Priority maps
    priorities: Dict[str, int] = field(default_factory=dict)

    # ------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------

    def register_suggestion_plugin(self, fn: Callable, name: str):
        self.suggestion_plugins.append(fn)
        self.priorities[name] = 10  # default priority

    def register_refinement_plugin(self, fn: Callable, name: str):
        self.refinement_plugins.append(fn)
        self.priorities[name] = 10

    def register_output_plugin(self, fn: Callable, name: str):
        self.output_plugins.append(fn)
        self.priorities[name] = 10

    # ------------------------------------------------------------
    # Priority Management
    # ------------------------------------------------------------

    def set_priority(self, plugin_name: str, value: int):
        self.priorities[plugin_name] = value

    def sort_plugins(self, plugins: List[Callable]) -> List[Callable]:
        """Sort plugins by priority (higher runs first)."""
        return sorted(
            plugins,
            key=lambda fn: self.priorities.get(fn.__name__, 10),
            reverse=True,
        )

    # ------------------------------------------------------------
    # Conflict Resolution
    # ------------------------------------------------------------

    def resolve_conflicts(self, outputs: List[str]) -> str:
        """
        Simple conflict resolution:
        - If outputs are identical → return one
        - If outputs differ → merge with separators
        """
        unique = list(dict.fromkeys(outputs))
        if len(unique) == 1:
            return unique[0]
        return "\n\n---\n\n".join(unique)

    # ------------------------------------------------------------
    # Suggestion Pipeline
    # ------------------------------------------------------------

    def apply_suggestion_pipeline(self, field: str, text: str, base: List[str], mode: str):
        self.state.last_action = "suggest"
        self.state.user_interaction_count += 1

        outputs = []
        for fn in self.sort_plugins(self.suggestion_plugins):
            try:
                out = fn(field, text, base, mode)
                outputs.append(out)
            except Exception:
                continue

        if not outputs:
            return base

        # Merge plugin outputs
        merged = []
        for out in outputs:
            for item in out:
                if item not in merged:
                    merged.append(item)

        return merged

    # ------------------------------------------------------------
    # Refinement Pipeline
    # ------------------------------------------------------------

    def apply_refinement_pipeline(self, text: str, mode: str):
        self.state.last_action = "refine"
        self.state.refinement_depth += 1

        outputs = []
        for fn in self.sort_plugins(self.refinement_plugins):
            try:
                out = fn(text, mode)
                outputs.append(out)
            except Exception:
                continue

        if not outputs:
            return text

        return self.resolve_conflicts(outputs)

    # ------------------------------------------------------------
    # Output Pipeline
    # ------------------------------------------------------------

    def apply_output_pipeline(self, text: str, mode: str):
        self.state.last_action = "output"
        self.state.output_complexity += 0.1

        outputs = []
        for fn in self.sort_plugins(self.output_plugins):
            try:
                out = fn(text, mode)
                outputs.append(out)
            except Exception:
                continue

        if not outputs:
            return text

        return self.resolve_conflicts(outputs)

    # ------------------------------------------------------------
    # Adaptive Behavior
    # ------------------------------------------------------------

    def adapt(self):
        """
        Adjust internal parameters based on user behavior.
        This is intentionally simple — a foundation for future evolution.
        """

        # If user switches modes often → increase suggestion density
        if self.state.mode_switch_count > 3:
            self.state.suggestion_density = min(2.0, self.state.suggestion_density + 0.1)

        # If refinement depth grows → increase output complexity
        if self.state.refinement_depth > 3:
            self.state.output_complexity = min(2.0, self.state.output_complexity + 0.1)

        # If user interacts heavily → reduce suggestion density (avoid overload)
        if self.state.user_interaction_count > 20:
            self.state.suggestion_density = max(0.5, self.state.suggestion_density - 0.1)

    # ------------------------------------------------------------
    # Kernel Summary (for UI)
    # ------------------------------------------------------------

    def summary(self):
        return {
            "mode": self.state.mode,
            "suggestion_density": round(self.state.suggestion_density, 2),
            "refinement_depth": self.state.refinement_depth,
            "output_complexity": round(self.state.output_complexity, 2),
            "plugins_active": len(self.suggestion_plugins)
                              + len(self.refinement_plugins)
                              + len(self.output_plugins),
        }