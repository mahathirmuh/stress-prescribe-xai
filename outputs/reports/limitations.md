# Limitations & Threats to Validity

## 12.1 Dataset Sintetis

Dataset Sleep Health & Daily Performance (Kaggle) adalah **data sintetis**, bukan pengukuran riil dari subjek manusia. Korelasi dan pola yang ditemukan mungkin merupakan artefak generator data, bukan fenomena alami.

**Disclaimer**: Penelitian ini adalah **methodological proof-of-concept**, bukan validasi klinis. Generalisasi ke populasi nyata memerlukan validasi pada data klinis.

## 12.2 Asumsi Kausalitas pada Counterfactual

DiCE mengasumsikan **causal stationarity** — perubahan fitur akan menghasilkan perubahan prediksi secara konsisten. Pada data sintetis, asumsi ini belum tentu valid. Rekomendasi intervensi harus dipahami sebagai "kemungkinan", bukan "kepastian". Validasi kausal nyata memerlukan eksperimen prospektif (RCT).

Untuk mitigasi parsial, kami:
- Memisahkan **behavior** (boleh diubah) vs **outcome** (gejala, tidak boleh) vs **immutable**
- Menerapkan `permitted_range` eksplisit per fitur behavior

## 12.3 GenAI Evaluation Scope

Evaluasi GenAI terbatas pada:
- **Struktur output**: JSON valid + key wajib (`summary`, `drivers`, `recommendations`, `encouragement`, `disclaimer`)
- **Safety filter**: regex blocklist untuk kata terlarang (obat, diagnosa, janji pasti, alkohol)

**Tidak dilakukan**: user study, expert panel, atau validasi klinis output GenAI. GenAI diposisikan sebagai **deployment layer** untuk presentasi naratif, bukan kontribusi ilmiah utama. Evaluasi rigor LLM (faithfulness scoring lewat human raters, hallucination benchmark) di luar scope penelitian ini.

## 12.4 Reproducibility Bound

`random_state=42` digunakan konsisten di seluruh pipeline (sampling, split, model). Namun:
- **DiCE** menggunakan `method='random'` — meskipun seed di-set, hasil bisa sedikit bervariasi karena sampling internal
- **GPT** bersifat probabilistik meski `temperature=0.3` — variasi minor antar run masih mungkin terjadi
- **TabNet** sensitif terhadap inisialisasi weight — gunakan multiple seeds untuk publikasi

## 12.5 Sampling Bias

Hasil pada sampel 10k bisa berbeda dari full 100k. Section 13 menjalankan ulang full untuk validasi final.
