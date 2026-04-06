# ============================================================
# Scholarly Prompt Studio — Controller (v2.0, Clean Rebuild)
# ============================================================

import os
import json
from datetime import datetime

from kivy.lang import Builder
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.screenmanager import Screen as KivyScreen
from kivy.core.window import Window
from kivy.properties import ListProperty

from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.chip import MDChip
from kivymd.uix.menu import MDDropdownMenu

from studio_engine import StudioEngine


# ------------------------------------------------------------
# Screen Classes
# ------------------------------------------------------------

class MDScreen(KivyScreen):
    pass

class SplashScreen(MDScreen):
    pass

class GenerateScreen(MDScreen):
    pass

class RefineScreen(MDScreen):
    pass

class OutputScreen(MDScreen):
    pass

class HistoryScreen(MDScreen):
    pass

class SettingsScreen(MDScreen):
    pass


# ------------------------------------------------------------
# File Paths
# ------------------------------------------------------------

APP_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_FILE = os.path.join(APP_DIR, "settings.json")
HISTORY_FILE = os.path.join(APP_DIR, "history.json")
PLUGINS_DIR = os.path.join(APP_DIR, "plugins")


DEFAULT_SETTINGS = {
    "theme_mode": "Light",
    "accent_color": "Indigo",
    "username": "Researcher",
    "last_screen": "generate",
}


# ------------------------------------------------------------
# Settings Manager
# ------------------------------------------------------------

class SettingsManager:
    def __init__(self):
        self.data = {}
        self.load()

    def load(self):
        if not os.path.exists(SETTINGS_FILE):
            self.data = DEFAULT_SETTINGS.copy()
            self.save()
        else:
            with open(SETTINGS_FILE, "r") as f:
                self.data = json.load(f)

    def save(self):
        with open(SETTINGS_FILE, "w") as f:
            json.dump(self.data, f, indent=4)


# ------------------------------------------------------------
# History Manager
# ------------------------------------------------------------

class HistoryManager:
    def __init__(self):
        self.entries = []
        self.load()

    def load(self):
        if not os.path.exists(HISTORY_FILE):
            self.entries = []
            self.save()
        else:
            with open(HISTORY_FILE, "r") as f:
                self.entries = json.load(f)

    def save(self):
        with open(HISTORY_FILE, "w") as f:
            json.dump(self.entries, f, indent=4)

    def add(self, text, meta=None):
        entry = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "content": text,
            "meta": meta or {},
        }
        self.entries.append(entry)
        self.save()


# ------------------------------------------------------------
# Plugin Manager
# ------------------------------------------------------------

class PluginManager:
    def __init__(self, plugins_dir):
        self.plugins_dir = plugins_dir
        self.plugins = []
        self.ensure_structure()

    def ensure_structure(self):
        if not os.path.exists(self.plugins_dir):
            os.makedirs(self.plugins_dir, exist_ok=True)

        for sub in ("suggestions", "modes", "refinement", "output"):
            path = os.path.join(self.plugins_dir, sub)
            if not os.path.exists(path):
                os.makedirs(path, exist_ok=True)

    def scan(self):
        self.plugins = []
        for root, dirs, files in os.walk(self.plugins_dir):
            for f in files:
                if f.endswith(".py") and not f.startswith("_"):
                    rel = os.path.relpath(os.path.join(root, f), self.plugins_dir)
                    module = rel[:-3].replace(os.sep, ".")
                    self.plugins.append(module)

    def load_all(self, engine):
        import importlib

        self.scan()
        for module in self.plugins:
            try:
                mod = importlib.import_module(f"plugins.{module}")
                if hasattr(mod, "register"):
                    mod.register(engine)
            except Exception as e:
                print(f"Plugin load error [{module}]:", e)
                # ------------------------------------------------------------
# Main Application
# ------------------------------------------------------------

class ScholarlyStudioApp(MDApp):
    mode_tint = ListProperty([0.25, 0.32, 0.71, 1])
    kernel_tint = ListProperty([0.6, 0.6, 0.6, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.settings = SettingsManager()
        self.history = HistoryManager()
        self.plugins = PluginManager(PLUGINS_DIR)
        self.engine = StudioEngine()

        self.mode_menu = None
        self.plugins.load_all(self.engine)

    # --------------------------------------------------------
    # Utility
    # --------------------------------------------------------

    def notify(self, msg):
        toast(msg)

    def apply_theme(self):
        mode = self.settings.data.get("theme_mode", "Light")
        accent = self.settings.data.get("accent_color", "Indigo")

        self.theme_cls.primary_palette = accent
        self.theme_cls.theme_style = "Dark" if mode == "Dark" else "Light"

    # --------------------------------------------------------
    # Brain Tint (retry until icon exists)
    # --------------------------------------------------------

    def update_brain_tint(self, *args):
        try:
            toolbar = self.root.ids.toolbar

            # If icon not created yet → retry
            if not toolbar.ids.right_actions.children:
                Clock.schedule_once(self.update_brain_tint, 0.05)
                return

            icon = toolbar.ids.right_actions.children[-1]
            icon.icon_color = self.mode_tint

        except Exception as e:
            print("Brain tint update error:", e)

    # --------------------------------------------------------
    # Brain Pulse
    # --------------------------------------------------------

    def pulse_brain_icon(self):
        try:
            toolbar = self.root.ids.toolbar
            icon = toolbar.ids.right_actions.children[-1]

            anim = (
                Animation(opacity=0.6, duration=0.12, t="out_quad") +
                Animation(opacity=1.0, duration=0.18, t="out_quad")
            )
            anim.start(icon)

        except Exception as e:
            print("Brain pulse error:", e)

    # --------------------------------------------------------
    # Kernel Indicator
    # --------------------------------------------------------

    def get_kernel_status(self):
        try:
            return self.engine.kernel.summary()
        except Exception:
            return {
                "mode": self.engine.current_mode,
                "plugins_active": 0,
                "refinement_depth": 1,
            }

    def update_kernel_indicator(self):
        try:
            s = self.get_kernel_status()
            self.root.ids.kernel_indicator.text = (
                f"Kernel: {s['mode'].capitalize()} • "
                f"Plugins: {s['plugins_active']} • "
                f"Refinement Depth: {s['refinement_depth']}"
            )
        except Exception as e:
            print("Kernel indicator update error:", e)

    def pulse_kernel(self):
        try:
            bright = [min(1.0, c + 0.2) for c in self.kernel_tint]

            anim = (
                Animation(kernel_tint=bright, duration=0.12, t="out_quad") +
                Animation(kernel_tint=[0.6, 0.6, 0.6, 1], duration=0.18, t="out_quad")
            )
            anim.start(self)

            self.pulse_brain_icon()

        except Exception as e:
            print("Kernel pulse error:", e)

    # --------------------------------------------------------
    # Build + Splash
    # --------------------------------------------------------

    def build(self):
        Window.softinput_mode = "below_target"
        self.apply_theme()
        root = Builder.load_file("main.kv")
        Clock.schedule_once(lambda dt: self.animate_splash(), 0.2)
        return root

    def animate_splash(self):
        try:
            splash = self.root.ids.splash_root
            Animation(opacity=1, duration=0.8, t="out_quad").start(splash)
        except:
            pass

        target = self.settings.data.get("last_screen", "generate")
        Clock.schedule_once(lambda dt: self.switch_screen(target), 2.0)

    def switch_screen(self, name):
        try:
            self.root.ids.sm.current = name
            self.settings.data["last_screen"] = name
            self.settings.save()
        except Exception as e:
            print("Screen switch error:", e)
            # --------------------------------------------------------
    # Generate
    # --------------------------------------------------------

    def on_generate(self):
        ids = self.root.ids

        task = ids.task_field.text.strip()
        context = ids.context_field.text.strip()
        reqs = ids.requirements_field.text.strip()
        style = ids.style_field.text.strip()

        if not task:
            self.notify("Please enter a task.")
            return

        meta = {
            "mode": "generate",
            "task": task,
            "context": context,
            "requirements": reqs,
            "style": style,
            "awareness_mode": self.engine.current_mode,
        }

        output = self.engine.generate(task, context, reqs, "", style)

        self.history.add(output, meta)
        self.display_output(output)
        self.update_kernel_indicator()
        self.pulse_kernel()

    # --------------------------------------------------------
    # Refine
    # --------------------------------------------------------

    def on_refine(self):
        ids = self.root.ids

        original = ids.original_field.text.strip()
        notes = ids.notes_field.text.strip()
        target_style = ids.target_style_field.text.strip()

        if not original:
            self.notify("Original text is required.")
            return

        meta = {
            "mode": "refine",
            "notes": notes,
            "target_style": target_style,
            "awareness_mode": self.engine.current_mode,
        }

        refined = self.engine.refine(original, notes, target_style)

        self.history.add(refined, meta)
        self.display_output(refined)
        self.update_kernel_indicator()
        self.pulse_kernel()

    # --------------------------------------------------------
    # Output
    # --------------------------------------------------------

    def display_output(self, text):
        self.root.ids.output_text.text = text
        self.switch_screen("output")

    def copy_output(self):
        text = self.root.ids.output_text.text
        if text:
            from kivy.core.clipboard import Clipboard
            Clipboard.copy(text)
            self.notify("Copied to clipboard.")

    def save_output_to_history(self):
        text = self.root.ids.output_text.text
        if text:
            self.history.add(text, meta={"mode": "manual-save"})
            self.notify("Saved to history.")

    def refine_again(self):
        text = self.root.ids.output_text.text
        self.root.ids.original_field.text = text
        self.switch_screen("refine")

    # --------------------------------------------------------
    # History
    # --------------------------------------------------------

    def load_history_into_ui(self):
        field = self.root.ids.history_field

        if not self.history.entries:
            field.text = "No history yet."
            return

        lines = []
        for e in self.history.entries:
            lines.append(f"[{e['timestamp']}]\n{e['content']}\n")

        field.text = "\n".join(lines)
        # --------------------------------------------------------
    # Theme
    # --------------------------------------------------------

    def set_light_mode(self):
        self.settings.data["theme_mode"] = "Light"
        self.settings.save()
        self.apply_theme()
        self.notify("Light mode enabled.")

    def set_dark_mode(self):
        self.settings.data["theme_mode"] = "Dark"
        self.settings.save()
        self.apply_theme()
        self.notify("Dark mode enabled.")

    def set_system_mode(self):
        self.settings.data["theme_mode"] = "System"
        self.settings.save()
        self.apply_theme()
        self.notify("System mode enabled.")

    # --------------------------------------------------------
    # Awareness Modes
    # --------------------------------------------------------

    def open_mode_menu(self, caller):
        modes = self.get_all_modes()

        items = [
            {"text": m, "viewclass": "OneLineListItem",
             "on_release": lambda x=m: self.set_awareness_mode(x)}
            for m in modes
        ]

        self.mode_menu = MDDropdownMenu(
            caller=caller,
            items=items,
            width_mult=4,
        )
        self.mode_menu.open()

    def get_all_modes(self):
        base = [
            "Default",
            "Phenomenological",
            "Architecture",
            "Systemic",
            "Reflective",
            "Analytical",
        ]
        plugin_modes = [m.capitalize() for m in self.engine.modes.keys()]
        return base + plugin_modes

    def get_mode_color(self, mode):
        colors = {
            "default": (0.25, 0.32, 0.71, 1),
            "phenomenological": (1.0, 0.55, 0.0, 1),
            "architecture": (0.13, 0.59, 0.95, 1),
            "systemic": (0.0, 0.59, 0.53, 1),
            "reflective": (0.61, 0.15, 0.69, 1),
            "analytical": (0.9, 0.1, 0.1, 1),
        }

        mode = mode.lower()

        if mode in self.engine.modes:
            cfg = self.engine.modes[mode]
            if "tint" in cfg:
                return cfg["tint"]

        return colors.get(mode, colors["default"])

    def apply_mode_tint(self, mode):
        new = self.get_mode_color(mode)
        Animation(mode_tint=new, duration=0.25, t="out_quad").start(self)

        try:
            self.root.ids.mode_badge.text = f"Mode: {mode.capitalize()}"
        except:
            pass

    def set_awareness_mode(self, mode):
        self.engine.current_mode = mode.lower()

        try:
            self.engine.kernel.state.update_mode(mode.lower())
        except:
            pass

        if self.mode_menu:
            self.mode_menu.dismiss()

        self.root.ids.mode_dropdown.text = "Mode"

        self.apply_mode_tint(mode.lower())
        self.update_brain_tint()
        self.update_kernel_indicator()
        self.pulse_kernel()
        self.notify(f"Mode set to {mode}")

    # --------------------------------------------------------
    # Suggestions
    # --------------------------------------------------------

    def _bind_suggestion_listeners(self):
        ids = self.root.ids

        ids.task_field.bind(
            text=lambda i, v: self.on_field_text_changed("task", v)
        )
        ids.context_field.bind(
            text=lambda i, v: self.on_field_text_changed("context", v)
        )
        ids.requirements_field.bind(
            text=lambda i, v: self.on_field_text_changed("requirements", v)
        )
        ids.style_field.bind(
            text=lambda i, v: self.on_field_text_changed("style", v)
        )

    def on_field_text_changed(self, field, text):
        if not text.strip():
            self._clear_suggestions(field)
            return

        suggestions = self.engine.get_suggestions(field, text)
        self._update_suggestions(field, suggestions)

    def _container_for(self, field):
        return {
            "task": "task_suggestions_box",
            "context": "context_suggestions_box",
            "requirements": "requirements_suggestions_box",
            "style": "style_suggestions_box",
        }.get(field)

    def _clear_suggestions(self, field):
        box = self.root.ids.get(self._container_for(field))
        if box:
            box.clear_widgets()

    def clear_all_suggestions(self):
        for f in ("task", "context", "requirements", "style"):
            self._clear_suggestions(f)
        self.engine.register_suggestion_ignored()

    def _update_suggestions(self, field, suggestions):
        box = self.root.ids.get(self._container_for(field))
        if not box:
            return

        box.clear_widgets()

        for s in suggestions:
            chip = MDChip(
                text=s,
                icon="lightbulb-on-outline",
                check=False,
                selected_chip_color=self.mode_tint,
            )
            chip.bind(on_release=lambda i, ss=s, ff=field:
                      self.on_suggestion_chip_pressed(ff, ss))
            box.add_widget(chip)

    def on_suggestion_chip_pressed(self, field, suggestion):
        widget = self.root.ids.get(f"{field}_field")
        if not widget:
            return

        current = widget.text.strip()

        if not current:
            widget.text = suggestion
        else:
            if current.endswith((".", "?", "!", ";", ":")):
                widget.text = current + " " + suggestion
            else:
                widget.text = current + " — " + suggestion

        self.engine.register_suggestion_used()

    # --------------------------------------------------------
    # Clear Page
    # --------------------------------------------------------

    def clear_generate_page(self):
        ids = self.root.ids
        ids.task_field.text = ""
        ids.context_field.text = ""
        ids.requirements_field.text = ""
        ids.style_field.text = ""
        self.clear_all_suggestions()

    # --------------------------------------------------------
    # Lifecycle
    # --------------------------------------------------------

    def on_start(self):
        try:
            self.load_history_into_ui()
        except:
            pass

        try:
            self._bind_suggestion_listeners()
        except:
            pass

        self.update_kernel_indicator()

        # Start tint update loop
        Clock.schedule_once(self.update_brain_tint, 0.1)


if __name__ == "__main__":
    ScholarlyStudioApp().run()