# Arithmeflow

Smooth interpolation between addition and multiplication using a single parameter `z`.

## Install

```bash
pip install arithmeflow
```

## Usage

```python
import arithmeflow

# Single value
result = arithmeflow.compute(3, 4, 1.5)
print(result)  # ~10.97

# Full curve
points = arithmeflow.curve(3, 4)
for z, val in points:
    print(f"z={z:.2f}  F={val:.4f}")
```

## What it does

- `z = 1.0` → returns `x + y` (addition)
- `z = 2.0` → returns `x * y` (multiplication)
- `z = 1.5` → smooth midpoint between the two

Based on an original ODE framework with proven boundary conditions.

## Links

- 🎮 Live demo: https://hyperflow-um4jhq9jvgeanzxw8wtufq.streamlit.app
- 📦 PyPI: https://pypi.org/project/arithmeflow
- 🔌 API: https://hyperflow-api.onrender.com
- 🛒 Buy: https://dashmir7.gumroad.com/l/zxtaqe
- 📡 RapidAPI: https://rapidapi.com/dashmirmejdii/api/hyperflow

## Author

Dashmir Mejdi — mathematician and AI engineer
