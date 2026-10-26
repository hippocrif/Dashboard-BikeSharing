# Proyek Analisis Data: Bike Sharing Dataset

Proyek Submission **"Fundamental Analisa Data"**

- **Nama:** Ilham Maulana
- **Email:** ilhamaulana1001@gmail.com
- **ID Dicoding:** ilham_maulana_hippo

## Struktur Direktori

```
submission
├───dashboard
│   ├───dashboard.py
│   ├───day_clean.csv
│   └───hour_clean.csv
├───data
│   ├───day.csv
│   └───hour.csv
├───Proyek_Analisis_Data_Ilham_Maulana_Submission_Fundamental_Analisis_Data.ipynb
├───README.md
├───requirements.txt
└───url.txt
```

## Setup Environment

1. Buka **Command Prompt (CMD)**, lalu arahkan ke folder `submission` ini dengan
   perintah `cd`, contoh:
   ```
   cd "C:\Users\NamaUser\Desktop\submission"
   ```
2. (Opsional) Buat virtual environment agar library tidak bercampur dengan
   instalasi Python lain:
   ```
   python -m venv venv
   venv\Scripts\activate      # Mac/Linux: source venv/bin/activate
   ```
3. Install seluruh library yang dibutuhkan:
   ```
   pip install -r requirements.txt
   ```
   Library yang digunakan meliputi pandas, numpy, matplotlib, seaborn, dan
   streamlit.
4. Cek apakah Streamlit sudah terpasang dengan benar:
   ```
   streamlit --version
   ```
   Jika muncul nomor versi, instalasi berhasil.

## Menjalankan Notebook

Buka `Proyek_Analisis_Data_Ilham_Maulana_Submission_Fundamental_Analisis_Data.ipynb`
dengan Jupyter Notebook, JupyterLab, atau Google Colab, lalu jalankan seluruh
cell secara berurutan (*Run All*). Pastikan folder `data/` berada satu level
dengan notebook tersebut.

```
jupyter notebook "Proyek_Analisis_Data_Ilham_Maulana_Submission_Fundamental_Analisis_Data.ipynb"
```

## Menjalankan Dashboard (Local)

Masih di jendela CMD yang sama dari folder `submission`, jalankan:

```
cd dashboard
streamlit run dashboard.py
```

Dashboard akan tersedia di `http://localhost:8501`.

## Deploy ke Streamlit Cloud

Dashboard ini sudah di-deploy dan dapat diakses publik di:
**https://dashboard-bikesharing-ilhammaulana.streamlit.app/**

Langkah umum untuk deploy:
1. Push file `dashboard.py`, `day_clean.csv`, `hour_clean.csv`, dan
   `requirements.txt` ke repository GitHub.
2. Buka [share.streamlit.io](https://share.streamlit.io), login dengan akun
   GitHub, lalu klik **New app**.
3. Pilih repository, branch, dan file utama `dashboard/dashboard.py`.
4. Klik **Deploy** dan tunggu proses build selesai.
5. URL aplikasi dicatat di berkas `url.txt`.
