# BPI HISTORICAL DATA SPECIFICATION v1.0
**Document ID:** `SPEC-HIST-v1.0`  
**Status:** `PROPOSED / DRAFT FOR REVIEW`  
**Parent Baseline:** `BPI v1.0 (Immutable) & Evaluation Spec v1.0 (Locked)`  

---

## 1. Tujuan Historical Data Layer
Historical Data Layer bertujuan untuk menyediakan repositori data historis yang terstandarisasi, permanen, dan *tamper-evident* untuk mendukung **Evaluation Layer**. Lapisan ini menyimpan rekam jejak pertandingan resmi beserta *pre-match BPI snapshot* secara presisi guna memastikan setiap proses evaluasi dapat direproduksi secara persis (*fully reproducible*) kapan pun dieksekusi ulang.

## 2. Prinsip Penyimpanan Utama
* **Append-Only Policy:** Data historis bersifat satu arah (*append-only*). Rekor pertandingan yang telah tercatat dan dikunci **dilarang keras** untuk dihapus, diubah, atau ditimpa (*overwritten*), guna menjaga integritas analisis lintas waktu.
* **Zero Data Leakage:** Setiap record wajib mengunci nilai BPI pra-pertandingan (*pre-match snapshot*) yang diambil tepat sebelum *kick-off*, memastikan tidak ada kontaminasi dari kalkulasi BPI pasca-pertandingan.
* **Deterministic Schema:** Setiap baris data harus memuat atribut struktural yang seragam agar dapat langsung dibaca oleh Evaluation Engine tanpa ambiguitas tipe data.

## 3. Struktur Direktori & Format Berkas
* **Direktori Utama:** `/HISTORICAL/`
* **Format Penyimpanan:** 
  * Format teks terstruktur berbasis baris (misalnya format JSON Lines (`.jsonl`) atau CSV terstandarisasi dengan pemisah koma) yang ramah kontrol versi (*version-control friendly*).
  * Pengelompokan berkas dapat dibagi berdasarkan musim kompetisi atau tahun kalender (contoh: `season_2025_2026.jsonl`).

## 4. Skema Data Wajib (Mandatory Record Schema)
Setiap record data dalam Historical Dataset wajib memuat kolom-kolom berikut secara lengkap:

| Nama Field | Tipe Data | Deskripsi / Keterangan |
| :--- | :--- | :--- |
| `match_id` | String | Identifikasi unik global untuk fixture (contoh: `COMP-2026-0012`). |
| `match_date` | Timestamp (ISO 8601) | Tanggal dan waktu aktual pertandingan dimulai. |
| `competition` | String | Nama liga atau kompetisi (contoh: `Eredivisie`, `La Liga`). |
| `team_home` | String | Nama kanonikal tim kandang. |
| `team_away` | String | Nama kanonikal tim tandang. |
| `bpi_home_pre_match` | Float (2 desimal) | Nilai BPI tim kandang tepat sebelum pertandingan dimulai. |
| `bpi_away_pre_match` | Float (2 desimal) | Nilai BPI tim tandang tepat sebelum pertandingan dimulai. |
| `power_gap` | Float (2 desimal) | Selisih mutlak: $|\text{bpi\_home\_pre\_match} - \text{bpi\_away\_pre\_match}|$. |
| `actual_goals_home` | Integer | Jumlah gol akhir tim kandang. |
| `actual_goals_away` | Integer | Jumlah gol akhir tim tandang. |
| `actual_result` | Enum (`H`, `D`, `A`) | Hasil akhir diskrit (`H` = Home win, `D` = Draw, `A` = Away win). |
| `snapshot_timestamp`| Timestamp (ISO 8601) | Waktu saat *pre-match BPI snapshot* dikunci ke sistem historis. |

## 5. Validasi Integritas Data (Data Integrity Checks)
Sebelum sebuah record historis dimasukkan ke dalam dataset utama, sistem harus memvalidasi:
1. **Validitas Tim:** Nama tim terdaftar secara sah di dalam master data BPI v1.0.
2. **Ketiadaan Nilai Kosong (Null Check):** Seluruh field wajib (*mandatory fields*) tidak boleh bernilai kosong (`null` atau *empty*).
3. **Kesesuaian Skor:** Nilai gol harus berupa bilangan bulat non-negatif ($\ge 0$).
4. **Konsistensi Hasil:** Nilai `actual_result` harus selaras secara matematis dengan perbandingan `actual_goals_home` dan `actual_goals_away`.

## 6. Isolasi & Hubungan dengan Lapisan Lain
* **Hubungan dengan BPI v1.0:** Lapisan historis hanya menerima snapshot keluaran dari BPI v1.0; ia tidak memiliki hak untuk memodifikasi formula dasar engine.
* **Hubungan dengan Evaluation Layer:** Historical Data Layer bertindak sebagai sumber data utama (*read source*) bagi Evaluation Engine untuk menghitung metrik performa.
