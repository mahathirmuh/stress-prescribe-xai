"""PREVIEW: detailed flowchart-style pipeline diagram for the JUTI paper.

Top-down control-flow with parallel models, data artifacts (I/O), decision
diamonds and feedback loops:
  Data -> Preprocess -> [CatBoost|RF|TabNet] -> CV/select
  -> SHAP explain -> sign-check -> DiCE prescribe -> CF metrics
  -> <CF valid?> (relax & re-run) -> Naturalize (GPT)
  -> <validation pass?> -> <retries<3?> (retry / dummy fallback) -> Narrative.
Saved to outputs/pipeline_flowchart_preview.png (does NOT touch the doc figure).
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon

fig, ax = plt.subplots(figsize=(6.7, 9.7))
ax.set_xlim(0, 104)
ax.set_ylim(0, 158)
ax.axis("off")

EDGE = "#333333"; GRAY = "#5A5A5A"
DEC, DECE = "#F2C14E", "#9C7A12"
LOOP = "#C0504D"; GREEN = "#2e7d32"
IO = "#FFF6E6"; IOE = "#B9912F"
STAGE = {"p": "#4C78A8", "e": "#F58518", "r": "#54A24B", "n": "#B279A2"}

CX, PW = 38.0, 48.0
SX = 86.0   # side column (loops / artifacts)

def rrect(cx, cy, w, h, fc, ec, lw=1.3, rnd=1.1, z=3, dash="solid"):
    ax.add_patch(FancyBboxPatch((cx-w/2, cy-h/2), w, h,
                 boxstyle=f"round,pad=0.2,rounding_size={rnd}",
                 linewidth=lw, edgecolor=ec, facecolor=fc, zorder=z, linestyle=dash))

def stadium(cy, h, text, w=PW, cx=CX, fc=GRAY, tc="white", fs=7.2):
    rrect(cx, cy, w, h, fc, EDGE, rnd=4.5)
    ax.text(cx, cy, text, ha="center", va="center", fontsize=fs, fontweight="bold",
            color=tc, zorder=4, linespacing=1.15)

def proc(cy, h, head, body, color, w=PW, cx=CX, hfs=7.1, bfs=6.0):
    rrect(cx, cy, w, h, "white", color, lw=1.4)
    rrect(cx, cy+h/2-3.5, w, 3.4, color, color, lw=0, rnd=0.4)
    ax.text(cx, cy+h/2-1.8, head, ha="center", va="center", fontsize=hfs,
            fontweight="bold", color="white", zorder=4)
    if body:
        ax.text(cx, cy-1.6, body, ha="center", va="center", fontsize=bfs,
                color="#222", zorder=4, linespacing=1.18)

def smallbox(cx, cy, w, h, head, body, color, hfs=6.2, bfs=5.3):
    rrect(cx, cy, w, h, "white", color, lw=1.3)
    rrect(cx, cy+h/2-2.8, w, 2.7, color, color, lw=0, rnd=0.3)
    ax.text(cx, cy+h/2-1.45, head, ha="center", va="center", fontsize=hfs,
            fontweight="bold", color="white", zorder=4)
    ax.text(cx, cy-1.4, body, ha="center", va="center", fontsize=bfs,
            color="#222", zorder=4, linespacing=1.12)

def diamond(cy, w, h, text, cx=CX, fs=6.3):
    ax.add_patch(Polygon([(cx, cy+h/2), (cx+w/2, cy), (cx, cy-h/2), (cx-w/2, cy)],
                 closed=True, linewidth=1.5, edgecolor=DECE, facecolor=DEC, zorder=3))
    ax.text(cx, cy, text, ha="center", va="center", fontsize=fs, fontweight="bold",
            color="#473800", zorder=4, linespacing=1.1)

def pario(cx, cy, w, h, text):  # parallelogram = data artifact / I/O
    s = 3.0
    pts = [(cx-w/2+s, cy+h/2), (cx+w/2+s, cy+h/2), (cx+w/2-s, cy-h/2), (cx-w/2-s, cy-h/2)]
    ax.add_patch(Polygon(pts, closed=True, linewidth=1.1, edgecolor=IOE, facecolor=IO, zorder=3))
    ax.text(cx, cy, text, ha="center", va="center", fontsize=5.3, style="italic",
            color="#5a4a14", zorder=4, linespacing=1.1)

def sidebox(cy, h, text, cx=SX, w=30, fc="#F7DEDE", ec=LOOP, tc="#7a2e2e", fs=5.9):
    rrect(cx, cy, w, h, fc, ec, lw=1.3)
    ax.text(cx, cy, text, ha="center", va="center", fontsize=fs, fontweight="bold",
            color=tc, zorder=4, linespacing=1.15)

def va(y0, y1, label=None, cx=CX, lcol=GREEN):
    ax.add_patch(FancyArrowPatch((cx, y0), (cx, y1), arrowstyle="-|>",
                 mutation_scale=12, linewidth=1.5, color=EDGE, zorder=2))
    if label:
        ax.text(cx+4.0, (y0+y1)/2, label, ha="left", va="center", fontsize=6.0,
                fontweight="bold", color=lcol, zorder=5)

def fa(x0, y0, x1, y1, color=EDGE, lw=1.4, ms=11, cs=None, dash="solid"):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=ms,
                 linewidth=lw, color=color, zorder=2, linestyle=dash,
                 **({"connectionstyle": cs} if cs else {})))

# ---- y-centers ----
yStart, yPre, yMod, ySel, yExp, ySign, yPres, yMet, yDcf, yNat, yDval, yEnd = \
    152, 140, 127, 114, 101, 90.5, 78, 66, 51, 37, 22, 6

stadium(yStart, 8.5, "Sleep & Lifestyle Data\n100k × 32 features · target stress_score")
proc(yPre, 10, "PREPROCESS", "drop 4 leakage feats · Version A/B encoding\n70/15/15 stratified split", GRAY)

# Stage 1: parallel models -> select
ax.text(CX-PW/2-0.5, yMod+7.6, "STAGE 1 · PREDICT", ha="left", va="bottom",
        fontsize=6.6, fontweight="bold", color=STAGE["p"])
mb_w = 16.0
for cx, nm, pr in [(20, "CatBoost", "1000 it · d6 · lr.05"),
                   (38, "Random Forest", "300 trees · leaf 5"),
                   (56, "TabNet", "≤200 ep · bs 1024")]:
    smallbox(cx, yMod, mb_w, 11, nm, pr, STAGE["p"], hfs=6.0)
proc(ySel, 10, "5-FOLD CV · SELECT BEST", "→ CatBoost  (R² 0.650 · RMSE 0.952 · MAE 0.758)", STAGE["p"])

# Stage 2: explain
proc(yExp, 11, "STAGE 2 · EXPLAIN (SHAP)", "TreeExplainer (2000) → global mean|SHAP|\n+ local waterfall plots", STAGE["e"])
proc(ySign, 7.5, "DOMAIN SIGN-CHECK ✓", "directional signs vs sleep medicine (r = −0.996)", STAGE["e"], hfs=6.4, bfs=5.6)
pario(SX, yExp, 28, 8, "SHAP values\n(global + local)")

# Stage 3: prescribe
proc(yPres, 12, "STAGE 3 · PRESCRIBE (DiCE)", "group features: behavior / outcome / immutable\ngenetic search, behavior-only · permitted_range", STAGE["r"])
proc(yMet, 9, "COMPUTE 5 CF METRICS", "validity · proximity · sparsity · diversity · plausibility", STAGE["r"], hfs=6.4, bfs=5.5)
pario(SX, yMet, 28, 8, "candidate\ncounterfactuals")
diamond(yDcf, 40, 17, "Counterfactual\nvalid?")

# Stage 4: naturalize
proc(yNat, 12, "STAGE 4 · NATURALIZE (GPT-4o-mini)", "counselor system prompt + CF facts\nT=0.3 · JSON · 5 fields", STAGE["n"])
pario(SX, yNat, 28, 8, "JSON output\n(5 fields)")
diamond(yDval, 44, 16, "Validation pass?\nsafety · faithful · struct")
stadium(yEnd, 8.5, "NARRATIVE RECOMMENDATION\nactionable · empathetic · Bahasa Indonesia")

# side loop / decision boxes
sidebox(yDcf, 11, "Relax target\n−0.30 → −0.15 → −0.05")
ax.add_patch(Polygon([(SX, yDval+7), (SX+13, yDval), (SX, yDval-7), (SX-13, yDval)],
             closed=True, linewidth=1.4, edgecolor=DECE, facecolor=DEC, zorder=3))
ax.text(SX, yDval, "retries\n< 3?", ha="center", va="center", fontsize=5.8,
        fontweight="bold", color="#473800", zorder=4, linespacing=1.1)
sidebox(yEnd, 8, "Dummy\nfallback", cx=SX, w=22)

# ---- main flow ----
va(yStart-4.3, yPre+5.1)
# preprocess -> 3 models (fan out)
for cx in (20, 38, 56):
    fa(CX, yPre-5.1, cx, yMod+5.6)
# 3 models -> select (fan in)
for cx in (20, 38, 56):
    fa(cx, yMod-5.6, CX, ySel+5.1)
va(ySel-5.1, yExp+5.6)
va(yExp-5.6, ySign+3.9)
va(ySign-3.9, yPres+6.1)
va(yPres-6.1, yMet+4.6)
va(yMet-4.6, yDcf+8.6)
va(yDcf-8.6, yNat+6.1, label="Yes")
va(yNat-6.1, yDval+8.1)
va(yDval-8.1, yEnd+4.4, label="Yes")

# thin artifact arrows
for ycp, ya in [(yExp, yExp), (yMet, yMet), (yNat, yNat)]:
    fa(CX+PW/2, ycp, SX-14, ya, color=IOE, lw=0.9, ms=8)

# CF-invalid loop: Dcf -> relax -> back to prescribe
fa(CX+20, yDcf, SX-15, yDcf, color=LOOP, ms=10)
ax.text((CX+20+SX-15)/2, yDcf+2.4, "No", ha="center", va="center", fontsize=6.0,
        fontweight="bold", color=LOOP, zorder=5)
fa(SX, yDcf+5.5, CX+PW/2, yPres, color=LOOP, lw=1.3, cs="angle,angleA=90,angleB=0,rad=4")
ax.text(SX-6, yPres-4, "relax & re-run", ha="center", va="center", fontsize=5.6,
        fontweight="bold", color=LOOP, zorder=5)

# validation-fail -> retry decision
fa(CX+22, yDval, SX-13, yDval, color=LOOP, ms=10)
ax.text((CX+22+SX-13)/2, yDval+2.4, "No", ha="center", va="center", fontsize=6.0,
        fontweight="bold", color=LOOP, zorder=5)
# retry yes -> back to naturalize
fa(SX, yDval+7, CX+PW/2, yNat, color=LOOP, lw=1.3, cs="angle,angleA=90,angleB=0,rad=4")
ax.text(SX-7, yNat-4, "retry (Yes)", ha="center", va="center", fontsize=5.6,
        fontweight="bold", color=LOOP, zorder=5)
# retry no -> dummy fallback -> end
fa(SX, yDval-7, SX, yEnd+4, color=LOOP, lw=1.2, dash="--")
ax.text(SX+2, (yDval-7+yEnd)/2+3, "No", ha="left", va="center", fontsize=5.6,
        fontweight="bold", color=LOOP, zorder=5)
fa(SX-11, yEnd, CX+PW/2, yEnd, color=LOOP, lw=1.2, dash="--")
ax.text(SX-17, yEnd+2.6, "fallback", ha="center", va="center", fontsize=5.4,
        style="italic", color=LOOP, zorder=5)

plt.tight_layout(pad=0.3)
out = "outputs/pipeline_flowchart_preview.png"
plt.savefig(out, dpi=300, bbox_inches="tight", facecolor="white")
print("SAVED", out)
