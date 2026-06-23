# Panduan Implementasi Penelitian: Explainable ML + Counterfactual + GenAI untuk Prediksi & Intervensi Stres

## Context

Penelitian ini bertujuan membangun **framework prediksi stres yang prescriptive** dari [sleep_health_dataset.csv](../sleep_health_dataset.csv) (100k baris × 32 kolom). Alur:

1. **Predict**: model regresi (`CatBoost`, `RandomForest`, `TabNet`) → `stress_score` (1.0–10.0)
2. **Explain**: SHAP → fitur penyebab prediksi
3. **Prescribe**: Counterfactual (DiCE) → perubahan minimal & realistis pada fitur
4. **Naturalize**: **GenAI (GPT)** → narasi sistem pakar (saran empatik, kontekstual, actionable) dari output counterfactual

Judul penelitian: **"Explainable Machine Learning with Counterfactual Analysis for Stress Prediction and Intervention Using Sleep and Lifestyle Data"**

**Penting tentang scope GenAI**: Judul tidak memuat GenAI, sehingga GenAI diposisikan sebagai **deployment layer** untuk presentasi naratif kepada pengguna akhir, **bukan sebagai kontribusi ilmiah utama**. Evaluasi GenAI terbatas pada **faithfulness check otomatis + safety filter**, tidak memerlukan user study atau expert panel.

Catatan: **evaluasi output GenAI** dalam bentuk rigor (user study, expert review) akan dibahas terpisah setelah implementasi inti jalan. Saat ini fokus pada membangun pipeline.

Unsur keterbaruan vs [research_draft.md](research_draft.md):
- **Tahap 4 (GenAI naturalisasi)** belum ada di draft, perlu ditambahkan ke `research_draft.md` (di luar plan mode)

Preferensi user:
- **Format**: 1 Jupyter Notebook end-to-end (`stress_prediction.ipynb`)
- **Iterasi**: Sample 10k dulu, baru full 100k
- **Urutan**: CatBoost end-to-end dulu, baru tambah RF/TabNet
- **Env**: Buat dari nol (venv + requirements.txt)

User: mahasiswa S2 Kecerdasan Komputasional, untuk UAS.

---

## Struktur Proyek

```
kk-ngebut/
├── sleep_health_dataset.csv          # sudah ada
├── research_draft.md                 # UPDATE (setelah keluar plan mode) — tambah section GenAI
├── draft_paper.pdf                   # sudah ada
├── requirements.txt                  # BUAT
├── README.md                         # BUAT
├── .env.example                      # BUAT — template OPENAI_API_KEY
├── .gitignore                        # BUAT — exclude .env, .venv, data besar
├── stress_prediction.ipynb           # BUAT — 1 notebook end-to-end
├── prompts/
│   └── expert_system_prompt.md       # BUAT — system prompt untuk GPT
├── data/
│   └── processed/
├── models/                           # .cbm, .pkl, .zip
└── outputs/
    ├── figures/                      # EDA, SHAP, CF plots
    ├── reports/                      # metrik & insight
    └── recommendations/              # output teks GPT per individu (.json)
```

---

## Struktur Notebook (`stress_prediction.ipynb`)

### Section 0 — Setup & Konfigurasi
- Import semua libraries (pandas, numpy, sklearn, catboost, pytorch-tabnet, shap, dice-ml, openai, matplotlib, seaborn, joblib, python-dotenv)
- Load `OPENAI_API_KEY` dari `.env`
- Set `RANDOM_STATE = 42`, `USE_SAMPLE = True`, path konstan
- Buat folder output otomatis

### Section 1 — Load & Sampling
Load CSV, stratified sample 10k by `stress_score` bin (jika `USE_SAMPLE`), tampilkan `.info()`, `.describe()`, cek missing.

### Section 2 — EDA
Distribusi target, heatmap korelasi, box plot kategorikal vs target, verifikasi statistik draft (mean ≈ 5.73, korelasi `sleep_quality_score` ≈ -0.639). Simpan ke `outputs/figures/eda_*.png`.

### Section 3 — Preprocessing
Drop leakage features (`person_id`, `cognitive_performance_score`, `sleep_disorder_risk`, `felt_rested`). Buat 2 versi data: **A (CatBoost-native)** dan **B (encoded+scaled untuk RF/TabNet)**. Split 70/15/15 stratified. Simpan encoder/scaler.

### Section 4 — CatBoost End-to-End ⭐ MILESTONE 1
- Train `CatBoostRegressor(iterations=1000, depth=6, lr=0.05, early_stopping_rounds=50, cat_features=...)`
- Evaluasi test: R², RMSE, MAE + plot pred vs actual + residual
- Simpan `models/catboost.cbm`
- **PAUSE** — validasi (R² ≥ 0.6, MAE ≤ 1.0)

### Section 5 — Random Forest
Train `RandomForestRegressor(n_estimators=300, min_samples_leaf=5, n_jobs=-1)` di Versi B. Evaluasi. Simpan.

### Section 6 — TabNet
Train `TabNetRegressor` di Versi B (scaled). `max_epochs=200, patience=20, batch_size=1024`. Evaluasi. Simpan.

### Section 7 — Perbandingan Model
Tabel R²/RMSE/MAE per model + 5-Fold CV pada model terbaik. Bar chart. Pilih `best_model` untuk SHAP+CF+GPT.

### Section 8 — SHAP Explainability
- Global: `summary_plot` (bar + beeswarm)
- Local: 3 individu (stres ~3, ~6, ~8.5) → `waterfall_plot`
- Domain validity sign-check top-10 fitur
- Konsistensi top-10 lintas model

### Section 9 — Counterfactual Analysis (DiCE)

#### 9.1 Kategorisasi Fitur (Causal Soundness)

Fitur dikelompokkan dengan ketat sebelum CF generation untuk menjamin **"Intervention" di judul terpenuhi**:

| Kategori | Fitur | Boleh diubah CF? |
|---|---|---|
| **Behavior (intervensi langsung)** | `sleep_duration_hrs`, `screen_time_before_bed_mins`, `caffeine_mg_before_bed`, `alcohol_units_before_bed`, `exercise_day`, `steps_that_day`, `nap_duration_mins`, `room_temperature_celsius`, `sleep_aid_used` | ✅ |
| **Outcome (gejala/hasil dari kebiasaan)** | `sleep_quality_score`, `wake_episodes_per_night`, `sleep_latency_mins`, `rem_percentage`, `deep_sleep_percentage`, `heart_rate_resting_bpm` | ❌ — gunakan sebagai validator/indikator saja |
| **Immutable** | `age`, `gender`, `occupation`, `country`, `bmi`, `chronotype`, `season`, `shift_work`, `mental_health_condition`, `day_type` | ❌ |

#### 9.2 Setup DiCE dengan Permitted Range (Safety)

`features_to_vary` = list behavior features di atas.

`permitted_range` eksplisit per behavior feature (safety constraint):

| Fitur | Range | Alasan |
|---|---|---|
| `sleep_duration_hrs` | [4.0, 10.0] | < 4 berbahaya, > 10 indikator depresi |
| `caffeine_mg_before_bed` | [0, 400] | 400mg = batas aman FDA |
| `alcohol_units_before_bed` | [0, 0] | Cegah rekomendasi konsumsi alkohol |
| `screen_time_before_bed_mins` | [0, 180] | 0 tidak realistis, 180 batas atas |
| `exercise_day` | [0, 1] | Binary |
| `steps_that_day` | [1000, 15000] | Realistic range |
| `nap_duration_mins` | [0, 30] | > 30 menit ganggu tidur malam |
| `room_temperature_celsius` | [16, 26] | Range nyaman untuk tidur |
| `sleep_aid_used` | [0, 1] | Binary |

#### 9.3 CF Evaluation pada 50–100 Instance (Kuantitatif)

Generate CF untuk **50–100 test instance** (stratified sampling by stress quartile), `total_CFs=3` per instance. Hitung 5 metrik standar komunitas DiCE:

| Metrik | Definisi | Target |
|---|---|---|
| **Validity** | % CF yang mencapai `desired_range` target | ≥ 80% |
| **Proximity** | Mean L1-distance normalized antara CF dan original | rendah = realistis |
| **Sparsity** | Mean jumlah fitur yang diubah per CF | 2–4 ideal |
| **Diversity** | Mean pairwise L1-distance antar k CF | sedang–tinggi |
| **Plausibility** | % CF dalam `permitted_range` | 100% (jika setup benar) |

Simpan tabel ke `outputs/reports/cf_evaluation_metrics.csv` + boxplot per quartile stress ke `outputs/figures/cf_metrics_*.png`.

#### 9.4 Case Study 3 Individu (Naratif)

3 individu (stres ~3, ~6, ~8.5) tetap di-generate untuk case study naratif di Section 11. Tampilkan tabel: original → CF → delta prediksi.

### Section 10 — GenAI Naturalisasi (BARU) 🆕
Tujuan: ubah angka CF menjadi narasi sistem pakar yang empatik & actionable.

- **System prompt** (`prompts/expert_system_prompt.md`):
  - Peran: konselor kesehatan tidur & manajemen stres
  - Aturan: hanya gunakan fakta dari input (no hallucination), tone empatik, bahasa Indonesia awam
  - **LARANGAN MUTLAK (safety)**: no diagnosis, no medical claims, no obat/suplemen, no terapi spesifik, no janji pasti
  - **Disclaimer wajib** di setiap output
  - Struktur output: ringkasan kondisi → 3 driver utama → 3 langkah konkret → motivasi → disclaimer
- **User prompt template** per individu, berisi:
  - (a) Profil singkat (umur, gender, pekerjaan)
  - (b) Prediksi `stress_score` aktual
  - (c) Top-5 SHAP feature contributions (nama fitur + nilai + arah pengaruh)
  - (d) Hasil CF (fitur yang diubah + nilai before/after + delta prediksi)
- **API call**:
  ```python
  client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[{"role": "system", ...}, {"role": "user", ...}],
      temperature=0.3,
      max_tokens=600,
      response_format={"type": "json_object"}
  )
  ```
- Output JSON terstruktur:
  ```json
  {
    "summary": "...",
    "drivers": ["...", "...", "..."],
    "recommendations": [
      {"action": "...", "target": "...", "rationale": "..."},
      ...
    ],
    "encouragement": "...",
    "disclaimer": "..."
  }
  ```
- Generate untuk 3 individu (low/mid/high), simpan ke `outputs/recommendations/individual_{id}.json`
- Tampilkan inline di notebook + render markdown
- **Safety filter (post-generation)**: regex check untuk kata terlarang (`obat`, `diagnosa`, `melatonin`, `antidepresan`, `menyembuhkan`, `akan menurunkan`, dll). Flag jika ada, lalu re-generate.

### Section 11 — Individual Insights & Kesimpulan
Narasi 3 individu (low/mid/high): profil → prediksi → SHAP drivers → CF → rekomendasi GPT. Ringkasan: model terbaik, fitur paling berpengaruh, kontribusi penelitian (explainable + prescriptive + naturalized). Simpan ke `outputs/reports/individual_insights.md`.

### Section 12 — Limitations & Threats to Validity (BARU) 🆕

Section eksplisit di notebook dan paper yang membahas keterbatasan jujur. Wajib untuk paper akademik formal.

**12.1 Dataset Sintetis**
- Dataset Sleep Health & Daily Performance (Kaggle) adalah **data sintetis**, bukan pengukuran riil dari subjek manusia
- Korelasi & pola yang ditemukan mungkin merupakan artefak generator data, bukan fenomena alami
- **Disclaimer**: Penelitian ini adalah **methodological proof-of-concept**, bukan validasi klinis. Generalisasi ke populasi nyata memerlukan validasi pada data klinis.

**12.2 Asumsi Kausalitas pada Counterfactual**
- DiCE mengasumsikan **causal stationarity**: perubahan fitur akan menghasilkan perubahan prediksi secara konsisten
- Pada data sintetis, asumsi ini belum tentu valid → rekomendasi intervensi harus dipahami sebagai "kemungkinan", bukan "kepastian"
- Validasi kausal nyata memerlukan eksperimen prospektif

**12.3 GenAI Evaluation Scope**
- Evaluasi GenAI terbatas pada **faithfulness check otomatis** (coverage, direction, hallucination)
- Tidak ada user study, expert panel, atau validasi klinis output GenAI
- GenAI diposisikan sebagai **deployment layer**, bukan kontribusi ilmiah → evaluasi rigor LLM di luar scope

**12.4 Reproducibility Bound**
- `random_state=42` digunakan konsisten, namun hasil GPT bersifat probabilistik meski dengan `temperature=0.3`
- Variasi minor pada output GenAI bisa terjadi antar run

Simpan ke `outputs/reports/limitations.md`.

### Section 13 — Re-run Full 100k (di akhir)
Set `USE_SAMPLE = False`, restart kernel, re-run section 1–12.

---

## Update `research_draft.md` (di luar plan mode)

Setelah plan disetujui, akan ditambah/diubah (hanya bagian GenAI, evaluasi nanti):

1. **Bagian 1 (Pendahuluan)**: tambah satu paragraf — interpretasi teknis SHAP/CF masih sulit dipahami non-ahli, perlu lapisan naturalisasi via GenAI.
2. **Bagian 2 (Rumusan Masalah)**: tambah poin "Bagaimana mengubah output counterfactual menjadi rekomendasi naratif yang mudah dipahami pengguna awam menggunakan GenAI?"
3. **Bagian 3 (Tujuan)**: tambah tujuan terkait GenAI naturalisasi.
4. **Bagian 5 (Keterbaruan)**: tambah subbab "5.4 Naturalisasi Rekomendasi dengan GenAI" — counterfactual mentah berupa angka diubah menjadi narasi sistem pakar.
5. **Bagian 9 (Metodologi)**: tambah 9.7 "GenAI Naturalisasi" — prompt engineering, output JSON terstruktur, integrasi dengan SHAP + CF.
6. **Bagian 10 (Teknologi)**: tambah `OpenAI Python SDK / GPT-4o-mini`, `python-dotenv`.
7. **Bagian 12 (Output)**: tambah "rekomendasi naratif siap pakai untuk pengguna awam".

Catatan: pengujian/evaluasi output GenAI akan ditambah ke `research_draft.md` di iterasi berikutnya setelah pipeline jalan.

---

## File yang Akan Dibuat/Diubah

| File | Status | Tujuan |
|---|---|---|
| `requirements.txt` | BUAT | pandas, numpy, scikit-learn, catboost, pytorch-tabnet, shap, dice-ml, openai, python-dotenv, matplotlib, seaborn, jupyter, joblib |
| `.env.example` | BUAT | Template `OPENAI_API_KEY=...` |
| `.gitignore` | BUAT | Exclude `.env`, `.venv`, `__pycache__`, file besar |
| `README.md` | BUAT | Setup venv + .env, cara jalankan |
| `stress_prediction.ipynb` | BUAT | Notebook utama end-to-end |
| `prompts/expert_system_prompt.md` | BUAT | System prompt GPT |
| `research_draft.md` | UPDATE | Tambah bagian GenAI (di luar plan mode) |
| `data/processed/`, `models/`, `outputs/*` | BUAT (folder) | Storage |

---

## Verifikasi End-to-End

- **Section 4**: CatBoost R² ≥ 0.6, MAE ≤ 1.0 pada sample 10k
- **Section 7**: minimal satu model R² ≥ 0.65, top-3 SHAP konsisten lintas model
- **Section 9**: 
  - CF generation: 3 alternatif per individu untuk 50–100 test instance
  - Metrik target: Validity ≥ 80%, Plausibility 100%, Sparsity 2–4 fitur, Proximity rendah
- **Section 10**: 
  - GPT output valid JSON dengan field `disclaimer`
  - Faithfulness check: coverage 100%, direction correct ≥ 95%
  - Safety filter: 0 flagging kata terlarang
- **Section 12**: Limitations section ditulis lengkap, mencakup data sintetis, asumsi kausal, GenAI scope
- **Section 13**: semua section selesai pada full 100k tanpa error

---

## Catatan Vibe Coding

- **Iterasi**: `USE_SAMPLE=True` sampai Section 11 jalan, baru `False` untuk run final
- **PAUSE points**: setelah Section 4 (CatBoost), Section 9 (CF), Section 10 (GPT output pertama) — review hasil
- **Cost control GPT**: `gpt-4o-mini`, `temperature=0.3` (lebih deterministik), `max_tokens=600`. 3 individu × beberapa retry ≈ <$0.05 total
- **JSON output mode** untuk parsing reliable (`response_format={"type": "json_object"}`)
- **API key handling**: `.env` di-`.gitignore`, jangan commit. `.env.example` untuk dokumentasi
- **Fallback**: jika DiCE bermasalah → custom CF grid search. Jika OpenAI API down → tunjukkan struktur prompt + dummy output
- **Evaluasi output GenAI**: akan dibahas terpisah setelah pipeline jalan
