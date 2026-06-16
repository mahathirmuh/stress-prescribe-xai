"""Detailed four-stage pipeline / architecture diagram for the JUTI paper.

Horizontal flow: DATA -> Predict -> Explain -> Prescribe -> Naturalize -> Narrative,
with per-stage sub-steps + real parameters, a feature-taxonomy callout under the
Prescribe stage, and a validation-retry loop under the Naturalize stage.
Designed at ~final embed size so on-screen == printed. 300 dpi.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# design at final embed size (~6.5in wide) so text sizes are WYSIWYG
fig, ax = plt.subplots(figsize=(6.7, 4.5))
ax.set_xlim(0, 100)
ax.set_ylim(0, 67)
ax.axis("off")

EDGE = "#333333"
COL   = {"p": "#4C78A8", "e": "#F58518", "r": "#54A24B", "n": "#B279A2"}
LIGHT = {"p": "#DCE6F1", "e": "#FCE3CC", "r": "#DAEDD3", "n": "#ECDDE8"}
C_IO  = "#5A5A5A"

HEAD_T, HEAD_B = 64.5, 59.0
BODY_T, BODY_B = 59.0, 30.0
FOOT_T, FOOT_B = 30.0, 24.0
MIDY = 47.0

def rbox(x, y, w, h, fc, ec=EDGE, lw=1.0, z=2, rnd=0.8):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                 boxstyle=f"round,pad=0.15,rounding_size={rnd}",
                 linewidth=lw, edgecolor=ec, facecolor=fc, zorder=z))

def stage(x, w, key, header, bullets, footer):
    c, lt = COL[key], LIGHT[key]
    rbox(x, HEAD_B, w, HEAD_T - HEAD_B, c, ec=c, z=3)
    ax.text(x + w/2, (HEAD_T+HEAD_B)/2, header, ha="center", va="center",
            fontsize=8.0, fontweight="bold", color="white", zorder=4)
    rbox(x, BODY_B, w, BODY_T - BODY_B, "white", ec=c, lw=1.2, z=2)
    yb = BODY_T - 1.8
    for b in bullets:
        ax.text(x + 1.1, yb, b, ha="left", va="top", fontsize=5.2,
                color="#222", zorder=4, linespacing=1.18)
        yb -= 2.55 * (b.count("\n") + 1) + 0.5
    rbox(x, FOOT_B, w, FOOT_T - FOOT_B, lt, ec=c, lw=1.0, z=2)
    ax.text(x + w/2, (FOOT_T+FOOT_B)/2, footer, ha="center", va="center",
            fontsize=5.4, fontweight="bold", color="#1a1a1a", zorder=4,
            linespacing=1.15)

# columns
DX, DW = 1.0, 11.0
W = 20.0
X = [14.0, 36.0, 58.0, 80.0]

# DATA inlet
rbox(DX, FOOT_B, DW, HEAD_T - FOOT_B, C_IO, ec=C_IO, z=3)
ax.text(DX + DW/2, HEAD_T - 1.6, "DATA &\nPREPROC.", ha="center", va="top",
        fontsize=6.2, fontweight="bold", color="white", zorder=4, linespacing=1.15)
for i, t in enumerate(["100k × 32", "− 4 leakage", "Ver A / Ver B", "70/15/15\nstratified"]):
    ax.text(DX + DW/2, 52 - i*6.6, t, ha="center", va="top", fontsize=4.5,
            color="white", zorder=4, linespacing=1.1)

stage(X[0], W, "p", "1 | PREDICT",
      ["• CatBoost (1000 iter,\n  depth 6, lr 0.05)",
       "• Random Forest (300)",
       "• TabNet (≤200 epochs)",
       "• 5-fold CV · seed 42"],
      "→ best: CatBoost\nR² 0.650 · MAE 0.758")

stage(X[1], W, "e", "2 | EXPLAIN",
      ["• SHAP TreeExplainer\n  (2000 samples)",
       "• global  mean |SHAP|",
       "• local  waterfalls",
       "• domain sign-check vs\n  sleep medicine"],
      "→ top r = −0.996\n(sleep_quality_score)")

stage(X[2], W, "r", "3 | PRESCRIBE",
      ["• DiCE genetic alg.\n  (regressor)",
       "• permitted_range\n  (alcohol=0; sleep 4–10h)",
       "• retry −.30 / −.15 / −.05",
       "• 5 CF metrics"],
      "→ 62.5% valid\nplausibility 100%")

stage(X[3], W, "n", "4 | NATURALIZE",
      ["• GPT-4o-mini\n  (T=0.3, JSON mode)",
       "• counselor prompt;\n  no Dx / drug / alcohol",
       "• 5 JSON fields",
       "• 3-layer validation"],
      "→ faithful narrative")

# feature-taxonomy callout under PRESCRIBE
ty = 18.5
ax.text(X[2] + W/2, ty + 5.2, "feature taxonomy", ha="center", va="bottom",
        fontsize=4.6, style="italic", color="#3b6b32", zorder=5)
for i, (lab, st, fc, tc) in enumerate([("behav.", "VARY", "#54A24B", "white"),
                                       ("outcome", "LOCK", "#C2C2C2", "#222"),
                                       ("immut.", "LOCK", "#C2C2C2", "#222")]):
    cw = (W - 1.5) / 3
    cx = X[2] + 0.75 + i*cw
    rbox(cx, ty, cw - 0.5, 4.6, fc, ec="#3b6b32", lw=0.7, z=6, rnd=0.4)
    ax.text(cx + (cw-0.5)/2, ty + 2.3, f"{lab}\n{st}", ha="center", va="center",
            fontsize=3.9, fontweight="bold", color=tc, zorder=7, linespacing=1.0)

# validation retry loop under NATURALIZE
ax.add_patch(FancyArrowPatch((X[3] + W - 3, ty + 4.5), (X[3] + 3, ty + 4.5),
             connectionstyle="arc3,rad=0.55", arrowstyle="-|>", mutation_scale=8,
             linewidth=1.0, color="#7A4F70", linestyle=(0, (3, 2)), zorder=6))
ax.text(X[3] + W/2, ty + 1.5, "retry ≤ 3 → dummy fallback", ha="center", va="center",
        fontsize=4.2, style="italic", color="#7A4F70", zorder=6)

# flow arrows
def arrow(x0, x1, y, lw=1.5, ms=12, color=EDGE):
    ax.add_patch(FancyArrowPatch((x0, y), (x1, y), arrowstyle="-|>",
                 mutation_scale=ms, linewidth=lw, color=color, zorder=1))
for x0, x1 in [(DX+DW, X[0]), (X[0]+W, X[1]), (X[1]+W, X[2]), (X[2]+W, X[3])]:
    arrow(x0 + 0.2, x1 - 0.2, MIDY)

# output banner
OY_T, OY_B = 12.5, 4.0
rbox(X[0], OY_B, (X[3] + W) - X[0], OY_T - OY_B, C_IO, ec=C_IO, z=3)
ax.text((X[0] + X[3] + W)/2, (OY_T+OY_B)/2,
        "NARRATIVE  RECOMMENDATION    ·    empathetic · actionable · causally-valid    ·    "
        "Bahasa Indonesia, for non-expert end users",
        ha="center", va="center", fontsize=5.4, fontweight="bold", color="white", zorder=4)
ax.add_patch(FancyArrowPatch((X[3] + W/2, FOOT_B - 0.2), (X[3] + W/2, OY_T + 0.2),
             arrowstyle="-|>", mutation_scale=11, linewidth=1.4, color=EDGE, zorder=1))

# top group labels
ax.text((X[0] + X[1] + W)/2, HEAD_T + 0.7, "EXPLAINABLE  ML", ha="center", va="bottom",
        fontsize=5.6, color="#777", fontweight="bold")
ax.text((X[2] + X[3] + W)/2, HEAD_T + 0.7, "PRESCRIPTIVE  +  GENAI", ha="center", va="bottom",
        fontsize=5.6, color="#777", fontweight="bold")

plt.tight_layout(pad=0.2)
out = "outputs/pipeline_overview.png"
plt.savefig(out, dpi=300, bbox_inches="tight", facecolor="white")
print("SAVED", out)
