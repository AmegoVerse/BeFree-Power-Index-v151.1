# BPI EVALUATION TEST SPECIFICATION v1.0
**Document ID:** `SPEC-EVAL-TEST-v1.0`  
**Status:** `READY FOR FINAL LOCK (POST-REVISION)`  
**Parent Specification:** `BPI Evaluation Specification v1.0 (Locked)`  
**Parent Baseline:** `BPI v1.0 (Immutable)`  

---

## 1. Test Identity & Scope
Dokumen ini menetapkan kerangka pengujian formal untuk memvalidasi kepatuhan (*compliance*) dan determinisme dari Evaluation Layer terhadap spesifikasi yang telah dikunci. Pengujian mencakup validasi metrik, pencegahan kebocoran data (*data leakage*), isolasi arsitektur (*zero feedback*), dan penanganan kasus ekstrem (*edge cases*).

## 2. Core Testing Principles
Seluruh rangkaian pengujian wajib mematuhi prinsip inti berikut:
* **Determinisme Mutlak:** Eksekusi berulang pada dataset dan spesifikasi yang sama wajib menghasilkan *output* metrik yang identik secara biner/numerik.
* **Zero Data Leakage:** Sistem pengujian harus menolak segala bentuk input yang menggunakan *post-match BPI snapshot*.
* **Read-Only Enforcement:** Pengujian isolasi wajib membuktikan bahwa Evaluation Engine tidak memiliki kapabilitas modifikasi terhadap kode core, formula, maupun basis data historis.
* **No Feedback Loop:** Hasil evaluasi tidak boleh memengaruhi *runtime input* dari BPI v1.0.

## 3. Controlled Synthetic Historical Dataset & Gap Buckets
Untuk memastikan ekspektasi matematis dapat dihitung dan diverifikasi secara presisi, pengujian menggunakan dataset sintetis standar yang terdiri dari 6 fixture uji terkontrol dengan interval *gap bucket* non-tumpang tindih ($0 \le \text{gap} < 10$, $10 \le \text{gap} < 20$, $20 \le \text{gap} < 30$, $\text{gap} \ge 30$):

| match_id | team_home | team_away | bpi_home_pre | bpi_away_pre | power_gap | actual_goals_home | actual_goals_away | actual_result | gap_bucket | fixture_type |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `FX-003` | Tim E | Tim F | 70.00 | 65.00 | 5.00 | 0 | 2 | `A` | $0 - <10$ | Higher-ranked loss (Upset-ish) |
| `FX-004` | Tim G | Tim H | 60.00 | 60.00 | 0.00 | 1 | 0 | `H` | $0 - <10$ | Equal BPI / Home Win |
| `FX-005` | Tim I | Tim J | 55.00 | 70.00 | 15.00 | 0 | 3 | `A` | $10 - <20$ | Underdog win (Away) |
| `FX-001` | Tim A | Tim B | 80.00 | 60.00 | 20.00 | 2 | 0 | `H` | $20 - <30$ | Higher-ranked win (Normal) |
| `FX-002` | Tim C | Tim D | 75.00 | 50.00 | 25.00 | 1 | 1 | `D` | $20 - <30$ | Higher-ranked draw |
| `FX-006` | Tim K | Tim L | 85.00 | 45.00 | 40.00 | 4 | 1 | `H` | $\ge 30$ | Massive Gap / Easy Win |

## 4. Expected Metrics (Dataset Uji Terkontrol)
Berdasarkan dataset sintetis di atas:
* **Total Fixtures:** 6
* **Equal BPI Fixture (`FX-004`):** 1 fixture (dikecualikan dari metrik *higher-rank* karena tidak ada tim dengan ranking lebih tinggi).
* **Eligible Higher-Rank Fixtures ($N$):** 5 fixture (`FX-001`, `FX-002`, `FX-003`, `FX-005`, `FX-006`).
* **Higher-Rank Wins:** 2 (`FX-001`, `FX-006`).
* **Higher-Rank Win Rate Target:** 
  $$\text{Higher-Rank Win Rate} = \frac{2}{5} = 40.00\%$$
* **Higher-Rank Non-Losses (Wins + Draws):** 3 (`FX-001`, `FX-002`, `FX-006`).
* **Higher-Rank Non-Loss Rate Target:** 
  $$\text{Higher-Rank Non-Loss Rate} = \frac{3}{5} = 60.00\%$$
* **Rank Accuracy Definition:** 
  * BPI Berbeda & Higher BPI Menang $\rightarrow$ Correct
  * BPI Berbeda & Higher BPI Kalah $\rightarrow$ Incorrect
  * BPI Berbeda & Seri $\rightarrow$ Neutral / Not Scored
  * BPI Sama ($\text{gap} = 0$) $\rightarrow$ Not Applicable (`N/A`)
* **Upset Rate Status:** `PENDING` (Threshold persentase/gap upset belum didefinisikan secara formal dalam spesifikasi v1.0).

## 5. Edge Cases & Boundary Handling Tests
Pengujian wajib memvalidasi penanganan kasus batas berikut:
* **EC-01 (Equal BPI / Gap = 0):** Memastikan fixture dengan `power_gap = 0.00` (`FX-004`) diproses tanpa galat pembagian nol (*division by zero* dan dikecualikan dari metrik ranking).
* **EC-02 (Single Fixture Dataset):** Memastikan agregasi metrik tetap berjalan normal dengan ukuran dataset $N=1$.
* **EC-03 (Missing Pre-Match BPI):** Sistem menolak (*reject*) record jika field pre-match BPI bernilai *null/empty*.
* **EC-04 (Duplicate Match ID):** Sistem mendeteksi dan menolak data duplikat untuk menjaga integritas *append-only*.
* *(Catatan Validasi Nilai Negatif seperti gol $<0$ ditangani oleh Historical Data Validation spec, bukan Evaluation Engine).*

## 6. Data Leakage Tests
* **DL-01 (Pre-Match Acceptance):** Memasukkan data dengan *pre-match snapshot* sah $\rightarrow$ **Expected: ACCEPT**.
* **DL-02 (Post-Match Rejection):** Memasukkan data di mana BPI diambil setelah pertandingan selesai / terdeteksi mencakup hasil pertandingan $\rightarrow$ **Expected: REJECT / RAISE SECURITY ERROR**.

## 7. Isolation & Guardrail Tests
* **ISO-01 (Resource Protection Contract):** Kontrak pengujian menyatakan bahwa skrip/engine evaluasi dilarang keras memiliki jalur tulis ke direktori `CORE/` atau berkas sumber historis mentah. Percobaan write operation ke resource terlindungi harus menghasilkan pengecualian (*failure/error*).
* **ISO-02 (Zero Feedback Loop):** Memverifikasi bahwa hasil evaluasi tidak mengekspor file atau state apa pun yang dapat dibaca kembali sebagai input oleh BPI v1.0.

## 8. Reproducibility Test
* **REP-01 (Multi-Run Verification):** Menjalankan rangkaian test evaluation sebanyak 3 kali berturut-turut pada dataset uji yang sama.
  $$\text{Run \#1 Output} == \text{Run \#2 Output} == \text{Run \#3 Output}$$

## 9. Pending / Blocked Metrics Status
* **Ranking Stability:** `PENDING` (Formula matematis belum didefinisikan).
* **Upset Rate:** `PENDING` (Threshold belum didefinisikan).
* Kedua metrik di atas dieksklusi dari assert suite utama versi v1.0.

## 10. Test Status Rules
Setiap pengujian di dalam test suite harus menghasilkan salah satu status berikut:
* `PASS`: Memenuhi seluruh kriteria ekspektasi secara akurat.
* `FAIL`: Gagal memenuhi ekspektasi matematis atau logika pengaman.
* `BLOCKED`: Ditunda karena dependensi eksternal belum siap.
* `PENDING`: Belum diimplementasikan / menunggu definisi formal.
* `NOT APPLICABLE`: Di luar cakupan skenario pengujian aktif.
