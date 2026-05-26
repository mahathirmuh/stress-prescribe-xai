# Limitations & Threats to Validity

## 12.1 Dataset Sintetis

Dataset Sleep Health & Daily Performance (Kaggle) adalah **data sintetis**, bukan pengukuran riil dari subjek manusia. Korelasi dan pola yang ditemukan mungkin merupakan artefak generator data, bukan fenomena alami.

**Disclaimer**: Penelitian ini adalah **methodological proof-of-concept**, bukan validasi klinis. Generalisasi ke populasi nyata memerlukan validasi pada data klinis.

## 12.2 Asumsi Kausalitas pada Counterfactual

DiCE mengasumsikan **causal stationarity** — perubahan fitur akan menghasilkan perubahan prediksi secara konsisten. Pada data sintetis, asumsi ini belum tentu valid. Rekomendasi intervensi harus dipahami sebagai "kemungkinan", bukan "kepastian". Validasi kausal nyata memerlukan eksperimen prospektif (RCT).

Untuk mitigasi parsial, kami:
- Memisahkan **behavior** (boleh diubah CF) vs **outcome** (locked, gejala) vs **immutable** (locked, atribut statis)
- Menerapkan `permitted_range` eksplisit per fitur behavior

## 12.3 GenAI Evaluation Scope

Evaluasi GenAI terbatas pada:
- **Struktur output**: JSON valid + key wajib (`summary`, `drivers`, `recommendations`, `encouragement`, `disclaimer`)
- **Safety filter**: regex blocklist untuk kata terlarang (obat, diagnosa, janji pasti, alkohol)

**Tidak dilakukan**: user study, expert panel, atau validasi klinis output GenAI. GenAI diposisikan sebagai **deployment layer** untuk presentasi naratif, bukan kontribusi ilmiah utama. Evaluasi rigor LLM (faithfulness scoring lewat human raters, hallucination benchmark) di luar scope penelitian ini.

## 12.4 Reproducibility Bound

`random_state=42` digunakan konsisten di seluruh pipeline (sampling, split, model). Namun:
- **DiCE** menggunakan `method='genetic'` — meskipun seed di-set, hasil bisa sedikit bervariasi karena sampling internal
- **GPT** bersifat probabilistik meski `temperature=0.3` — variasi minor antar run masih mungkin terjadi
- **TabNet** sensitif terhadap inisialisasi weight — gunakan multiple seeds untuk publikasi

## 12.5 Sampling Bias

Hasil pada sampel 10k bisa berbeda dari full 100k. Section 13 menjalankan ulang full untuk validasi final.

## 12.6 Modest Effect Size of Behavior-Only Counterfactuals

Eksperimen kami menunjukkan **finding penting**: ketika DiCE direstrik hanya mengubah behavior features (sleep_duration, screen_time, caffeine, exercise, dll) dengan outcome features tetap locked, **counterfactual yang dihasilkan hanya menggeser prediksi stress score sebesar ~0.3 poin**. Magnitudo ini lebih kecil dibandingkan jika outcomes diizinkan berubah (yang bisa menggeser >1.5 poin), tetapi merupakan estimasi yang **causally honest**.

**Interpretasi**: pada dataset Sleep Health, kontribusi behavior features terhadap variansi `stress_score` dimediasi oleh outcomes (mis. sleep duration mempengaruhi sleep quality, yang kemudian mempengaruhi stress). Counterfactual behavior-only menangkap hanya **direct effect**, sedangkan total effect (direct + indirect) memerlukan **two-stage causal architecture**:

1. **Stage 1**: behavior → outcome (e.g., behaviors → sleep_quality_score)
2. **Stage 2**: outcome + immutable → stress_score
3. **Two-stage CF**: optimize behaviors untuk mencapai outcome target, lalu hitung implied stress reduction

**Implikasi untuk paper**: hasil modest effect (~0.3 poin) bukan kegagalan metodologi, melainkan **realistic estimate** dari pure-behavior intervention. Improvement substantial memerlukan kombinasi behavior change + sleep quality monitoring + adherence support. Two-stage CF architecture diusulkan sebagai **future work**.

## 12.7 GPT Hallucination Risk

Meskipun safety filter regex sudah diterapkan, GPT masih bisa menambahkan klaim yang tidak ada di input (mis. menyebut "stress kerja" padahal data hanya menunjukkan SHAP feature). Mitigasi: instruksi sistem prompt eksplisit "JANGAN menambah fakta", `temperature=0.3` untuk determinism, dan retry mechanism. Untuk paper formal, sebaiknya dilengkapi dengan **automated faithfulness scoring** (e.g., NLI-based entailment check antara CF facts dan GPT output).
