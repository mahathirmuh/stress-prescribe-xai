# Explainable Machine Learning with Counterfactual Analysis and GenAI-based Naturalization for Stress Prediction and Intervention Using Sleep and Lifestyle Data

## 1. Pendahuluan

Stres merupakan salah satu isu penting dalam kehidupan modern. Tingkat stres seseorang dapat dipengaruhi oleh berbagai faktor, seperti tekanan pekerjaan, pola tidur, aktivitas fisik, kondisi kesehatan, serta kebiasaan digital, termasuk penggunaan layar sebelum tidur. Seiring meningkatnya ketersediaan data gaya hidup dan kesehatan, pendekatan machine learning dapat digunakan untuk memprediksi tingkat stres berdasarkan pola-pola yang terdapat dalam data.

Namun, banyak model prediksi stres hanya berfokus pada akurasi prediksi tanpa memberikan penjelasan yang cukup mengenai faktor-faktor yang memengaruhi hasil prediksi tersebut. Model machine learning yang kompleks, seperti ensemble model dan deep learning, memang mampu menghasilkan performa prediksi yang baik, tetapi sering kali bersifat black-box. Kondisi ini menjadi tantangan, khususnya ketika hasil prediksi digunakan untuk mendukung pengambilan keputusan atau rekomendasi intervensi.

Oleh karena itu, penelitian ini mengembangkan pendekatan explainable dan actionable machine learning untuk memprediksi tingkat stres. Selain membangun model regresi untuk memprediksi `stress_score`, penelitian ini juga menggunakan metode Explainable AI, khususnya SHAP, untuk menjelaskan kontribusi fitur terhadap prediksi. Selanjutnya, pendekatan counterfactual analysis digunakan untuk menghasilkan rekomendasi perubahan gaya hidup yang lebih konkret dan dapat ditindaklanjuti.

Meskipun SHAP dan counterfactual analysis sudah memberikan informasi yang lebih kaya dibandingkan prediksi tunggal, output keduanya tetap bersifat teknis dan numerik sehingga sulit dipahami oleh pengguna awam. Untuk mengatasi keterbatasan tersebut, penelitian ini menambahkan lapisan naturalisasi menggunakan Generative AI (GenAI), khususnya model GPT, untuk mengubah hasil counterfactual menjadi narasi rekomendasi sistem pakar yang empatik, kontekstual, dan mudah dipahami.

## 2. Rumusan Masalah

Berdasarkan latar belakang tersebut, rumusan masalah dalam penelitian ini adalah sebagai berikut:

1. Bagaimana membangun model machine learning yang mampu memprediksi `stress_score` berdasarkan data tidur, gaya hidup, kesehatan, dan aktivitas harian?
2. Faktor apa saja yang paling berpengaruh terhadap prediksi tingkat stres berdasarkan hasil Explainable AI?
3. Bagaimana pendekatan counterfactual analysis dapat digunakan untuk memberikan rekomendasi intervensi yang spesifik dan realistis bagi individu?
4. Bagaimana perbandingan performa model CatBoost, Random Forest, dan TabNet dalam memprediksi tingkat stres?
5. Bagaimana hasil counterfactual dapat dinaturalisasi menjadi narasi rekomendasi sistem pakar yang mudah dipahami pengguna awam menggunakan GenAI?

## 3. Tujuan Penelitian

Penelitian ini bertujuan untuk:

1. Membangun model regresi untuk memprediksi `stress_score`.
2. Membandingkan performa beberapa model machine learning, yaitu CatBoost Regressor, Random Forest Regressor, dan TabNet Regressor.
3. Menggunakan SHAP untuk menjelaskan faktor-faktor yang paling berpengaruh terhadap prediksi stres.
4. Mengembangkan pendekatan counterfactual analysis untuk menghasilkan rekomendasi intervensi yang dapat ditindaklanjuti.
5. Menyusun insight individual untuk kasus stres rendah, sedang, dan tinggi.
6. Mengintegrasikan GenAI (GPT) untuk menaturalisasi hasil counterfactual menjadi narasi rekomendasi sistem pakar yang empatik dan kontekstual.

## 4. Gap Penelitian Sebelumnya

Penelitian sebelumnya terkait prediksi stres dan interpretabilitas model umumnya masih berfokus pada pemahaman pola global dan performa prediksi. Beberapa penelitian telah menggunakan metode interpretabilitas seperti SHAP, attention scores, dan box plots. Namun, output yang dihasilkan masih bersifat teknis sehingga membutuhkan pemahaman machine learning untuk dapat diinterpretasikan secara tepat.

Selain itu, penelitian sebelumnya belum banyak mengimplementasikan counterfactual analysis sebagai bagian dari proses rekomendasi intervensi. Meskipun pendekatan counterfactual sering disebut memiliki potensi untuk mendukung pengambilan keputusan, implementasinya dalam konteks prediksi stres masih terbatas.

Penelitian sebelumnya juga lebih banyak menampilkan pola global, misalnya hubungan antara fitur tertentu dengan arousal atau stres, tetapi belum memberikan penjelasan dan rekomendasi yang spesifik untuk individu tertentu. Dengan demikian, masih terdapat peluang untuk mengembangkan sistem yang tidak hanya menjelaskan prediksi, tetapi juga memberikan rekomendasi perubahan yang lebih personal dan actionable.

## 5. Unsur Keterbaruan Penelitian

Penelitian ini memiliki beberapa unsur keterbaruan sebagai berikut:

### 5.1 Prescriptive Approach

Penelitian ini tidak hanya berfokus pada prediksi tingkat stres dan penjelasan faktor penyebabnya, tetapi juga menyediakan jalur intervensi konkret melalui counterfactual explanations. Dengan pendekatan ini, model dapat menunjukkan perubahan minimal pada fitur tertentu yang berpotensi menurunkan prediksi tingkat stres.

Untuk menjamin **causal validity** rekomendasi, counterfactual analysis direstrik hanya pada **behavior features** (durasi tidur, screen time sebelum tidur, konsumsi kafein, aktivitas fisik, dll.) — *manipulable causes* yang dapat diubah pengguna secara langsung. Fitur *outcome* fisiologis (sleep quality, REM percentage, heart rate, dll.) dan fitur *immutable* (umur, gender, pekerjaan, dll.) di-lock dan tidak boleh diubah CF. Pendekatan ini menghasilkan rekomendasi yang **actionable secara causally honest**, meskipun magnitudo perubahan prediksi yang dapat dicapai lebih modest dibandingkan jika outcomes diizinkan berubah (lihat Section 12.6).

### 5.2 Arsitektur Hybrid

Penelitian ini membandingkan model berbasis pohon konvensional, yaitu CatBoost dan Random Forest, dengan model deep learning khusus data tabular, yaitu TabNet. Perbandingan ini bertujuan untuk mengetahui model mana yang paling sesuai untuk prediksi stres berbasis data tidur dan gaya hidup.

### 5.3 Personalisasi Intervensi

Penelitian ini mengintegrasikan SHAP dan counterfactual analysis untuk memberikan rekomendasi yang tidak hanya didasarkan pada pola global, tetapi juga disesuaikan dengan kondisi individu. Dengan demikian, hasil penelitian diharapkan dapat menghasilkan insight yang lebih personal dan realistis.

### 5.4 Naturalisasi Rekomendasi dengan GenAI

Penelitian ini menambahkan lapisan naturalisasi berbasis Generative AI (GPT) yang mengubah hasil counterfactual yang masih berupa angka dan nama fitur teknis menjadi narasi rekomendasi sistem pakar dalam bahasa awam. Dengan demikian, rekomendasi yang dihasilkan tidak hanya akurat dan personal, tetapi juga mudah dipahami dan lebih siap untuk ditindaklanjuti oleh pengguna non-ahli. Pendekatan ini menjembatani gap antara output model machine learning yang teknis dengan kebutuhan komunikasi yang manusiawi dan empatik.

## 6. Dataset

Dataset yang digunakan dalam penelitian ini adalah **Sleep Health & Daily Performance Dataset** dari Kaggle. Dataset ini berisi data sintetis mengenai pola tidur, gaya hidup, kondisi kesehatan, dan performa harian.

| Informasi | Keterangan |
|---|---|
| Jumlah data | 100.000 baris |
| Jumlah kolom awal | 32 kolom |
| Target utama | `stress_score` dengan rentang 1.0–10.0 |
| Jenis task | Supervised Learning — Regression |
| Missing value | Tidak ada |

Variabel dalam dataset meliputi:

`person_id`, `age`, `gender`, `occupation`, `bmi`, `country`, `sleep_duration_hrs`, `sleep_quality_score`, `rem_percentage`, `deep_sleep_percentage`, `sleep_latency_mins`, `wake_episodes_per_night`, `caffeine_mg_before_bed`, `alcohol_units_before_bed`, `screen_time_before_bed_mins`, `exercise_day`, `steps_that_day`, `nap_duration_mins`, `stress_score`, `work_hours_that_day`, `chronotype`, `mental_health_condition`, `heart_rate_resting_bpm`, `sleep_aid_used`, `shift_work`, `room_temperature_celsius`, `weekend_sleep_diff_hrs`, `season`, `day_type`, `cognitive_performance_score`, `sleep_disorder_risk`, dan `felt_rested`.

## 7. Variabel dan Fitur Penelitian

Fitur yang digunakan dalam penelitian dikelompokkan ke dalam beberapa kategori utama.

| Kelompok Fitur | Contoh Fitur |
|---|---|
| Demografi | `age`, `gender`, `occupation`, `bmi`, `country` |
| Tidur utama | `sleep_duration_hrs`, `sleep_quality_score`, `rem_percentage`, `deep_sleep_percentage` |
| Kebiasaan sebelum tidur | `caffeine_mg_before_bed`, `screen_time_before_bed_mins`, `alcohol_units_before_bed` |
| Aktivitas dan kesehatan | `exercise_day`, `steps_that_day`, `heart_rate_resting_bpm`, `shift_work` |
| Pekerjaan | `work_hours_that_day` |
| Lingkungan | `room_temperature_celsius`, `season`, `day_type`, `chronotype` |

Beberapa fitur dihapus untuk mencegah data leakage, yaitu:

| Fitur | Alasan Penghapusan |
|---|---|
| `person_id` | Tidak informatif |
| `cognitive_performance_score` | Co-outcome atau hasil, bukan prediktor |
| `sleep_disorder_risk` | Co-outcome atau label kondisi lain |
| `felt_rested` | Sangat dekat dengan kondisi hasil akhir |

**Catatan tentang outcome features**: Fitur seperti `sleep_quality_score`, `rem_percentage`, `wake_episodes_per_night`, `sleep_latency_mins`, `deep_sleep_percentage`, dan `heart_rate_resting_bpm` **tetap digunakan sebagai prediktor** karena memang predictive (mis. `sleep_quality_score` r = -0.639). Namun, fitur-fitur ini diklasifikasikan sebagai *outcomes* (gejala fisiologis, bukan behavior yang dapat dimanipulasi langsung) dan akan **di-lock di tahap counterfactual analysis** (Section 9) — DiCE hanya akan mengubah *behavior features*. Pendekatan ini memberi keseimbangan antara akurasi prediksi (R² tetap tinggi) dan causal soundness rekomendasi intervensi.

## 8. Eksplorasi Awal Dataset

Eksplorasi awal dataset dilakukan untuk memahami distribusi target dan hubungan antar fitur numerik. Berdasarkan hasil EDA, distribusi `stress_score` pada 100.000 sampel mendekati distribusi normal dengan nilai rata-rata 5.73 dan standar deviasi 1.62.

Analisis korelasi numerik menunjukkan bahwa `sleep_quality_score` memiliki korelasi negatif terkuat dengan `stress_score`, yaitu sebesar -0.639. Selain itu, `sleep_duration_hrs` juga memiliki korelasi negatif yang cukup kuat dengan `stress_score`, yaitu sebesar -0.500. Hal ini menunjukkan bahwa kualitas tidur dan durasi tidur yang lebih baik cenderung berkaitan dengan tingkat stres yang lebih rendah.

Beberapa fitur lain juga menunjukkan hubungan dengan `stress_score`, seperti `work_hours_that_day`, `wake_episodes_per_night`, `sleep_latency_mins`, dan `shift_work`. Fitur-fitur tersebut dapat menjadi indikator penting dalam pemodelan prediksi stres.

## 9. Metodologi Penelitian

Penelitian ini menggunakan pendekatan supervised learning dengan task regresi. Target yang diprediksi adalah `stress_score`. Secara umum, tahapan penelitian meliputi eksplorasi data, preprocessing, pembagian data, pelatihan model, evaluasi model, interpretasi model, counterfactual analysis, dan penyusunan rekomendasi intervensi.

### 9.1 Eksplorasi Data

Tahap eksplorasi dilakukan untuk memahami struktur dataset, distribusi target, statistik deskriptif, dan hubungan antar fitur. Visualisasi yang digunakan meliputi histogram, box plot, dan heatmap korelasi.

### 9.2 Preprocessing

Preprocessing dilakukan dalam beberapa tahap. Pertama, dilakukan penghapusan fitur leakage yang terlalu dekat dengan target (`person_id`, `cognitive_performance_score`, `sleep_disorder_risk`, `felt_rested`). Outcome features fisiologis (`sleep_quality_score`, `rem_percentage`, `wake_episodes_per_night`, `sleep_latency_mins`, `deep_sleep_percentage`, `heart_rate_resting_bpm`) **tetap digunakan sebagai prediktor** karena memang predictive terhadap stress; causal soundness rekomendasi intervensi dijaga di tahap counterfactual (Section 9.6) dengan me-lock outcomes dan hanya mengubah behavior features.

Setelah seleksi fitur, dilakukan encoding pada variabel kategorikal serta normalisasi (StandardScaler) untuk model yang membutuhkan input numerik tertentu (Random Forest dan TabNet). Dua versi data disiapkan: **Versi A** dengan kategorikal mentah untuk CatBoost yang native-supports cat_features, dan **Versi B** dengan encoded + scaled untuk RF/TabNet. Final feature count untuk pemodelan adalah **27 fitur input** (32 kolom awal − 1 target − 4 leakage).

### 9.3 Pembagian Data

Dataset dibagi menjadi tiga bagian:

| Data | Proporsi |
|---|---|
| Training set | 70% |
| Validation set | 15% |
| Test set | 15% |

Pembagian ini dilakukan untuk memastikan model dapat dilatih, divalidasi, dan diuji secara objektif.

### 9.4 Model yang Digunakan

Model yang digunakan dalam penelitian ini meliputi:

1. **CatBoost Regressor**  
   Model gradient boosting yang efektif untuk data tabular dan mampu menangani fitur kategorikal dengan baik.

2. **Random Forest Regressor**  
   Model ensemble berbasis decision tree yang digunakan sebagai pembanding karena stabil dan mudah diinterpretasikan secara relatif.

3. **TabNet Regressor**  
   Model deep learning untuk data tabular yang menggunakan mekanisme attention untuk memilih fitur yang relevan pada setiap tahap keputusan.

### 9.5 Explainable AI dengan SHAP

SHAP digunakan untuk menjelaskan kontribusi fitur terhadap prediksi model. Analisis dilakukan pada dua level:

1. **Global explanation**, untuk mengetahui fitur-fitur yang paling berpengaruh secara keseluruhan.
2. **Local explanation**, untuk menjelaskan prediksi pada individu tertentu, misalnya individu dengan tingkat stres tinggi, sedang, atau rendah.

### 9.6 Counterfactual Analysis

Counterfactual analysis digunakan untuk mengidentifikasi perubahan minimal pada fitur tertentu yang dapat menurunkan prediksi tingkat stres. Pendekatan ini bertujuan menghasilkan rekomendasi yang lebih actionable.

Contoh bentuk rekomendasi counterfactual adalah:

- Meningkatkan `sleep_duration_hrs`.
- Meningkatkan `sleep_quality_score`.
- Mengurangi `screen_time_before_bed_mins`.
- Mengurangi `caffeine_mg_before_bed`.
- Mengurangi `work_hours_that_day` apabila realistis.
- Mengurangi `wake_episodes_per_night` melalui perbaikan kebiasaan tidur.

### 9.7 Naturalisasi Rekomendasi dengan GenAI

Output dari SHAP dan counterfactual analysis kemudian digunakan sebagai input untuk model Generative AI (GPT) yang berperan sebagai konselor kesehatan tidur dan manajemen stres. Tahapan ini meliputi:

1. **Penyusunan prompt sistem pakar**: peran model didefinisikan sebagai konselor yang memberi saran berbasis data, dengan aturan ketat untuk hanya menggunakan fakta dari input (tidak berhalusinasi) dan menggunakan bahasa Indonesia yang mudah dipahami.
2. **Konstruksi prompt pengguna**: prompt dibangun secara terstruktur dari profil individu, prediksi `stress_score`, top-5 kontribusi fitur dari SHAP, dan hasil counterfactual (fitur yang diubah beserta nilai sebelum dan sesudah).
3. **Pemanggilan API dengan output JSON terstruktur**: model GPT dipanggil dengan parameter temperatur rendah untuk konsistensi, dan output dipaksa dalam format JSON yang memuat ringkasan kondisi, driver utama, langkah-langkah konkret, serta kalimat motivasi.
4. **Integrasi pipeline**: narasi yang dihasilkan disajikan bersama hasil SHAP dan counterfactual sebagai satu paket rekomendasi yang lengkap, mulai dari prediksi hingga saran yang siap dibaca pengguna.

Pengujian dan evaluasi terhadap output GenAI akan dibahas pada iterasi penelitian berikutnya.

## 10. Teknologi yang Digunakan

| Tahapan | Teknologi |
|---|---|
| Exploration | Pandas, NumPy, Matplotlib, Seaborn |
| Preprocessing | Scikit-learn |
| Model Regresi | CatBoost, Random Forest, TabNet |
| Explainable AI | SHAP TreeExplainer |
| Counterfactual | DiCE / Custom Python Scenario |
| GenAI Naturalisasi | OpenAI Python SDK, GPT-4o-mini, python-dotenv |

## 11. Skenario Evaluasi

Evaluasi dilakukan untuk mengukur performa model, stabilitas hasil, validitas interpretasi, dan kelayakan rekomendasi counterfactual.

| Skenario | Evaluasi |
|---|---|
| Model Performance | R², RMSE, MAE |
| Model Comparison | CatBoost vs Random Forest vs TabNet |
| Cross-validation | Stabilitas R² melalui 5-Fold Cross Validation |
| SHAP Sanity Check | Konsistensi nilai SHAP |
| Domain Validity | Directional check, misalnya Sleep Quality ↑ → Stress ↓ |
| Counterfactual Validity | Perbandingan prediksi sebelum dan sesudah perubahan |
| Plausibility | Pemeriksaan apakah perubahan yang disarankan realistis |

## 12. Output yang Diharapkan

Output yang diharapkan dari penelitian ini adalah:

1. Model regresi dengan performa prediksi yang baik untuk memprediksi `stress_score`.
2. Perbandingan performa antara CatBoost, Random Forest, dan TabNet.
3. Visualisasi Explainable AI menggunakan SHAP untuk menjelaskan fitur yang paling berpengaruh.
4. Penjelasan individual untuk kasus stres tinggi, sedang, dan rendah.
5. Rekomendasi intervensi gaya hidup yang actionable dan berbasis data.
6. Narasi rekomendasi sistem pakar berbasis GenAI yang empatik dan siap dipahami pengguna awam.
7. Framework prediksi stres yang tidak hanya akurat, tetapi juga explainable, prescriptive, dan naturalized.

## 13. Kesimpulan Sementara

Penelitian ini dirancang untuk membangun model prediksi stres berbasis data tidur, gaya hidup, kesehatan, dan aktivitas harian. Berbeda dari pendekatan prediksi konvensional, penelitian ini menggabungkan model machine learning dengan Explainable AI dan counterfactual analysis. Dengan demikian, hasil penelitian diharapkan tidak hanya mampu memprediksi tingkat stres, tetapi juga menjelaskan penyebab prediksi dan memberikan rekomendasi intervensi yang lebih personal, realistis, dan dapat ditindaklanjuti.