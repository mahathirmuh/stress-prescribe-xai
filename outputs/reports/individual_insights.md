# Individual Insights — Stress Prediction

**Model terbaik**: `CatBoost` (R² = 0.6503, RMSE = 0.9523, MAE = 0.7584)

## Top-5 Fitur Paling Berpengaruh (SHAP global)

1. `sleep_quality_score` — mean |SHAP| = 0.660
2. `occupation` — mean |SHAP| = 0.569
3. `sleep_duration_hrs` — mean |SHAP| = 0.133
4. `room_temperature_celsius` — mean |SHAP| = 0.084
5. `wake_episodes_per_night` — mean |SHAP| = 0.077

---

## Individu LOW Stress

- **Actual stress_score**: 3.00
- **Predicted**: 4.05
- **CF target prediction**: 3.85 (Δ = -0.21)

**Perubahan disarankan (4 fitur):**
- `sleep_duration_hrs`: 6.08 → 7.78
- `screen_time_before_bed_mins`: 29.00 → 30.00
- `steps_that_day`: 13046.00 → 1000.00
- `room_temperature_celsius`: 17.20 → 16.00

**Narasi GenAI**:

> Saat ini, Anda memiliki tingkat stres yang cukup tinggi dengan skor 4.05. Ada beberapa area yang dapat diperbaiki untuk membantu menurunkan tingkat stres Anda.

---

## Individu MID Stress

- **Actual stress_score**: 6.00
- **Predicted**: 5.25
- **CF target prediction**: 4.95 (Δ = -0.30)

**Perubahan disarankan (6 fitur):**
- `sleep_duration_hrs`: 6.86 → 5.79
- `screen_time_before_bed_mins`: 145.00 → 0.00
- `caffeine_mg_before_bed`: 100.00 → 40.00
- `steps_that_day`: 7156.00 → 1000.00
- `nap_duration_mins`: 0.00 → 29.00
- `room_temperature_celsius`: 24.00 → 25.50

**Narasi GenAI**:

> Saat ini, tingkat stres Anda berada di angka 5.25, yang menunjukkan adanya beberapa faktor yang dapat diperbaiki untuk membantu menurunkan stres Anda.

---

## Individu HIGH Stress

- **Actual stress_score**: 8.50
- **Predicted**: 7.21
- **CF target prediction**: 6.84 (Δ = -0.38)

**Perubahan disarankan (4 fitur):**
- `sleep_duration_hrs`: 6.01 → 5.76
- `screen_time_before_bed_mins`: 102.00 → 0.00
- `alcohol_units_before_bed`: 1.00 → 0.00
- `room_temperature_celsius`: 20.80 → 23.10

**Narasi GenAI**:

> Saat ini, tingkat stres Anda berada di angka 7.21, yang menunjukkan adanya tekanan yang cukup tinggi dalam hidup Anda. Beberapa faktor yang berkontribusi terhadap stres ini termasuk durasi tidur dan kebiasaan sebelum tidur.

---

## Kontribusi Penelitian

1. **Explainable** — SHAP mengidentifikasi driver utama stres per individu, mendukung interpretabilitas model.
2. **Prescriptive** — DiCE Counterfactual memberi rekomendasi perubahan **behavior** minimal & realistis (causal-sound, di-constrain dengan `permitted_range`).
3. **Naturalized** — GenAI (GPT-4o-mini) mengubah angka teknis menjadi narasi sistem pakar empatik berbahasa Indonesia, dengan safety filter.
