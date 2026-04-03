import numpy as np

# ---------------------------------------------------------
# v3.4 Awareness Dynamics Engine
# Cognitive-Architecture Edition
# ---------------------------------------------------------

def cosine_similarity(a, b):
    denom = (np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0:
        return 0.0
    return np.dot(a, b) / denom


def detect_frame_boundary(prev_A, A, prev_alpha, alpha, prev_beta, beta, threshold=0.15):
    events = []

    if np.sign(prev_A) != np.sign(A):
        events.append("A_sign_flip")

    if abs(alpha - prev_alpha) > threshold:
        events.append("alpha_jump")

    if abs(beta - prev_beta) > threshold:
        events.append("beta_jump")

    return events


def simulate_awareness(
    T=30.0,
    dt=0.002,
    dim=12,
    k_id_frac=1/3,
    theta=1.0,
    mu=1.0,
    sigma=0.25,
    gamma=0.7,
    ac_drift_scale=0.08,
    cc_push_scale=0.12,
    drift_threshold=0.25,
    seed=None,
):
    if seed is not None:
        np.random.seed(seed)

    steps = int(T / dt)

    # Identity mask
    k_id = max(1, int(dim * k_id_frac))
    I_mask = np.zeros(dim)
    I_mask[:k_id] = 1.0

    # Initial state
    F = np.random.randn(dim)
    L = 0.0
    A_trace = np.zeros(steps)
    L_trace = np.zeros(steps)
    alpha_trace = np.zeros(steps)
    beta_trace = np.zeros(steps)
    drift_trace = np.zeros(steps)
    boundary_events = []

    prev_F = F.copy()
    prev_A = 0
    prev_alpha = 0
    prev_beta = 0

    for i in range(steps):
        # Normalize frame
        normF = np.linalg.norm(F)
        if normF == 0:
            F = np.random.randn(dim)
            normF = np.linalg.norm(F)
        F = F / normF

        # Projections
        F_I = F * I_mask
        F_perp = F * (1.0 - I_mask)

        alpha = np.linalg.norm(F_I)
        beta = np.linalg.norm(F_perp)
        A = beta - alpha

        # Store
        A_trace[i] = A
        L_trace[i] = L
        alpha_trace[i] = alpha
        beta_trace[i] = beta

        # Drift
        sim = cosine_similarity(F, prev_F)
        drift = 1 - sim
        drift_trace[i] = drift

        # Boundary detection
        events = detect_frame_boundary(prev_A, A, prev_alpha, alpha, prev_beta, beta)
        if events:
            boundary_events.append((i * dt, events))

        # Load update
        dL = theta * (mu - L) * dt + sigma * np.sqrt(dt) * np.random.randn()
        L += dL

        # AC drift
        dF_ac = ac_drift_scale * np.random.randn(dim)

        # CC push
        dF_cc = -cc_push_scale * np.sign(alpha - beta) * F_I

        # Load pull
        dF_load = -gamma * L * F_I

        # ---------------------------------------------------------
        # Recursive Stability Layer (RSL)
        # ---------------------------------------------------------
        if drift > drift_threshold:
            dF_ac *= 0.5
            dF_cc *= 0.5

        # Total update
        dF = (dF_ac + dF_cc + dF_load) * dt
        F = F + dF

        # Update previous
        prev_F = F.copy()
        prev_A = A
        prev_alpha = alpha
        prev_beta = beta

    return {
        "A": A_trace,
        "L": L_trace,
        "alpha": alpha_trace,
        "beta": beta_trace,
        "drift": drift_trace,
        "events": boundary_events,
        "dt": dt,
        "T": T,
    }        header.pack(pady=(0, 20))

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
