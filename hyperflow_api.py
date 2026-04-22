from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from scipy.integrate import solve_ivp

app = FastAPI(
    title="Hyperflow API",
    description="Smooth interpolation between addition and multiplication.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def flow(z, F, x, y):
    u = x*y - x - y
    L = np.log(x) + np.log(y) - np.log(x + y)
    L_star = L / (1 + L)
    t = z - 1
    remaining = (x*y - F[0]) / (2 - z + 1e-10)
    shape = 1 + 2 * np.sin(np.pi * t)
    dF = remaining * shape * (1 + L_star) / (1 + abs(u)/(x*y))
    return [dF]

def compute_hyperflow(x: float, y: float, z: float) -> float:
    z = max(1.0, min(2.0, z))
    F0 = [x + y]
    sol = solve_ivp(flow, [1, z], F0, args=(x, y),
                    dense_output=True, max_step=0.001,
                    rtol=1e-6, atol=1e-8)
    return float(sol.sol([z])[0][0])

@app.get("/")
def root():
    return {
        "name": "Arithmeflow API",
        "usage": "GET /compute?x=3&y=4&z=1.5",
        "demo": "https://hyperflow-um4jhq9jvgeanzxw8wtufq.streamlit.app/",
	"pypi": "pip install arithmeflow",
        "github": "https://github.com/d4shm1r/hyperflow",
        "buy": "https://dashmir7.gumroad.com/l/zxtaqe"
    }

@app.get("/compute")
def compute(
    x: float = Query(..., gt=1, description="First operand (must be > 1)"),
    y: float = Query(..., gt=1, description="Second operand (must be > 1)"),
    z: float = Query(..., ge=1.0, le=2.0, description="Operation parameter (1=addition, 2=multiplication)")
):
    result = compute_hyperflow(x, y, z)
    return {
        "x": x,
        "y": y,
        "z": z,
        "result": result,
        "addition": x + y,
        "multiplication": x * y
    }

@app.get("/curve")
def curve(
    x: float = Query(..., gt=1),
    y: float = Query(..., gt=1),
    steps: int = Query(20, ge=5, le=100)
):
    z_vals = np.linspace(1, 2, steps)
    points = [{"z": round(float(z), 4), "value": compute_hyperflow(x, y, float(z))} for z in z_vals]
    return {
        "x": x,
        "y": y,
        "addition": x + y,
        "multiplication": x * y,
        "curve": points
    }
