# ============================================================
# ETAPA 4 — EFECTO DEL INTERCAMBIO DE REPETIDAS
# N=100, S=7, R=10,000, Semilla=2026
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

# ── Parámetros ──────────────────────────────────────────────
N      = 100
S      = 7
R      = 10_000
SEED   = 2026
KS     = [1, 2, 5, 10]
MS     = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70]
PRECIO = 9.50
COLORES = {1:"#1D9E75", 2:"#378ADD", 5:"#BA7517", 10:"#D85A30", "base":"#888780"}

# ============================================================
# FUNCIONES
# ============================================================

def sim_completar(K, rng):
    """Simula hasta completar el álbum con regla de canje K."""
    tiene     = np.zeros(N, dtype=bool)
    distintas = 0
    repetidas = 0
    sobres    = 0
    while distintas < N:
        sobres += 1
        for e in rng.integers(0, N, size=S):
            if not tiene[e]:
                tiene[e] = True
                distintas += 1
            else:
                repetidas += 1
        if K < N:
            while repetidas >= K and distintas < N:
                repetidas -= K
                falt = np.where(~tiene)[0]
                idx  = rng.integers(0, len(falt))
                tiene[falt[idx]] = True
                distintas += 1
    return sobres


def prob_M_sobres(K, M, rng):
    """Probabilidad de completar el álbum con exactamente M sobres y canje K."""
    tiene     = np.zeros((R, N), dtype=bool)
    repetidas = np.zeros(R, dtype=np.int32)
    distintas = np.zeros(R, dtype=np.int32)
    idx_r     = np.arange(R)

    for _ in range(M):
        est = rng.integers(0, N, size=(R, S))
        for s in range(S):
            e        = est[:, s]
            es_nueva = ~tiene[idx_r, e]
            tiene[idx_r, e] = True
            distintas += es_nueva.astype(np.int32)
            repetidas += (~es_nueva).astype(np.int32)
        if K < N:
            for i in range(R):
                while repetidas[i] >= K and distintas[i] < N:
                    repetidas[i] -= K
                    falt = np.where(~tiene[i])[0]
                    j    = rng.integers(0, len(falt))
                    tiene[i, falt[j]] = True
                    distintas[i] += 1

    return float((distintas == N).sum()) / R

# ============================================================
# PARTE A — Sobres hasta completar
# ============================================================

print("=" * 58)
print("PARTE A — Sobres hasta completar el álbum")
print("=" * 58)

rng       = np.random.default_rng(SEED)
base_arr  = np.array([sim_completar(999999, rng) for _ in range(R)])
media_base = base_arr.mean()
std_base   = base_arr.std()
print(f"  Sin intercambio : media={media_base:.2f}  std={std_base:.2f}")

sims_A = {}
for K in KS:
    rng      = np.random.default_rng(SEED)
    arr      = np.array([sim_completar(K, rng) for _ in range(R)])
    sims_A[K] = arr
    media    = arr.mean()
    std      = arr.std()
    reduccion = (media_base - media) / media_base * 100
    print(f"  K={K:2d}            : media={media:.2f}  std={std:.2f}  "
          f"reducción={reduccion:.1f}%")

# ── Histogramas: 2 paneles para evitar aplastamiento ────────
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

ax1.hist(base_arr, bins=50, alpha=0.5, color=COLORES["base"],
         label=f"Sin intercambio  μ={media_base:.1f}", density=True)
ax1.hist(sims_A[10], bins=30, alpha=0.6, color=COLORES[10],
         label=f"K=10  μ={sims_A[10].mean():.1f}", density=True)
ax1.set_xlabel("Número de sobres")
ax1.set_ylabel("Densidad")
ax1.set_title("Sin intercambio vs K=10")
ax1.legend()

for K in [5, 2, 1]:
    ax2.hist(sims_A[K], bins=25, alpha=0.55, color=COLORES[K],
             label=f"K={K}  μ={sims_A[K].mean():.1f}  σ={sims_A[K].std():.1f}",
             density=True)
ax2.hist(sims_A[10], bins=30, alpha=0.35, color=COLORES[10],
         label=f"K=10  μ={sims_A[10].mean():.1f}", density=True)
ax2.set_xlabel("Número de sobres")
ax2.set_ylabel("Densidad")
ax2.set_title("Detalle por K (con intercambio)")
ax2.legend()

fig.suptitle("Distribución de sobres hasta completar el álbum — por K", fontsize=13)
plt.tight_layout()
plt.savefig("etapa4_histogramas.png", dpi=150)
plt.show()

# ============================================================
# PARTE B — P(completar) vs M para cada K
# ============================================================

print("\n" + "=" * 58)
print("PARTE B — P(completar álbum) vs M sobres")
print("=" * 58)

probs_B = {}

rng = np.random.default_rng(SEED)
probs_B["base"] = [prob_M_sobres(999999, M, rng) for M in MS]
print(f"  Base : {[round(p,3) for p in probs_B['base']]}")

for K in KS:
    rng = np.random.default_rng(SEED)
    probs_B[K] = [prob_M_sobres(K, M, rng) for M in MS]
    print(f"  K={K:2d} : {[round(p,3) for p in probs_B[K]]}")

# ── Gráfica de líneas ────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(MS, probs_B["base"], color=COLORES["base"], linewidth=2,
        linestyle="--", marker="o", ms=5, label="Sin intercambio")
for K in KS:
    ax.plot(MS, probs_B[K], color=COLORES[K], linewidth=2,
            marker="o", ms=5, label=f"K={K}")
for u, lbl in [(0.50,"50%"), (0.75,"75%"), (0.90,"90%")]:
    ax.axhline(u, color="gray", linestyle=":", linewidth=1, alpha=0.5)
    ax.text(MS[-1]+0.4, u, lbl, fontsize=9, color="gray", va="center")
ax.set_xlabel("Número de sobres (M)")
ax.set_ylabel("P(completar álbum)")
ax.set_title("Probabilidad de completar el álbum vs. sobres comprados — por K")
ax.yaxis.set_major_formatter(PercentFormatter(1.0))
ax.set_xlim(MS[0]-1, MS[-1]+3)
ax.legend()
plt.tight_layout()
plt.savefig("etapa4_prob_vs_M.png", dpi=150)
plt.show()

# ── Sobres necesarios para 50%, 75%, 90% ────────────────────
print("\n" + "=" * 58)
print("Sobres necesarios para P ≥ 50%, 75%, 90%")
print("=" * 58)

def M_umbral(probs, u):
    for i, p in enumerate(probs):
        if p >= u:
            return MS[i]
    return f">{MS[-1]}"

claves = ["base"] + KS
header = f"  {'Umbral':<8}" + "".join(
    [f"  {'Sin intercambio' if k=='base' else f'K={k}':>16}" for k in claves])
print(header)
for u in [0.50, 0.75, 0.90]:
    row = f"  P≥{int(u*100)}%   "
    for k in claves:
        row += f"  {str(M_umbral(probs_B[k], u)):>16}"
    print(row)

# ============================================================
# PREGUNTAS DE ANÁLISIS
# ============================================================

print("\n" + "=" * 58)
print("PREGUNTAS DE ANÁLISIS")
print("=" * 58)

# P1
medias = {"base": media_base}
for K in KS:
    medias[K] = sims_A[K].mean()
print("\nP1 — Media de sobres por K:")
for K in KS:
    print(f"  K={K:2d}: {medias[K]:.2f}  (reducción {(media_base-medias[K])/media_base*100:.1f}%)")
diffs = [medias[KS[i]] - medias[KS[i+1]] for i in range(len(KS)-1)]
print(f"  Diferencias entre K consecutivos: {[round(float(d),2) for d in diffs]}")
print("  Conclusión: la relación NO es lineal (mejoras decrecientes al bajar K).")

# P2
ahorro_s = media_base - medias[2]
ahorro_Q = ahorro_s * PRECIO
print(f"\nP2 — Ahorro con K=2 vs sin intercambio:")
print(f"  Sobres ahorrados en promedio : {ahorro_s:.2f}")
print(f"  Ahorro en quetzales          : Q{ahorro_Q:.2f}")

# P3
idx45 = MS.index(45)
p10 = probs_B[10][idx45]
p5  = probs_B[5][idx45]
p1  = probs_B[1][idx45]
print(f"\nP3 — M=45 sobres:")
print(f"  K=10: {p10:.4f}")
print(f"  K=5 : {p5:.4f}  →  diferencia K=10 a K=5 : +{p5-p10:.4f}")
print(f"  K=1 : {p1:.4f}  →  diferencia K=5  a K=1 : +{p1-p5:.4f}")

# P4
print(f"\nP4 — Punto de rendimiento decreciente:")
print(f"  Entre K=2 y K=1 la mejora es pequeña (~5 sobres).")
print(f"  A partir de K≤2 mejorar la tasa de intercambio")
print(f"  produce muy poco beneficio adicional.")
print(f"  Razón: con K=1 cada repetida se canjea de inmediato,")
print(f"  que es el límite físico del mecanismo.")

# P5
print(f"\nP5 — Costo efectivo por estampa nueva vía canje:")
for K in KS:
    costo = (K * PRECIO) / S
    print(f"  K={K:2d}: Q{costo:.4f} por estampa nueva")
print(f"  K=1 es la más rentable (Q{1*PRECIO/S:.4f} por estampa nueva).")

print("\n" + "=" * 58)
print("FIN ETAPA 4")
print("=" * 58)