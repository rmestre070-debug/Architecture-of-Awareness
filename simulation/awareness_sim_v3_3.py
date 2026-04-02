import numpy as np
import matplotlib.pyplot as plt

def simulate_awareness(
    T=100.0,
    dt=0.001,
    dim=10,
    k_id_frac=1/3,
    theta=1.0,
    mu=1.0,
    sigma=0.2,
    gamma=0.5,
    ac_drift_scale=0.1,
    cc_push_scale=0.1,
    seed=None,
):
    """
    Simulate awareness dynamics under the v3.3 architecture.

    Returns:
        t: time array
        A_trace: awareness index over time (beta - alpha)
        L_trace: load over time
        alpha_trace: identification metric over time
        beta_trace: observation metric over time
    """
    if seed is not None:
        np.random.seed(seed)

    steps = int(T / dt)
    t = np.linspace(0, T, steps)

    # Identity subspace mask
    k_id = max(1, int(dim * k_id_frac))
    I_mask = np.zeros(dim)
    I_mask[:k_id] = 1.0

    # Initialize frame and load
    F = np.random.randn(dim)
    L = mu

    A_trace = np.zeros(steps)
    L_trace = np.zeros(steps)
    alpha_trace = np.zeros(steps)
    beta_trace = np.zeros(steps)

    for i in range(steps):
        # Normalize F to avoid blow-up
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

        # Store traces
        A_trace[i] = A
        L_trace[i] = L
        alpha_trace[i] = alpha
        beta_trace[i] = beta

        # Load update (Ornstein–Uhlenbeck)
        dL = theta * (mu - L) * dt + sigma * np.sqrt(dt) * np.random.randn()
        L += dL

        # AC: random drift in all dimensions
        dF_ac = ac_drift_scale * np.random.randn(dim)

        # CC: push away from identity when awareness is positive,
        # push toward identity when awareness is negative
        # sign(alpha - beta) > 0 => identification dominates
        dF_cc = -cc_push_scale * np.sign(alpha - beta) * F_I

        # Load-driven pull into identity subspace
        dF_load = -gamma * L * F_I

        # Total frame update
        dF = (dF_ac + dF_cc + dF_load) * dt
        F = F + dF

    return t, A_trace, L_trace, alpha_trace, beta_trace


if __name__ == "__main__":
    # Run a simulation
    T = 60.0
    dt = 0.001

    t, A, L, alpha, beta = simulate_awareness(
        T=T,
        dt=dt,
        dim=12,
        k_id_frac=1/3,
        theta=1.0,
        mu=1.0,
        sigma=0.25,
        gamma=0.7,
        ac_drift_scale=0.08,
        cc_push_scale=0.12,
        seed=42,
    )

    # Plot awareness index and load
    fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

    axes[0].plot(t, A, label="Awareness index A(t) = β - α")
    axes[0].axhline(0.0, color="k", linestyle="--", linewidth=0.8)
    axes[0].set_ylabel("A(t)")
    axes[0].set_title("Awareness Dynamics (v3.3)")
    axes[0].legend(loc="best")

    axes[1].plot(t, alpha, label="α(t) = identification", color="tab:red")
    axes[1].plot(t, beta, label="β(t) = observation", color="tab:blue", alpha=0.8)
    axes[1].set_ylabel("α, β")
    axes[1].legend(loc="best")

    axes[2].plot(t, L, label="Load L(t)", color="tab:purple")
    axes[2].set_ylabel("L(t)")
    axes[2].set_xlabel("Time")
    axes[2].legend(loc="best")

    plt.tight_layout()
    plt.show()
