# Stress Prediction with Explainable ML + Counterfactual + GenAI

Implementasi penelitian UTS Kecerdasan Komputasional S2: prediksi `stress_score` dari data tidur & gaya hidup, dijelaskan dengan SHAP, diberi rekomendasi via counterfactual (DiCE), lalu dinaturalisasi menjadi narasi sistem pakar via GPT.

Detail riset di [research_draft.md](research_draft.md).

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

## Struktur

```
.
├── sleep_health_dataset.csv          # dataset 100k baris
├── research_draft.md                 # konsep & metodologi
├── stress_prediction.ipynb           # notebook utama end-to-end
├── prompts/
│   └── expert_system_prompt.md       # system prompt GPT
├── data/processed/                   # encoder, scaler, split data
├── models/                           # model terlatih
└── outputs/
    ├── figures/                      # plot EDA, SHAP, CF
    ├── reports/                      # ringkasan & insight
    └── recommendations/              # output naratif GPT (.json)
```

## Alur Kerja

1. **Section 0–2**: setup, load data, EDA
2. **Section 3**: preprocessing (drop leakage, encoding, split 70/15/15)
3. **Section 4**: train **CatBoost** (milestone — validasi pipeline) ⭐
4. **Section 5–6**: train Random Forest & TabNet
5. **Section 7**: bandingkan 3 model, pilih best
6. **Section 8**: SHAP global + local (3 individu: stres rendah/sedang/tinggi)
7. **Section 9**: Counterfactual analysis (DiCE) untuk 3 individu
8. **Section 10**: GPT naturalisasi → narasi sistem pakar (JSON terstruktur)
9. **Section 11**: insight individual & kesimpulan
10. **Section 12**: re-run di full 100k

Toggle `USE_SAMPLE = True` di Section 0 untuk iterasi cepat dengan 10k sampel.
