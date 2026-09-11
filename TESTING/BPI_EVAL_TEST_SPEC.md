# BPI EVALUATION TEST SPECIFICATION v1.0
**Document ID:** `SPEC-EVAL-TEST-v1.0`  
**Status:** `PROPOSED / DRAFT FOR REVIEW`  
**Parent Specification:** `BPI Evaluation Specification v1.0 (Locked)`  
**Parent Baseline:** `BPI v1.0 (Immutable)`  

---

## 1. Test Identity & Scope
Dokumen ini menetapkan kerangka pengujian formal untuk memvalidasi kepatuhan (*compliance*) dan determinisme dari Evaluation Layer terhadap spesifikasi yang telah dikunci. Pengujian mencakup validasi metrik metatarget, pencegahan kebocoran data (*data leakage*), isolasi arsitektur (*zero feedback*), dan penanganan kasus ekstrem (*edge cases*).

## 2. Core Testing Principles
Seluruh rangkaian pengujian wajib mematuhi prinsip inti berikut:
* **Determinisme Mutlak:** Eksekusi berulang pada dataset dan spesifikasi yang sama wajib menghasilkan *output* metrik yang identik secara biner/numerik.
* **Zero Data Leakage:** Sistem pengujian harus menolak segala bentuk input yang menggunakan *post-match BPI snapshot*.
* **Read-Only Enforcement:** Pengujian isolasi wajib membuktikan bahwa Evaluation Engine tidak memiliki kemampuan modifikasi terhadap kode core, formula, maupun basis data historis.
* **No Feedback Loop:** Hasil evaluasi tidak boleh memengaruhi *runtime input* dari BPI v1.0.

## 3. Controlled Synthetic Historical Dataset
Untuk memastikan ekspektasi matematis dapat dihitung dan diverifikasi secara presisi, pengujian menggunakan dataset sintetis standar yang terdiri dari 6 fixture uji terkontrol:

| match_id | team_home | team_away | bpi_home_pre | bpi_away_pre | power_gap | actual_goals_home | actual_goals_away | actual_result | fixture_type |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `FX-001` | Tim A | Tim B | 80.00 | 60.00 | 20.00 | 2 | 0 | `H` | Higher-ranked win (Normal) |
| `FX-002` | Tim C | Tim D | 75.00 | 50.00 | 25.00 | 1 | 1 | `D` | Higher-ranked draw (Upset-ish) |
| `FX-003` | Tim E | Tim F | 70.00 | 65.00 | 5.00 | 0 | 2 | `A` | Higher-ranked loss (Upset) |
| `FX-004` | Tim G | Tim H | 60.00 | 60.00 | 0.00 | 1 | 0 | `H` | Equal BPI / Home Win |
| `FX-005` | Tim I | Tim J | 55.00 | 70.00 | 15.00 | 0 | 3 | `A` | Underdog win (Away) |
| `FX-006` | Tim K | Tim L | 85.00 | 45.00 | 40.00 | 4 | 1 | `H` | Massive Gap / Easy Win |

## 4. Expected Metrics (Dataset Uji Terkontrol)
Berdasarkan dataset sintetis di atas (total 6 eligible matches):
* **Higher-Rank Win Cases:** `FX-001` (Team A > B, Home wins), `FX-006` (Team K > L, Home wins) $\rightarrow$ 2 wins. *(Catatan: FX-002 draw, FX-003 higher lost, FX-004 equal, FX-005 higher lost).*
* **Higher-Rank Win Rate Target:** 
  $$\text{Higher-Rank Win Rate} = \frac{2}{6} \approx 33.33\%$$
* **Higher-Rank Non-Loss Rate Target:** (Wins + Draws: `FX-001`, `FX-002`, `FX-006`) $\rightarrow \frac{3}{6} = 50.00\%$
* **Rank Accuracy:** Ketepatan prediksi arah peringkat terhadap hasil akhir.
* **Empirical Gap-Bucket Results:**
  * Gap 0–5 (`FX-003`, `FX-004`): Win rate/performance terukur sesuai data.
  * Gap 10–20 (`FX-005`): Terukur.
  * Gap > 20 (`FX-001`, `FX-002`, `FX-006`): Terukur.

## 5. Edge Cases & Error Handling Tests
Pengujian wajib memvalidasi penanganan kasus batas berikut:
* **EC-01 (Equal BPI / Gap = 0):** Memastikan fixture dengan `power_gap = 0.00` (`FX-004`) diproses tanpa galat pembagian nol (*division by zero*).
* **EC-02 (Single Fixture Dataset):** Memastikan agregasi metrik tetap berjalan normal dengan ukuran dataset $N=1$.
* **EC-03 (Missing Pre-Match BPI):** Sistem harus menolak (*reject*) record jika field `bpi_home_pre` atau `bpi_away_pre` bernilai *null/empty*.
* **EC-04 (Duplicate Match ID):** Sistem mendeteksi dan menolak data duplikat untuk menjaga integritas *append-only*.
* **EC-05 (Negative Goals):** Menolak rekam data yang memiliki nilai gol $< 0$.

## 6. Data Leakage Tests
* **DL-01 (Pre-Match Acceptance):** Memasukkan data dengan *pre-match snapshot* $\rightarrow$ **Expected: ACCEPT**.
* **DL-02 (Post-Match Rejection):** Memasukkan data di mana BPI diambil setelah pertandingan selesai (atau terdeteksi mencakup hasil pertandingan) $\rightarrow$ **Expected: REJECT / RAISE SECURITY ERROR**.

## 7. Isolation & Guardrail Tests
* **ISO-01 (Formula Protection):** Memverifikasi bahwa skrip eksekusi evaluasi tidak memiliki akses tulis ke direktori `CORE/` atau `ENGINE/`.
* **ISO-02 (Historical Tampering Protection):** Memverifikasi bahwa file data historis diperlakukan secara *append-only* (mencegah penimpaan file mentah).
* **ISO-03 (Zero Feedback Loop):** Memverifikasi bahwa fungsi evaluasi tidak menghasilkan file konfigurasi atau *state* yang dibaca kembali oleh BPI v1.0.

## 8. Reproducibility Test
* **REP-01 (Multi-Run Verification):** Menjalankan `BPI_EVAL_TESTS.py` sebanyak 3 kali berturut-turut pada dataset uji yang sama.
  $$\text{Run \#1 Output} == \text{Run \#2 Output} == \text{Run \#3 Output}$$

## 9. Ranking Stability Status
* **Status:** `🟡 PENDING / BLOCKED`
* **Catatan:** Karena formula matematis *Ranking Stability* belum didefinisikan secara resmi, seluruh test case yang berkaitan dengan metrik stabilitas peringkat ditandai sebagai `BLOCKED` dan dieksklusi dari eksekusi test suite v1.0.

## 10. Test Status Rules
Setiap pengujian di dalam test suite harus menghasilkan salah satu status berikut:
* `PASS`: Memenuhi seluruh kriteria ekspektasi secara akurat.
* `FAIL`: Gagal memenuhi ekspektasi matematis atau logika pengaman.
* `BLOCKED`: Ditunda karena dependensi eksternal belum siap (cth: *Ranking Stability*).
* `PENDING`: Belum diimplementasikan.
* `NOT APPLICABLE`: Di luar cakupan skenario pengujian aktif.
