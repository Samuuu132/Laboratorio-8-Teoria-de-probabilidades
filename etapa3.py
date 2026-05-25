# ============================================================
# ETAPA 3 - SIMULACIÓN DE ÁLBUM DE ESTAMPAS CON PRESUPUESTO
# ============================================================
# Parámetros: N=100, S=7, precio=Q9.50, presupuesto=Q1000
# Simulaciones: R=10,000 | Semilla: 2026
# ============================================================

import numpy as np
import matplotlib.pyplot as plt

# ── Parámetros ──────────────────────────────────────────────
N             = 100
S             = 7
PRECIO_SOBRE  = 9.50
PRESUPUESTO   = 1000
R             = 10_000
SEMILLA       = 2026
SOBRES_CAJA   = 104
COSTO_CAJA    = 975.00

np.random.seed(SEMILLA)

# ============================================================
# SIMULACIÓN PRINCIPAL — sobres sueltos hasta agotar presupuesto
# ============================================================

resultados_completo  = []
resultados_sobres    = []
resultados_distintas = []

for _ in range(R):
    coleccion = np.zeros(N, dtype=bool)
    gasto     = 0.0
    sobres    = 0

    while (gasto + PRECIO_SOBRE <= PRESUPUESTO) and (coleccion.sum() < N):
        estampas          = np.random.randint(0, N, size=S)
        coleccion[estampas] = True
        gasto  += PRECIO_SOBRE
        sobres += 1

    completo = 1 if coleccion.sum() == N else 0
    resultados_completo.append(completo)
    resultados_sobres.append(sobres)
    resultados_distintas.append(int(coleccion.sum()))

resultados_completo  = np.array(resultados_completo)
resultados_sobres    = np.array(resultados_sobres)
resultados_distintas = np.array(resultados_distintas)

prob_completar   = resultados_completo.mean()
esperado_sobres  = resultados_sobres.mean()
no_exitosos_mask = resultados_completo == 0
esperado_distintas_fallo = resultados_distintas[no_exitosos_mask].mean()

print("=" * 50)
print("RESULTADOS DE LA SIMULACIÓN")
print("=" * 50)
print(f"Probabilidad de completar el álbum:              {prob_completar:.4f}")
print(f"Número esperado de sobres comprados:             {esperado_sobres:.2f}")
print(f"Esperado estampas distintas (casos no exitosos): {esperado_distintas_fallo:.2f}")

# ── Visualización ────────────────────────────────────────────
completados     = resultados_completo.sum()
no_completados  = R - completados
categorias      = ["Completó", "No completó"]
valores         = [completados / R, no_completados / R]

plt.figure(figsize=(7, 5))
bars = plt.bar(categorias, valores, color=["#1D9E75", "#D85A30"], width=0.5)
plt.ylabel("Proporción")
plt.title("Proporción de álbumes completados (sobres sueltos, Q1000)")
for bar, v in zip(bars, valores):
    plt.text(bar.get_x() + bar.get_width() / 2, v + 0.01,
             f"{v:.3f}", ha="center", fontweight="bold")
plt.ylim(0, 1.1)
plt.tight_layout()
plt.savefig("etapa3_barras.png", dpi=150)
plt.show()

# ============================================================
# PREGUNTA 1
# ============================================================

max_sobres              = int(PRESUPUESTO // PRECIO_SOBRE)
estampas_teoricas       = max_sobres * S
sobres_minimo_teorico   = int(np.ceil(N / S))

print("\n" + "=" * 50)
print("PREGUNTA 1")
print("=" * 50)
print(f"Máximo sobres con Q{PRESUPUESTO}:                {max_sobres}")
print(f"Estampas posibles sin repetidos ({max_sobres}×{S}):    {estampas_teoricas}")
print(f"Mínimo teórico de sobres sin repetidos:          {sobres_minimo_teorico}")
if estampas_teoricas >= N:
    print("Sí alcanza en teoría si NO hubiera repetidos.")
else:
    print("No alcanza ni siquiera en teoría.")

# ============================================================
# PREGUNTA 2 — Caja de 104 sobres (Q975)
# ============================================================

resultados_caja = []

for _ in range(R):
    coleccion = np.zeros(N, dtype=bool)
    for _ in range(SOBRES_CAJA):
        coleccion[np.random.randint(0, N, size=S)] = True
    resultados_caja.append(1 if coleccion.sum() == N else 0)

prob_caja = np.mean(resultados_caja)

print("\n" + "=" * 50)
print("PREGUNTA 2 — CAJA DE 104 SOBRES (Q975)")
print("=" * 50)
print(f"Probabilidad completar con caja:     {prob_caja:.4f}")
print(f"Probabilidad comprando sueltos:      {prob_completar:.4f}")
print(f"Diferencia:                          {prob_caja - prob_completar:+.4f}")
if prob_caja > prob_completar:
    print("Conviene la caja.")
else:
    print("No conviene la caja.")

# ============================================================
# PREGUNTA 3 — Estrategia mixta: caja + sobres sueltos
# ============================================================

dinero_restante = PRESUPUESTO - COSTO_CAJA
sobres_extra    = int(dinero_restante // PRECIO_SOBRE)
costo_total_mixta = COSTO_CAJA + sobres_extra * PRECIO_SOBRE

print("\n" + "=" * 50)
print("PREGUNTA 3 — ESTRATEGIA MIXTA")
print("=" * 50)
print(f"Costo de la caja:                    Q{COSTO_CAJA:.2f}")
print(f"Dinero restante tras la caja:        Q{dinero_restante:.2f}")
print(f"Sobres extra posibles:               {sobres_extra}")
print(f"Costo total (caja + {sobres_extra} sueltos):     Q{costo_total_mixta:.2f}")
print(f"Presupuesto no gastado:              Q{PRESUPUESTO - costo_total_mixta:.2f}")

resultados_mixta = []

for _ in range(R):
    coleccion = np.zeros(N, dtype=bool)
    # Comprar la caja
    for _ in range(SOBRES_CAJA):
        coleccion[np.random.randint(0, N, size=S)] = True
    # Comprar sobres extra con el presupuesto restante
    for _ in range(sobres_extra):
        coleccion[np.random.randint(0, N, size=S)] = True
    resultados_mixta.append(1 if coleccion.sum() == N else 0)

prob_mixta = np.mean(resultados_mixta)

print(f"\nProbabilidad estrategia mixta:       {prob_mixta:.4f}")

# ── Comparación final ────────────────────────────────────────
print("\n" + "=" * 50)
print("COMPARACIÓN FINAL")
print("=" * 50)
print(f"A) Sobres sueltos (Q{PRESUPUESTO}):       P = {prob_completar:.4f}  |  gasto prom. Q{esperado_sobres * PRECIO_SOBRE:.2f}")
print(f"B) Caja 104 sobres (Q{COSTO_CAJA:.0f}):      P = {prob_caja:.4f}  |  gasto fijo  Q{COSTO_CAJA:.2f}")
print(f"C) Caja + {sobres_extra} sueltos (Q{costo_total_mixta:.0f}):    P = {prob_mixta:.4f}  |  gasto fijo  Q{costo_total_mixta:.2f}")

mejor = max([("A: Sobres sueltos", prob_completar),
             ("B: Caja", prob_caja),
             ("C: Caja + sueltos", prob_mixta)],
            key=lambda x: x[1])
print(f"\nEstrategia recomendada: {mejor[0]} (P = {mejor[1]:.4f})")