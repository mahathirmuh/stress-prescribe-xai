# Stress Prediction with Explainable ML + Counterfactual + GenAI

Penelitian conference paper: framework 4-tahap untuk prediksi `stress_score` dari data tidur & gaya hidup, dijelaskan dengan SHAP, diberi rekomendasi via counterfactual (DiCE), lalu dinaturalisasi menjadi narasi sistem pakar berbahasa Indonesia via GPT-4o-mini.

**Authors**: Ananta Dwi Prayoga Alwy, Dhayu Intan Nareswari, Mahathir Muhammad, Obi Kastanya
Department of Informatics, Faculty of Intelligent Electrical and Informatics Technology, Institut Teknologi Sepuluh Nopember (ITS), Surabaya.

Detail riset di [docs/research_draft.md](docs/research_draft.md). Paper final di `JUTI.docx` (lokal, gitignored).

## Pipeline 4-Tahap

1. **PREDICT** — Regresi `stress_score` (1.0–10.0) pakai CatBoost, Random Forest, TabNet
2. **EXPLAIN** — SHAP global + local + domain validity sign-check
3. **PRESCRIBE** — DiCE counterfactual dengan causal restriction (behavior-only)
4. **NATURALIZE** — GPT-4o-mini dengan 3-layer validation (safety + structural + faithfulness)

## Hasil Utama (sample 10k)

| Metrik | Value |
|---|---|
| **CatBoost R²** | 0.6503 (best dari 3 model) |
| MAE | 0.7584 |
| 5-Fold CV R² | 0.6266 ± 0.0093 |
| SHAP `sleep_quality_score` corr | −0.996 (domain valid) |
| **CF Success Rate** | 62.5% (25 dari 40 instances) |
| Plausibility | 100% (semua CF di dalam `permitted_range`) |
| Case Studies | 3/3 sukses (low/mid/high) |
| GenAI naturalization | 3/3 lolos safety + structural + faithfulness |

## Setup

### 1. Buat virtual environment & install dependencies

PowerShell (Windows):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Bash (Linux/Mac):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Siapkan API key OpenAI

```powershell
Copy-Item .env.example .env
# lalu edit .env, isi OPENAI_API_KEY
```

### 3. Jalankan notebook

```powershell
jupyter notebook stress_prediction.ipynb
```

Toggle `USE_SAMPLE = True` di Section 0 untuk iterasi cepat dengan 10k sampel (~15–20 menit). Set `False` di Section 13 untuk full 100k run (~60–120 menit, CPU only).

## Struktur Repository

```
.
├── stress_prediction.ipynb           # notebook utama end-to-end (13 sections)
├── sleep_health_dataset.csv          # dataset Kaggle 100k baris × 32 kolom
├── build_slides_v2.py                # generator deck (-> kk-ngebut_slides_v2.pptx)
├── make_pipeline_fig*.py             # generator figur pipeline (alternatif matplotlib)
├── requirements.txt                  # dependencies Python
├── README.md                         # file ini
├── .env.example                      # template API key
├── JUTI.docx / JUTI.pdf              # paper aktif (format JUTI)
├── kk-ngebut_slides_v2.pptx          # slide aktif
├── docs/                             # dokumentasi
│   ├── research_draft.md             # draft riset & metodologi
│   ├── plan.md                       # detail implementasi per-section
│   ├── REFERENCES.md                 # 40 referensi IEEE (clickable)
│   └── PIPELINE_FLOWCHART.md         # penjelasan flowchart pipeline
├── prompts/
│   └── expert_system_prompt.md       # system prompt GPT dengan safety rules
├── data/processed/                   # encoder, scaler, split data (artifacts)
├── models/                           # model terlatih (catboost.cbm dll)
├── outputs/
│   ├── figures/                      # plot EDA, SHAP, CF (PNG)
│   ├── reports/                      # CSV/MD metrics & insights
│   ├── recommendations/              # output JSON naratif GPT per individu
│   └── pipeline_flowchart.svg/.png   # flowchart pipeline (Fig. 1 paper)
├── catboost_info/                    # log training CatBoost (auto-generated)
└── archive/                          # arsip non-aktif (gitignored): versi lama, backup, template
```

## Alur Kerja Notebook (13 Sections)

1. **§0–2**: Setup, load data, EDA (verifikasi statistik draft)
2. **§3**: Preprocessing (drop 4 leakage features, dual-encoding A/B, stratified 70/15/15)
3. **§4**: Train **CatBoost** ⭐ milestone (R² ≥ 0.6, MAE ≤ 1.0)
4. **§5–6**: Train Random Forest & TabNet
5. **§7**: Comparison + 5-Fold CV pada best model
6. **§8**: SHAP global (bar + beeswarm) + local (waterfall × 3) + domain validity sign-check
7. **§9**: Counterfactual analysis (DiCE genetic method)
    - Causal restriction: behavior vs outcome vs immutable
    - `permitted_range` safety constraints (alcohol locked at [0,0], dll)
    - 5 metrics: Validity, Proximity, Sparsity, Diversity, Plausibility
    - Cascade retry untuk case studies (target orig−0.30 → −0.15 → −0.05)
8. **§10**: GenAI naturalization dengan **3-layer validation**:
    - **Layer 1 — Safety filter**: regex blocklist (obat, diagnosa, promote alkohol)
    - **Layer 2 — Faithfulness check**: angka before/after exact match, no locked outcome leak
    - **Layer 3 — Structural validation**: required keys + type + content + nested schema
    - Iterative refinement retry (kirim feedback ke GPT antar attempt)
9. **§11**: Individual insights & kesimpulan (markdown rendering)
10. **§12**: Limitations & threats to validity (7 sub-sections)
11. **§13**: Instruksi re-run full 100k

## Paper & Slides

Output bukan-kode (tidak di-track di git, ada di disk lokal):

- `JUTI.docx` — paper format JUTI (single column, IEEE refs, flowchart pipeline + 40 referensi)
- `JUTI.pdf` — PDF export untuk submission
- `kk-ngebut_slides_v2.pptx` — deck presentasi (regenerate via `python build_slides_v2.py`)
- `archive/` — versi lama (paper & slide v1), backup `JUTI.docx`, dan template jurnal

## Causal Restriction (Yang Membuat Pipeline Unik)

DiCE counterfactual **hanya boleh mengubah** behavior features:
- `sleep_duration_hrs`, `screen_time_before_bed_mins`, `caffeine_mg_before_bed`
- `alcohol_units_before_bed`, `exercise_day`, `steps_that_day`
- `nap_duration_mins`, `room_temperature_celsius`, `sleep_aid_used`

Sementara outcome features (`sleep_quality_score`, `rem_percentage`, `heart_rate_resting_bpm`, dll) dan immutable features (`age`, `gender`, `occupation`, dll) **di-lock** dari modifikasi. Ini menjamin rekomendasi intervensi adalah **manipulable causes**, bukan outcomes yang user tidak bisa kontrol langsung.

## Lisensi & Akademik

Penelitian akademik, kode untuk reproducibility paper. Dataset Sleep Health & Daily Performance dari Kaggle (sintetis). Atribusi pada paper.
