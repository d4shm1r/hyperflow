import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import streamlit as st

def flow(z, F, x, y):
    u = x*y - x - y
    L = np.log(x) + np.log(y) - np.log(x + y)
    L_star = L / (1 + L)
    t = z - 1
    remaining = (x*y - F[0]) / (2 - z + 1e-10)
    shape = 1 + 2 * np.sin(np.pi * t)
    dF = remaining * shape * (1 + L_star) / (1 + abs(u)/(x*y))
    return [dF]

st.title("Hyperflow")
st.markdown("Smooth interpolation between **addition** and **multiplication**.")

x = st.slider("x", min_value=2, max_value=20, value=3)
y = st.slider("y", min_value=2, max_value=20, value=4)

F0 = [x + y]
sol = solve_ivp(flow, [1, 2], F0, args=(x, y),
                dense_output=True, max_step=0.001,
                rtol=1e-6, atol=1e-8)

z_vals = np.linspace(1, 2, 200)
F_vals = sol.sol(z_vals)[0]

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(z_vals, F_vals, color='royalblue', linewidth=2.5, label='Hyperflow F(z)')
ax.axhline(y=x+y, color='gray', linestyle='--', label=f'Addition = {x+y}')
ax.axhline(y=x*y, color='black', linestyle='--', label=f'Multiplication = {x*y}')
ax.set_xlabel('z  (1 = addition, 2 = multiplication)')
ax.set_ylabel('F(x, y, z)')
ax.set_title(f'Hyperflow: x={x}, y={y}')
ax.legend()
ax.grid(True)
st.pyplot(fig)

col1, col2, col3 = st.columns(3)
col1.metric("Addition", f"{x+y}")
col2.metric("Hyperflow at z=1.5", f"{sol.sol([1.5])[0][0]:.2f}")
col3.metric("Multiplication", f"{x*y}")