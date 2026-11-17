# Brazilian E-Commerce Public Dataset by Olist

## Deskripsi Proyek

Proyek ini menganalisis Brazilian E-Commerce Public Dataset by Olist untuk memahami performa penjualan, karakteristik pelanggan, dan kinerja pengiriman. Hasil analisis disajikan melalui notebook dan dashboard interaktif menggunakan Streamlit.

## Fokus Analisis

1. **Sales Performance** – Menganalisis tren penjualan, jumlah pesanan, pendapatan, dan rata-rata nilai pesanan.
2. **Customer RFM** – Mengidentifikasi segmentasi pelanggan berdasarkan Recency, Frequency, dan Monetary.
3. **Delivery Performance** – Menganalisis durasi dan ketepatan waktu pengiriman pesanan.

## Struktur Folder

```text
SUBMISSION/
├── Proyek_Analisis_Data.ipynb
├── requirements.txt
└── dashboard/
    ├── app.py
    ├── monthly_sales.csv
    ├── rfm_scored.csv
    └── delivery_data.csv
```

## Instalasi

1. Clone repository:

```bash
git clone <URL-REPOSITORY>
```

2. Masuk ke folder utama proyek:

```bash
cd Proyek_Analisis_Data
```

3. Buat virtual environment:

```bash
python3 -m venv .venv
```

4. Aktifkan virtual environment.

Untuk macOS/Linux:

```bash
source .venv/bin/activate
```

Untuk Windows:

```bash
.venv\Scripts\activate
```

5. Instal seluruh dependensi yang dibutuhkan:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Menjalankan Dashboard

Pastikan virtual environment sudah aktif, kemudian jalankan perintah berikut dari folder utama proyek:

```bash
streamlit run dashboard/app.py
```

Setelah berhasil dijalankan, dashboard dapat diakses melalui alamat lokal yang ditampilkan pada terminal.

## Teknologi yang Digunakan

- Python
- Pandas
- Streamlit
- Plotly
- Google Colab