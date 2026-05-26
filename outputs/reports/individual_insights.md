# Individual Insights — Stress Prediction

**Model terbaik**: `CatBoost` (R² = 0.6391, RMSE = 0.9728, MAE = 0.7717)

## Top-5 Fitur Paling Berpengaruh (SHAP global)

1. `sleep_quality_score` — mean |SHAP| = 0.566
2. `occupation` — mean |SHAP| = 0.548
3. `sleep_duration_hrs` — mean |SHAP| = 0.094
4. `mental_health_condition` — mean |SHAP| = 0.049
5. `rem_percentage` — mean |SHAP| = 0.047

---

## Kontribusi Penelitian

1. **Explainable** — SHAP mengidentifikasi driver utama stres per individu, mendukung interpretabilitas model.
2. **Prescriptive** — DiCE Counterfactual memberi rekomendasi perubahan **behavior** minimal & realistis (causal-sound, di-constrain dengan `permitted_range`).
3. **Naturalized** — GenAI (GPT-4o-mini) mengubah angka teknis menjadi narasi sistem pakar empatik berbahasa Indonesia, dengan safety filter.
