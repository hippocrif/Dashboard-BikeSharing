# Bike Sharing Dashboard ✨

Dashboard interaktif untuk analisis data peminjaman sepeda (*Bike Sharing Dataset*), mencakup eksplorasi faktor musim, cuaca, jam sibuk, perbandingan tipe pengguna (*casual* vs *registered*), serta analisis lanjutan (RFM & Binning Waktu).

## Setup Environment - Anaconda
```bash
conda create --name bike-sharing python=3.9
conda activate bike-sharing
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal
```bash
mkdir bike_sharing_dashboard
cd bike_sharing_dashboard
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Run Streamlit App
```bash
streamlit run dashboard.py
```
