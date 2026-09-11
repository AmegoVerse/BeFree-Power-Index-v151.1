# BeFree Power Index v151.1
# BPI DATA SPECIFICATION

**Document:** BPI_DATA_SPEC.md  
**Project:** BeFree Power Index v151.1  
**Data Layer:** BPI Data Specification  
**Status:** Official Data Specification  
**BPI v1.0 Formula:** LOCKED  
**BPI v2.0 Formula:** NOT YET LOCKED  

---

# 1. PURPOSE

Dokumen ini mendefinisikan standar data yang digunakan oleh BeFree Power Index™.

Tujuan utama:

- Menentukan data apa yang boleh digunakan.
- Menentukan struktur data yang harus digunakan.
- Menentukan aturan validasi data.
- Menjamin konsistensi data antar tim.
- Menjamin reproducibility hasil BPI.
- Mencegah penggunaan data yang tidak konsisten.
- Menjadi dasar untuk Calculation Engine.
- Menjadi dasar untuk Historical Database.
- Menjadi dasar untuk Evaluation Engine.

Data Specification ini merupakan bagian dari Source of Truth BeFree Power Index™.

---

# 2. DATA PRINCIPLES

Semua data BPI harus memenuhi prinsip berikut:

1. Accurate
2. Complete
3. Consistent
4. Traceable
5. Timestamped
6. Versioned
7. Reproducible

Data tidak boleh dimanipulasi untuk menghasilkan ranking atau prediksi yang diinginkan.

BPI harus mengikuti data, bukan data mengikuti hasil BPI.

---

# 3. DATA SNAPSHOT

BPI menggunakan konsep Data Snapshot.

Satu Data Snapshot adalah kumpulan data yang mewakili kondisi kompetisi pada satu waktu tertentu.

Setiap snapshot wajib memiliki:

- Snapshot ID
- Snapshot Date
- Snapshot Time
- Competition
- Season
- Data Source
- Extraction Time
- Data Specification Version
- BPI Engine Version
- Data Quality Status

Contoh:

Snapshot ID:
`EPL-2026-2027-2026-09-11-001`

Competition:
`English Premier League`

Season:
`2026/2027`

Snapshot Date:
`2026-09-11`

---

# 4. DATA CONSISTENCY

Semua tim dalam satu perhitungan BPI harus berasal dari snapshot yang sama.

Tidak diperbolehkan:

- menggunakan data Manchester United dari tanggal A
- menggunakan data Liverpool dari tanggal B
- menggunakan data Arsenal dari tanggal C

untuk menghasilkan satu ranking BPI.

Semua tim harus berasal dari Data Snapshot yang sama.

---

# 5. BPI v1.0 REQUIRED DATA

BPI v1.0 membutuhkan data berikut:

| Field | Description | Required |
|---|---|---|
| Team | Nama tim | YES |
| Played | Jumlah pertandingan | YES |
| Wins | Jumlah kemenangan | YES |
| Draws | Jumlah seri | YES |
| Losses | Jumlah kekalahan | YES |
| GF | Goals For | YES |
| GA | Goals Against | YES |
| Points | Jumlah poin | YES |
| Recent Form | Nilai numerik Recent Form | YES |

---

# 6. BPI v1.0 RAW DATA DEFINITIONS

## 6.1 Team

Nama resmi tim yang digunakan dalam kompetisi.

Contoh:

`Manchester United`

`Liverpool`

`Arsenal`

Team name harus konsisten di seluruh database.

Perubahan nama tim harus dicatat dalam historical data mapping.

---

## 6.2 Played

Jumlah pertandingan yang telah dimainkan.

Notation:

`P`

Constraint:

`P > 0`

---

## 6.3 Wins

Jumlah pertandingan yang dimenangkan.

Notation:

`W`

Constraint:

`W >= 0`

---

## 6.4 Draws

Jumlah pertandingan seri.

Notation:

`D`

Constraint:

`D >= 0`

---

## 6.5 Losses

Jumlah pertandingan yang kalah.

Notation:

`L`

Constraint:

`L >= 0`

Relationship:

`W + D + L = P`

---

## 6.6 Goals For

Jumlah gol yang dicetak tim.

Notation:

`GF`

Constraint:

`GF >= 0`

---

## 6.7 Goals Against

Jumlah gol yang diterima tim.

Notation:

`GA`

Constraint:

`GA >= 0`

---

## 6.8 Points

Jumlah poin resmi dalam kompetisi.

Untuk kompetisi dengan sistem standar:

`Points = (Wins × 3) + Draws`

Data harus diverifikasi terhadap klasemen resmi.

---

# 7. RECENT FORM

Recent Form merupakan salah satu komponen resmi BPI v1.0 dengan bobot:

`15%`

Namun, metode encoding numerik Recent Form belum dianggap terkunci sampai metode tersebut disetujui secara eksplisit.

Status:

**PENDING FORM ENCODING LOCK**

Artinya:

- Recent Form wajib tersedia.
- Recent Form harus berupa nilai numerik.
- Encoding harus reproducible.
- Encoding tidak boleh berubah antar snapshot tanpa versioning.
- Metode final harus disetujui sebelum Calculation Engine produksi dianggap final.

Tidak boleh membuat metode encoding secara diam-diam.

---

# 8. PROPOSED RECENT FORM ENCODING

Sebagai kandidat untuk pengujian, sistem dapat menggunakan 5 pertandingan terakhir:

Win = 3 poin  
Draw = 1 poin  
Loss = 0 poin

Maximum:

`15`

Candidate Recent Form:

`RecentForm = PointsLast5 / 15 × 100`

Contoh:

`W-W-D-L-W`

= 3 + 3 + 1 + 0 + 3

= 10

Recent Form:

`10 / 15 × 100 = 66.67`

IMPORTANT:

Metode ini adalah **PROPOSED METHOD**.

Metode ini belum menjadi bagian formula resmi yang terkunci sampai disetujui dan dimasukkan sebagai encoding resmi.

---

# 9. DERIVED DATA

Data berikut dihitung oleh Calculation Engine dan bukan input manual utama.

## 9.1 Points Per Game

`PPG = Points / Played`

## 9.2 Goal Difference

`GD = GF - GA`

## 9.3 Goal Difference Per Match

`GD/Match = GD / Played`

## 9.4 Win Rate

`WinRate = Wins / Played × 100`

## 9.5 Goals For Per Match

`GF/Match = GF / Played`

## 9.6 Goals Against Per Match

`GA/Match = GA / Played`

## 9.7 Defensive Score

Defensive Score menggunakan GA/Match.

Karena nilai GA/Match yang lebih rendah berarti performa defensif yang lebih baik:

`DEF = (GAmax - GAi) / (GAmax - GAmin) × 100`

Jika:

`GAmax = GAmin`

maka:

`DEF = 50`

untuk seluruh tim.

---

# 10. BPI v1.0 INPUT → DERIVED → SCORE FLOW

```text
RAW DATA
   │
   ├── Played
   ├── Wins
   ├── Draws
   ├── Losses
   ├── GF
   ├── GA
   ├── Points
   └── Recent Form
          │
          ↓
DERIVED METRICS
          │
          ├── PPG
          ├── GD/Match
          ├── Win Rate
          ├── GF/Match
          ├── GA/Match
          └── Defensive Score
          │
          ↓
NORMALIZATION
          │
          ↓
BPI v1.0
          │
          ↓
RANKING


---

11. DATA VALIDATION

Sebelum Calculation Engine dijalankan, data harus melewati validation layer.

Minimum validation:

V1

Played > 0

V2

Wins >= 0

V3

Draws >= 0

V4

Losses >= 0

V5

GF >= 0

V6

GA >= 0

V7

Wins + Draws + Losses = Played

V8

Points >= 0

V9

Untuk sistem 3 poin:

Points = (Wins × 3) + Draws

V10

Team tidak boleh kosong.

V11

Tidak boleh ada duplicate team dalam snapshot yang sama.

V12

Semua tim harus menggunakan snapshot yang sama.


---

12. MISSING DATA

Missing data tidak boleh diganti secara otomatis dengan angka yang dapat memengaruhi hasil BPI.

Contoh yang tidak diperbolehkan:

GA = NULL → GA = 0

atau:

Recent Form = NULL → Recent Form = 50

kecuali aturan tersebut secara eksplisit ditetapkan dalam data policy.

Jika data wajib hilang:

DATA STATUS = INVALID

Calculation Engine tidak boleh menghasilkan official BPI dari data yang invalid.


---

13. DUPLICATE DATA

Satu tim hanya boleh muncul satu kali dalam satu snapshot.

Contoh invalid:

Manchester United
Manchester United
Liverpool
Arsenal

Duplicate record harus diperbaiki sebelum calculation.


---

14. DATA SOURCE

Data source harus dicatat.

Contoh:

Official Competition Data

Official League Table

Approved Statistical Provider

Approved Data API


Setiap dataset harus memiliki:

Source Name

Source Reference

Extraction Timestamp

Data source dapat berubah, tetapi perubahan source harus dicatat dalam historical record.


---

15. DATA TIMESTAMP

Setiap snapshot wajib memiliki timestamp.

Minimum:

YYYY-MM-DD HH:MM:SS UTC

Contoh:

2026-09-11 12:00:00 UTC

Timestamp digunakan untuk:

historical comparison

BPI Change

reproducibility

evaluation

audit



---

16. DATA VERSIONING

Data Specification memiliki version.

Contoh:

DATA_SPEC_VERSION = 1.0

Perubahan struktur data harus meningkatkan versi data specification jika perubahan tersebut dapat memengaruhi calculation.

Perubahan kecil yang tidak memengaruhi calculation dapat dicatat dalam CHANGELOG.


---

17. BPI ENGINE VERSION

Setiap hasil BPI harus menyimpan engine version.

Contoh:

BPI_ENGINE = v1.0

Data yang sama harus menghasilkan hasil yang sama apabila:

data snapshot sama

data specification sama

engine version sama

formula sama



---

18. HISTORICAL DATA RECORD

Historical record minimal menyimpan:

Snapshot ID
Snapshot Date
Competition
Season
Team
Played
Wins
Draws
Losses
GF
GA
Points
Recent Form
PPG
GD
GD/Match
Win Rate
GF/Match
GA/Match
Defensive Score
BPI Score
Power Ranking
BPI Engine Version
Data Specification Version
Data Source

Historical data tidak boleh ditimpa.

Jika terjadi koreksi data, record lama harus tetap dapat ditelusuri.


---

19. DATA IMMUTABILITY

Historical BPI result harus diperlakukan sebagai immutable record.

Artinya:

Data historis yang telah digunakan untuk menghasilkan official BPI tidak boleh diubah tanpa audit trail.

Jika data sumber kemudian dikoreksi:

1. Record lama dipertahankan.


2. Koreksi dicatat.


3. Snapshot baru dibuat.


4. BPI dihitung ulang dengan snapshot baru.


5. Perubahan dicatat dalam history.




---

20. BPI v2.0 DATA

BPI v2.0 membutuhkan data tambahan karena berfungsi sebagai Match Engine.

Planned data:

Match Data

Match ID

Date

Competition

Season

Home Team

Away Team

Venue


Recent Performance

Recent matches

Recent results

Recent goals

Recent opponent strength


Home/Away

Home performance

Away performance

Home goals

Away goals


Opponent Strength

Previous opponents

Opponent BPI

Opponent ranking

Strength-adjusted results


Squad

Starting XI

Player availability

Injuries

Suspensions

Bench strength


Momentum

Recent performance trend

Result sequence

Performance direction


Goal Timing

Goals scored by time interval

Goals conceded by time interval

Goal timing matchup


BPI v2.0 data structure akan dikembangkan lebih lanjut setelah BPI v1.0 data layer dan testing selesai.


---

21. DATA SEPARATION

BPI v1.0 dan BPI v2.0 harus memiliki separation yang jelas.

BPI v1.0:

League / Competition Strength

BPI v2.0:

Specific Match Evaluation

Data tambahan BPI v2.0 tidak boleh dimasukkan ke dalam BPI v1.0 secara diam-diam.


---

22. DATA QUALITY STATUS

Setiap snapshot dapat memiliki status:

VALID

Data memenuhi seluruh validation rule.

WARNING

Data dapat digunakan tetapi terdapat issue yang tidak mengubah calculation secara langsung.

INVALID

Data tidak memenuhi syarat calculation.

Official BPI hanya boleh dihitung dari:

VALID

kecuali terdapat keputusan khusus yang terdokumentasi.


---

23. DATA AUDIT

Setiap official BPI calculation harus dapat ditelusuri kembali ke:

Data Source
      ↓
Snapshot
      ↓
Raw Data
      ↓
Derived Metrics
      ↓
Normalization
      ↓
BPI Calculation
      ↓
Ranking

Tujuannya adalah agar setiap angka BPI dapat diaudit.


---

24. REPRODUCIBILITY

Sistem harus memenuhi prinsip:

Same Data
+
Same Specification
+
Same Engine Version
+
Same Formula
=
Same BPI Result

Perbedaan hasil harus dapat dijelaskan oleh:

perubahan data

perubahan specification

perubahan engine version

perubahan formula resmi


Tidak boleh terjadi perubahan hasil tanpa alasan yang dapat ditelusuri.


---

25. DATA SECURITY AND INTEGRITY

Data tidak boleh dimanipulasi untuk:

menaikkan ranking tim tertentu

menurunkan ranking tim tertentu

menghasilkan prediction tertentu

menyesuaikan hasil dengan opini

menyesuaikan hasil dengan popularitas klub


BPI harus tetap data-driven.


---

26. GOLDEN TEST REQUIREMENT

Data Specification menjadi salah satu dasar untuk Golden Test Case.

Golden Test harus menggunakan dataset yang:

lengkap

valid

deterministic

terdokumentasi

dapat dihitung ulang


Golden Test harus menghasilkan output yang sama selama specification dan engine tidak berubah.


---

27. CHANGE GOVERNANCE

Perubahan pada data specification harus diklasifikasikan.

MINOR CHANGE

Tidak mengubah hasil BPI.

Contoh:

penambahan dokumentasi

perbaikan typo

penjelasan field


MATERIAL CHANGE

Berpotensi mengubah hasil BPI.

Contoh:

perubahan Recent Form encoding

perubahan normalization

perubahan required input

perubahan data treatment


Material change harus:

1. didokumentasikan


2. diuji


3. dievaluasi


4. dicatat di CHANGELOG


5. mendapatkan versioning yang sesuai




---

28. SOURCE OF TRUTH

Urutan authority:

BPI_MASTER_SPEC.md
        ↓
BPI_v1.0.md / BPI_v2.0.md
        ↓
BPI_DATA_SPEC.md
        ↓
TEST CASES
        ↓
IMPLEMENTATION

Jika implementation berbeda dengan specification, implementation harus diperbaiki.

Bukan specification yang disesuaikan secara diam-diam untuk mengikuti implementation.


---

29. CURRENT STATUS

BPI v1.0:

FORMULA LOCKED

Data Layer:

SPECIFICATION DEFINED

Recent Form Encoding:

PENDING EXPLICIT LOCK

BPI v2.0 Data:

ARCHITECTURE DEFINED / EXPANSION PENDING

Calculation Engine:

NOT YET IMPLEMENTED

Golden Test:

NOT YET IMPLEMENTED

Evaluation Engine:

NOT YET IMPLEMENTED


---

30. OFFICIAL PRINCIPLE

BeFree Power Index™ tidak boleh menjadi sistem yang hanya menghasilkan angka.

BPI harus menjadi sistem yang:

dapat ditelusuri

dapat diuji

dapat diulang

dapat dibandingkan

dapat dievaluasi

dapat dikembangkan tanpa merusak versi sebelumnya


Data adalah fondasi dari seluruh sistem.


---

BeFree Power Index™ v151.1

Proprietary System

All Rights Reserved
