"""Generate the four-stage pipeline / architecture diagram for the JUTI paper.

Pipeline: Sleep & Lifestyle Data -> PREDICT -> EXPLAIN -> PRESCRIBE -> NATURALIZE -> Narrative.
Grayscale-friendly for print. Saved to outputs/pipeline_overview.png at 300 dpi.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import os

os.makedirs("outputs", exist_ok=True)

fig, ax = plt.subplots(figsize=(14.5, 4.4))
ax.set_xlim(0, 110)
ax.set_ylim(0, 32)
ax.axis("off")

# ---- palette (grayscale-friendly) ----
C_IO    = "#E8E8E8"   # input/output boxes
C_STAGE = ["#4C78A8", "#F58518", "#54A24B", "#B279A2"]  # 4 stages
EDGE    = "#333333"

box_w, box_h = 15.0, 13.0
y = 11.0
# input + 4 stages, each box 15 wide with 3-wide gaps -> step of 18
xs = [2, 20, 38, 56, 74]   # input + 4 stages; output appended after stage 4

def box(x, w, h, yy, face, title, lines, title_color="white", body_color="white"):
    p = FancyBboxPatch((x, yy), w, h,
                        boxstyle="round,pad=0.3,rounding_size=1.2",
                        linewidth=1.3, edgecolor=EDGE, facecolor=face, zorder=2)
    ax.add_patch(p)
    cx = x + w / 2
    ax.text(cx, yy + h - 2.4, title, ha="center", va="top",
            fontsize=11, fontweight="bold", color=title_color, zorder=3)
    ax.text(cx, yy + h - 5.6, "\n".join(lines), ha="center", va="top",
            fontsize=8.2, color=body_color, zorder=3, linespacing=1.35)

# Input
box(xs[0], box_w, box_h, y, C_IO,
    "Sleep & Lifestyle\nData",
    ["100k synthetic samples", "32 features", "target: stress_score"],
    title_color="#222", body_color="#333")

# Stage 1 - Predict
box(xs[1], box_w, box_h, y, C_STAGE[0],
    "1 | PREDICT",
    ["CatBoost / RandomForest", "/ TabNet regressors", "best: CatBoost", "R² = 0.650"])

# Stage 2 - Explain
box(xs[2], box_w, box_h, y, C_STAGE[1],
    "2 | EXPLAIN",
    ["SHAP global + local", "domain-validity", "sign check", "(r = -0.996 top feat.)"])

# Stage 3 - Prescribe
box(xs[3], box_w, box_h, y, C_STAGE[2],
    "3 | PRESCRIBE",
    ["DiCE counterfactuals", "behavior-only (causal)", "outcomes locked", "valid 62.5%, plaus. 100%"])

# Stage 4 - Naturalize
box(xs[4], box_w, box_h, y, C_STAGE[3],
    "4 | NATURALIZE",
    ["GPT-4o-mini", "JSON output", "safety filter +", "faithfulness check"])

# Output
out_x = xs[4] + box_w + 3.0
box(out_x, 16.0, box_h, y, C_IO,
    "Narrative\nRecommendation",
    ["empathetic, actionable", "Bahasa Indonesia", "for non-expert users"],
    title_color="#222", body_color="#333")

# ---- arrows between boxes ----
def arrow(x0, x1, yy):
    a = FancyArrowPatch((x0, yy), (x1, yy),
                        arrowstyle="-|>", mutation_scale=16,
                        linewidth=1.6, color=EDGE, zorder=1)
    ax.add_patch(a)

ymid = y + box_h / 2
gaps = [(xs[0]+box_w, xs[1]), (xs[1]+box_w, xs[2]),
        (xs[2]+box_w, xs[3]), (xs[3]+box_w, xs[4]),
        (xs[4]+box_w, out_x)]
for x0, x1 in gaps:
    arrow(x0 + 0.2, x1 - 0.2, ymid)

# ---- retry / validation feedback loop under stage 4 ----
loop = FancyArrowPatch((xs[4] + box_w - 3, y), (xs[4] + 3, y),
                       connectionstyle="arc3,rad=0.55",
                       arrowstyle="-|>", mutation_scale=12,
                       linewidth=1.2, color="#B279A2", linestyle=(0, (4, 2)), zorder=1)
ax.add_patch(loop)
ax.text(xs[4] + box_w / 2, y - 4.6, "retry ≤ 3 on validation fail",
        ha="center", va="center", fontsize=7.5, color="#7A4F70", style="italic")

# ---- top band labels (spanning the stage pairs) ----
mid_12 = (xs[1] + xs[2] + box_w) / 2
mid_34 = (xs[3] + xs[4] + box_w) / 2
ax.text(mid_12, y + box_h + 2.4, "EXPLAINABLE  ML",
        ha="center", fontsize=8.5, color="#555", fontweight="bold")
ax.text(mid_34, y + box_h + 2.4, "PRESCRIPTIVE  +  GENAI",
        ha="center", fontsize=8.5, color="#555", fontweight="bold")

plt.tight_layout()
out = "outputs/pipeline_overview.png"
plt.savefig(out, dpi=300, bbox_inches="tight", facecolor="white")
print("SAVED", out)
