"""Layered top-down architecture diagram for the JUTI paper (legible variant).

Each stage is a full-width band -> Data -> Predict -> Explain -> Prescribe ->
Naturalize -> Narrative, with a colored stage label (left), detailed sub-steps
(center), and an output/metric chip (right). More horizontal room => larger,
print-legible text. 300 dpi -> outputs/pipeline_overview.png
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(6.6, 8.0))
ax.set_xlim(0, 100)
ax.set_ylim(0, 121)
ax.axis("off")

EDGE = "#333333"
COL   = {"p": "#4C78A8", "e": "#F58518", "r": "#54A24B", "n": "#B279A2"}
LIGHT = {"p": "#DCE6F1", "e": "#FCE3CC", "r": "#DAEDD3", "n": "#ECDDE8"}
C_IO  = "#5A5A5A"

LX, LW = 3.0, 20.0      # label box
BX, BW = 25.0, 46.0     # body box
MX, MW = 73.0, 24.0     # metric chip

def rbox(x, y, w, h, fc, ec=EDGE, lw=1.0, z=2, rnd=1.0):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                 boxstyle=f"round,pad=0.2,rounding_size={rnd}",
                 linewidth=lw, edgecolor=ec, facecolor=fc, zorder=z))

def band(y0, h, key, label, bullets, metric):
    c, lt = COL[key], LIGHT[key]
    yc = y0 + h/2
    rbox(LX, y0, LW, h, c, ec=c, z=3)
    ax.text(LX + LW/2, yc, label, ha="center", va="center", fontsize=9.5,
            fontweight="bold", color="white", zorder=4, linespacing=1.1)
    rbox(BX, y0, BW, h, "white", ec=c, lw=1.3, z=2)
    yb = y0 + h - 2.2
    for b in bullets:
        ax.text(BX + 1.6, yb, b, ha="left", va="top", fontsize=6.6, color="#222",
                zorder=4, linespacing=1.16)
        yb -= 2.85 * (b.count("\n") + 1) + 0.6
    rbox(MX, y0, MW, h, lt, ec=c, lw=1.0, z=2)
    ax.text(MX + MW/2, yc, metric, ha="center", va="center", fontsize=6.7,
            fontweight="bold", color="#1a1a1a", zorder=4, linespacing=1.2)

def varrow(y_top, y_bot, color=EDGE, lw=1.8, ms=15):
    ax.add_patch(FancyArrowPatch((50, y_top), (50, y_bot), arrowstyle="-|>",
                 mutation_scale=ms, linewidth=lw, color=color, zorder=1))

# ---- DATA band ----
DY, DH = 110, 8.5
rbox(LX, DY, LW, DH, C_IO, ec=C_IO, z=3)
ax.text(LX + LW/2, DY + DH/2, "DATA &\nPRE-\nPROCESS", ha="center", va="center",
        fontsize=8.0, fontweight="bold", color="white", zorder=4, linespacing=1.1)
rbox(BX, DY, BW + MW - (BX - BX) + (MX + MW - (BX + BW)), DH, "white", ec=C_IO, lw=1.2, z=2)
ax.text(BX + 1.8, DY + DH - 1.8,
        "• 100,000 synthetic samples × 32 features · target stress_score (1–10)\n"
        "• Drop 4 leakage features · Ver. A (raw categorical → CatBoost) /\n"
        "  Ver. B (ordinal + StandardScaler → RF, TabNet)\n"
        "• Split 70 / 15 / 15, stratified by stress_score deciles",
        ha="left", va="top", fontsize=6.8, color="#222", zorder=4, linespacing=1.2)

# ---- stage bands ----
band(90, 15, "p", "1\nPREDICT",
     ["• CatBoost — 1000 iters, depth 6, lr 0.05, early-stop 50",
      "• Random Forest — 300 trees, min_samples_leaf 5",
      "• TabNet — ≤200 epochs, batch 1024, patience 20",
      "• Best model by test R²; 5-fold CV (seed 42)"],
     "Best: CatBoost\nR² 0.650\nRMSE 0.952\nMAE 0.758")

band(71, 15, "e", "2\nEXPLAIN",
     ["• SHAP TreeExplainer on 2000-sample test subset",
      "• Global: mean |SHAP| feature-importance ranking",
      "• Local: per-instance waterfall plots",
      "• Domain-validity sign-check vs sleep-medicine priors"],
     "Top feature\nr = −0.996\n(sleep_quality\n_score)")

band(46, 21, "r", "3\nPRE-\nSCRIBE",
     ["• DiCE — genetic algorithm, regressor mode",
      "• Feature taxonomy: behavior = vary;\n  outcome / immutable = locked",
      "• permitted_range (alcohol=0; sleep ∈[4,10]h;\n  steps ∈[1k,15k])",
      "• Cascade retry targets −0.30 / −0.15 / −0.05",
      "• 5 CF metrics: validity, proximity, sparsity,\n  diversity, plausibility"],
     "62.5% valid\nplausibility\n100%")

band(21, 21, "n", "4\nNATURAL-\nIZE",
     ["• GPT-4o-mini — temperature 0.3, JSON-object mode",
      "• System prompt: sleep/stress counselor;\n  no diagnosis / drug / alcohol promotion",
      "• Output 5 JSON fields: summary, drivers,\n  recommendations, encouragement, disclaimer",
      "• 3-layer post-validation:\n  safety regex · faithfulness · structural",
      "• On failure → retry ≤ 3, then dummy fallback"],
     "All 3 case\nstudies pass\nvalidation")

# ---- OUTPUT band ----
OY, OH = 6, 10
rbox(LX, OY, (MX + MW) - LX, OH, C_IO, ec=C_IO, z=3)
ax.text((LX + MX + MW)/2, OY + OH/2,
        "NARRATIVE  RECOMMENDATION\n"
        "empathetic · actionable · causally-valid  ·  Bahasa Indonesia, for non-expert end users",
        ha="center", va="center", fontsize=7.4, fontweight="bold", color="white",
        zorder=4, linespacing=1.3)

# ---- vertical flow arrows ----
varrow(DY - 0.3, 105 + 0.3)        # data -> S1
varrow(90 - 0.3, 86 + 0.3)         # S1 -> S2
varrow(71 - 0.3, 67 + 0.3)         # S2 -> S3
varrow(46 - 0.3, 42 + 0.3)         # S3 -> S4
varrow(21 - 0.3, OY + OH + 0.3)    # S4 -> output

# ---- group brackets on far left ----
ax.text(1.0, (90 + 71 + 15)/2, "EXPLAINABLE  ML", rotation=90, ha="center",
        va="center", fontsize=6.4, color="#777", fontweight="bold")
ax.text(1.0, (46 + 21 + 21)/2, "PRESCRIPTIVE + GENAI", rotation=90, ha="center",
        va="center", fontsize=6.4, color="#777", fontweight="bold")

plt.tight_layout(pad=0.3)
out = "outputs/pipeline_overview.png"
plt.savefig(out, dpi=300, bbox_inches="tight", facecolor="white")
print("SAVED", out)
