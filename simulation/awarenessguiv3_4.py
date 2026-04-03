import tkinter as tk
from tkinter import ttk
import numpy as np
from awareness_engine_v3_4 import simulate_awareness

# ---------------------------------------------------------
# v3.4 Cognitive-Architecture GUI
# ---------------------------------------------------------

class AwarenessGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Awareness Dynamics v3.4")
        self.root.geometry("900x600")
        self.root.configure(bg="#e6e6e6")

        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.style.configure("Card.TFrame", background="#ffffff")
        self.style.configure("Header.TLabel", background="#ffffff",
                             font=("Segoe UI", 18, "bold"))
        self.style.configure("Metric.TLabel", background="#ffffff",
                             font=("Segoe UI", 11))

        # Layout
        self.build_layout()

    def build_layout(self):
        # Main container
        container = ttk.Frame(self.root, padding=20, style="Card.TFrame")
        container.pack(fill="both", expand=True)

        # Header
        header = ttk.Label(container, text="Awareness Dynamics Console",
                           style="Header.TLabel")
        header.pack(pady=(0, 20))

        # Split: left (console) / right (metrics)
        body = ttk.Frame(container, style="Card.TFrame")
        body.pack(fill="both", expand=True)

        body.columnconfigure(0, weight=3)
        body.columnconfigure(1, weight=1)

        # Console
        console_frame = ttk.Frame(body, style="Card.TFrame")
        console_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 20))

        self.console = tk.Text(console_frame, wrap="word",
                               font=("Segoe UI", 11),
                               bg="#f2f2f2", relief="flat",
                               padx=10, pady=10)
        self.console.pack(fill="both", expand=True)

        # Metrics panel
        metrics_frame = ttk.Frame(body, padding=10, style="Card.TFrame")
        metrics_frame.grid(row=0, column=1, sticky="ns")

        ttk.Label(metrics_frame, text="Metrics", font=("Segoe UI", 14, "bold"),
                  background="#ffffff").pack(pady=(0, 10))

        self.metric_A = ttk.Label(metrics_frame, text="A(t): --", style="Metric.TLabel")
        self.metric_alpha = ttk.Label(metrics_frame, text="α(t): --", style="Metric.TLabel")
        self.metric_beta = ttk.Label(metrics_frame, text="β(t): --", style="Metric.TLabel")
        self.metric_L = ttk.Label(metrics_frame, text="L(t): --", style="Metric.TLabel")
        self.metric_drift = ttk.Label(metrics_frame, text="Drift: --", style="Metric.TLabel")

        for m in [self.metric_A, self.metric_alpha, self.metric_beta,
                  self.metric_L, self.metric_drift]:
            m.pack(anchor="w", pady=5)

        # Run button
        run_button = ttk.Button(container, text="Run Simulation",
                                command=self.run_simulation)
        run_button.pack(pady=15)

    def run_simulation(self):
        self.console.delete("1.0", tk.END)
        self.console.insert(tk.END, "Running simulation...\n")

        data = simulate_awareness(T=20.0, dt=0.002, seed=42)

        A = data["A"]
        alpha = data["alpha"]
        beta = data["beta"]
        L = data["L"]
        drift = data["drift"]
        events = data["events"]

        # Update metrics with final values
        self.metric_A.config(text=f"A(t): {A[-1]:.3f}")
        self.metric_alpha.config(text=f"α(t): {alpha[-1]:.3f}")
        self.metric_beta.config(text=f"β(t): {beta[-1]:.3f}")
        self.metric_L.config(text=f"L(t): {L[-1]:.3f}")
        self.metric_drift.config(text=f"Drift: {drift[-1]:.3f}")

        # Log events
        if events:
            self.console.insert(tk.END, "\nFrame Boundary Events:\n")
            for t, ev in events:
                self.console.insert(tk.END, f"  t={t:.3f}: {ev}\n")
        else:
            self.console.insert(tk.END, "\nNo boundary events detected.\n")

        self.console.insert(tk.END, "\nSimulation complete.\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = AwarenessGUI(root)
    root.mainloop()