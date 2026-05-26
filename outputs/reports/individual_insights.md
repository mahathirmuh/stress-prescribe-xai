# Individual Insights — Stress Prediction

**Model terbaik**: `CatBoost` (R² = 0.6391, RMSE = 0.9728, MAE = 0.7717)

## Top-5 Fitur Paling Berpengaruh (SHAP global)

1. `sleep_quality_score` — mean |SHAP| = 0.566
2. `occupation` — mean |SHAP| = 0.548
3. `sleep_duration_hrs` — mean |SHAP| = 0.094
4. `mental_health_condition` — mean |SHAP| = 0.049
5. `rem_percentage` — mean |SHAP| = 0.047

---

## Individu LOW Stress

- **Actual stress_score**: 3.00
- **Predicted**: 3.92
- **CF target prediction**: 3.57 (Δ = -0.36)

**Perubahan disarankan (5 fitur):**
- `sleep_duration_hrs`: 7.39 → 9.63
- `screen_time_before_bed_mins`: 11.00 → 151.00
- `steps_that_day`: 3836.00 → 3721.00
- `room_temperature_celsius`: 21.60 → 22.30
- `sleep_aid_used`: 0.00 → 1.00

**Narasi GenAI**:

> Saat ini, Anda memiliki tingkat stres yang relatif rendah dengan skor 3.92, namun ada beberapa area yang bisa diperbaiki untuk lebih menurunkan stres Anda.

---

## Individu MID Stress

- **Actual stress_score**: 6.00
- **Predicted**: 5.82
- **CF target prediction**: 5.75 (Δ = -0.08)

**Perubahan disarankan (4 fitur):**
- `sleep_duration_hrs`: 5.00 → 5.32
- `screen_time_before_bed_mins`: 10.00 → 27.00
- `nap_duration_mins`: 12.00 → 0.00
- `room_temperature_celsius`: 18.30 → 16.00

**Narasi GenAI**:

> Saat ini, tingkat stres Anda berada di angka 5.82, yang menunjukkan adanya beberapa faktor yang dapat mempengaruhi kesejahteraan Anda. Sebagai seorang pengemudi, pekerjaan Anda berkontribusi pada peningkatan stres.

---

## Individu HIGH Stress

- **Actual stress_score**: 8.50
- **Predicted**: 8.33
- **CF target prediction**: 7.94 (Δ = -0.38)

**Perubahan disarankan (4 fitur):**
- `sleep_duration_hrs`: 6.18 → 5.61
- `screen_time_before_bed_mins`: 76.00 → 180.00
- `alcohol_units_before_bed`: 4.00 → 0.00
- `room_temperature_celsius`: 19.60 → 16.00

**Narasi GenAI**:

> Saat ini, tingkat stres Anda berada pada 8.33, yang menunjukkan adanya beberapa faktor yang dapat mempengaruhi kesejahteraan Anda. Beberapa faktor utama yang berkontribusi terhadap stres Anda termasuk kualitas tidur yang rendah dan tuntutan pekerjaan sebagai dokter.

---

## Kontribusi Penelitian

1. **Explainable** — SHAP mengidentifikasi driver utama stres per individu, mendukung interpretabilitas model.
2. **Prescriptive** — DiCE Counterfactual memberi rekomendasi perubahan **behavior** minimal & realistis (causal-sound, di-constrain dengan `permitted_range`).
3. **Naturalized** — GenAI (GPT-4o-mini) mengubah angka teknis menjadi narasi sistem pakar empatik berbahasa Indonesia, dengan safety filter.
