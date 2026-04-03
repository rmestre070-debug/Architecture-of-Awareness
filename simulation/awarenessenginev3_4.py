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
    L
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
    }