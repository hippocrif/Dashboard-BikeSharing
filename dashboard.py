from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st

st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide",
)

sns.set_theme(style="whitegrid")
plt.rcParams["font.sans-serif"] = "DejaVu Sans"

BASE_DIR = Path(__file__).resolve().parent

SEASON_ORDER = ["Spring", "Summer", "Fall", "Winter"]
WEATHER_ORDER = [
    "Clear/Partly Cloudy",
    "Misty/Cloudy",
    "Light Snow/Rain",
    "Severe Weather",
]
TIME_ORDER = ["Rush Hour (Pagi & Sore)", "Jam Kerja / Siang", "Malam / Dini Hari"]
DAY_NAMES = {
    0: "Senin", 1: "Selasa", 2: "Rabu", 3: "Kamis",
    4: "Jumat", 5: "Sabtu", 6: "Minggu",
}
DAY_ORDER = list(DAY_NAMES.values())

SEASON_MAP = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
WEATHER_MAP = {
    1: "Clear/Partly Cloudy",
    2: "Misty/Cloudy",
    3: "Light Snow/Rain",
    4: "Severe Weather",
}
WORKINGDAY_MAP = {0: "Weekend/Holiday", 1: "Working Day"}

SEASON_COLORS = {"Spring": "#2E8B57", "Summer": "#FFA500", "Fall": "#CD5C5C", "Winter": "#4682B4"}
COLOR_CASUAL = "#87CEEB"
COLOR_REGISTERED = "#1E90FF"
COLOR_WORKING = "#1E90FF"
COLOR_HOLIDAY = "#FF6347"


# Memuat & menyiapkan data
def find_file(name: str) -> Path:
    for candidate in (BASE_DIR / name, BASE_DIR.parent / "data" / name, BASE_DIR.parent / name):
        if candidate.exists():
            return candidate
    raise FileNotFoundError(name)


def hr_group(hr: int) -> str:
    """Binning kategori jam"""
    if 7 <= hr <= 9 or 17 <= hr <= 19:
        return "Rush Hour (Pagi & Sore)"
    elif 10 <= hr <= 16:
        return "Jam Kerja / Siang"
    return "Malam / Dini Hari"


def prepare(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["dteday"] = pd.to_datetime(df["dteday"])
    if "season_label" not in df:
        df["season_label"] = df["season"].map(SEASON_MAP)
    if "weather_label" not in df:
        df["weather_label"] = df["weathersit"].map(WEATHER_MAP)
    if "workingday_label" not in df:
        df["workingday_label"] = df["workingday"].map(WORKINGDAY_MAP)
    df["day_name"] = df["dteday"].dt.dayofweek.map(DAY_NAMES)
    if "hr" in df:
        df["time_category"] = df["hr"].apply(hr_group)
    return df


@st.cache_data
def load_data():
    day_df = prepare(pd.read_csv(find_file("day_clean.csv")))
    hour_df = prepare(pd.read_csv(find_file("hour_clean.csv")))
    return day_df, hour_df


def fmt(x) -> str:
    """Format angka dengan pemisah ribuan titik (gaya Indonesia)."""
    return f"{x:,.0f}".replace(",", ".")


def fmt_hr(h: int) -> str:
    return f"{int(h):02d}:00"


INSIGHT_GATHERING = [
    "Dataset berhasil dimuat ke dalam dua dataframe, yaitu `day_df` (peminjaman sepeda harian) dan "
    "`hour_df` (peminjaman per jam). Keduanya memiliki variabel yang sama seperti musim (`season`), "
    "kondisi cuaca (`weathersit`), suhu (`temp`), kelembapan (`hum`), kecepatan angin (`windspeed`), "
    "serta jumlah peminjaman (`cnt`).",
    "Pada lima baris pertama `day_df`, jumlah peminjaman harian (`cnt`) berkisar antara 801 hingga 1.600 "
    "per hari. Pada `hour_df`, `cnt` bervariasi dari 1 hingga 40 pada beberapa jam pertama 1 Januari 2011, "
    "menunjukkan adanya fluktuasi aktivitas peminjaman berdasarkan waktu.",
]
INSIGHT_ASSESSING = [
    "Dataset terdiri dari 731 observasi harian dan 17.379 observasi per jam. Tidak ditemukan missing value "
    "maupun data duplikat pada `day_df` dan `hour_df`, sehingga kelengkapan dan konsistensi data sudah baik.",
    "Jumlah peminjaman per jam (`cnt`) berkisar antara 1 hingga 977, menunjukkan variasi aktivitas yang "
    "signifikan dan potensi adanya jam sibuk tertentu. Kolom `dteday` masih bertipe object dan beberapa "
    "variabel kategorikal berupa kode numerik, sehingga perlu penyesuaian tipe data dan pemahaman kode kategori.",
]
INSIGHT_CLEANING = [
    "Kolom `dteday` diubah menjadi datetime, sehingga data siap untuk analisis berbasis waktu "
    "(harian, bulanan, dan tahunan).",
    "Kolom `season_label`, `weather_label`, dan `workingday_label` ditambahkan agar kode numerik lebih mudah "
    "dipahami dan diinterpretasikan pada eksplorasi dan visualisasi.",
]
INSIGHT_EDA = [
    "Kombinasi musim **Fall** dengan cuaca **Clear/Partly Cloudy** menghasilkan rata-rata peminjaman tertinggi "
    "(sekitar **5.878** per hari), sedangkan **Spring** dengan **Light Snow/Rain** terendah (sekitar **935** per hari). "
    "Cuaca cerah atau sedikit berawan menghasilkan peminjaman lebih tinggi dibanding hujan atau salju ringan, "
    "sehingga musim dan cuaca merupakan faktor penting dalam penggunaan layanan.",
    "Pada data per jam, peminjaman di hari libur (Weekend/Holiday) meningkat mulai pagi dan terus bertambah "
    "hingga menjelang siang. Pengguna terdaftar (*registered*) secara konsisten lebih tinggi dibanding pengguna "
    "kasual (*casual*), sehingga menjadi kontributor utama total peminjaman.",
]
INSIGHT_Q1 = [
    "Rata-rata peminjaman tertinggi terjadi pada musim **Fall** dengan cuaca **Clear/Partly Cloudy**, disusul "
    "**Summer** dan **Winter** dengan cuaca serupa. Cuaca **Light Snow/Rain** secara konsisten menghasilkan "
    "peminjaman jauh lebih rendah di seluruh musim. Pengelola dapat menyiapkan lebih banyak unit pada musim "
    "dan cuaca yang mendukung aktivitas bersepeda.",
    "Pada **hari kerja** terdapat dua puncak sangat tinggi, yaitu sekitar pukul **08.00** dan **17.00–18.00** "
    "(aktivitas komuter). Pada **hari libur**, peminjaman naik bertahap dan puncaknya pada **12.00–15.00**.",
]
INSIGHT_Q2 = [
    "Pengguna terdaftar (*registered*) mendominasi peminjaman, terutama pada jam sibuk hari kerja, sedangkan "
    "pengguna kasual (*casual*) lebih aktif pada siang hingga sore hari dan saat hari libur.",
    "Pola ini menunjukkan perbedaan perilaku yang dapat dimanfaatkan untuk optimalisasi distribusi sepeda dan "
    "penyusunan program loyalitas pelanggan yang lebih tepat sasaran.",
]
INSIGHT_ADV = [
    "Binning waktu: kategori **Rush Hour (Pagi & Sore)** memiliki rata-rata peminjaman tertinggi, sekitar "
    "**332** per jam, jauh di atas Jam Kerja/Siang (**242** per jam) dan Malam/Dini Hari (**77** per jam). "
    "Ini memperkuat temuan bahwa permintaan tertinggi terjadi pada jam mobilitas utama, sehingga ketersediaan "
    "unit perlu diprioritaskan pada rentang tersebut.",
    "RFM bulanan: total peminjaman memuncak pada **September 2012** (lebih dari 218 ribu peminjaman, rata-rata "
    "lebih dari 7.285 per hari), lalu turun bertahap hingga **Desember 2012** (sekitar 123 ribu peminjaman, "
    "rata-rata 3.991 per hari). Pola ini mengindikasikan pengaruh musiman yang perlu dipertimbangkan dalam "
    "perencanaan operasional dan strategi bisnis.",
]
CONCLUSION_Q1 = (
    "Jumlah peminjaman sepeda sangat dipengaruhi oleh musim, kondisi cuaca, dan waktu peminjaman. Musim Fall dengan "
    "cuaca Clear/Partly Cloudy menghasilkan rata-rata peminjaman tertinggi, sedangkan Light Snow/Rain secara "
    "konsisten terendah pada seluruh musim. Pada hari kerja ada dua puncak utama, sekitar pukul 08.00 dan "
    "17.00–18.00 yang mencerminkan perjalanan pergi dan pulang kerja. Pada hari libur, puncak terjadi pada siang "
    "hingga sore hari. Permintaan sepeda meningkat ketika kondisi lingkungan mendukung aktivitas luar ruang dan "
    "pada jam dengan mobilitas masyarakat yang tinggi."
)
CONCLUSION_Q2 = (
    "Pengguna terdaftar (registered) mendominasi jumlah peminjaman pada hampir seluruh periode waktu dan menjadi "
    "kontributor utama total penyewaan. Mereka menunjukkan pola yang sangat kuat pada jam sibuk hari kerja, "
    "terutama pagi dan sore, yang mengindikasikan penggunaan untuk komuter. Pengguna kasual lebih aktif pada "
    "siang hingga sore hari dan cenderung meningkat pada hari libur. Kedua kelompok memiliki kebutuhan dan "
    "karakteristik berbeda sehingga memerlukan pendekatan layanan dan promosi yang berbeda pula."
)
CONCLUSION_ADV = (
    "Kategori Rush Hour (Pagi & Sore) memiliki rata-rata peminjaman tertinggi dibanding kategori waktu lain. "
    "Analisis RFM bulanan memperlihatkan puncak peminjaman pada kuartal ketiga 2012 dan penurunan menjelang akhir "
    "tahun. Ini mengindikasikan pengaruh pola mobilitas harian dan faktor musiman dalam perencanaan operasional."
)
RECOMMENDATIONS = [
    "Menambah jumlah unit sepeda dan memastikan ketersediaan armada pada jam sibuk (**07.00–09.00** dan "
    "**17.00–19.00**), terutama pada hari kerja ketika permintaan mencapai tingkat tertinggi.",
    "Mengoptimalkan distribusi dan pemeliharaan armada pada musim dengan permintaan tinggi, khususnya **Fall** "
    "dan **Summer**, serta menyesuaikan kapasitas operasional saat cuaca kurang mendukung.",
    "Mengembangkan program loyalitas bagi pengguna kasual, seperti diskon berlangganan atau poin reward, untuk "
    "mendorong mereka beralih menjadi pengguna terdaftar yang lebih aktif dan konsisten.",
    "Menyusun kampanye promosi khusus pada periode akhir tahun atau saat permintaan menurun untuk menjaga "
    "tingkat penggunaan dan meningkatkan jumlah peminjaman.",
    "Memanfaatkan perbedaan perilaku pengguna dengan layanan yang lebih personal, seperti **paket komuter** "
    "untuk pengguna terdaftar dan **paket rekreasi akhir pekan** untuk pengguna kasual.",
]


def show_bullets(items):
    for item in items:
        st.markdown(f"- {item}")


try:
    day_all, hour_all = load_data()
except FileNotFoundError as err:
    st.error(
        f"File `{err}` tidak ditemukan. Letakkan `day_clean.csv` dan `hour_clean.csv` "
        "di folder yang sama dengan `dashboard.py` (atau di folder `data/`)."
    )
    st.stop()

# Sidebar: filter
with st.sidebar:
    st.title("🚲 Bike Sharing")
    st.caption("Filter berlaku untuk seluruh grafik dan metrik.")

    min_date = day_all["dteday"].min().date()
    max_date = day_all["dteday"].max().date()
    date_range = st.date_input(
        "Rentang tanggal",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )
    if isinstance(date_range, (tuple, list)):
        if len(date_range) == 2:
            start_date, end_date = date_range
        else:
            start_date = end_date = date_range[0]
    else:
        start_date = end_date = date_range

    seasons = [s for s in SEASON_ORDER if s in set(day_all["season_label"])]
    selected_seasons = st.multiselect("Musim", seasons, default=seasons)

    weathers = [w for w in WEATHER_ORDER if w in set(day_all["weather_label"])]
    selected_weathers = st.multiselect("Kondisi cuaca", weathers, default=weathers)

    st.markdown("---")
    st.markdown("**Nama:** Ilham Maulana  \n**ID Dicoding:** ds009b6y0786")


def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    mask = (
        (df["dteday"].dt.date >= start_date)
        & (df["dteday"].dt.date <= end_date)
        & (df["season_label"].isin(selected_seasons))
        & (df["weather_label"].isin(selected_weathers))
    )
    return df[mask]


day_df = apply_filters(day_all)
hour_df = apply_filters(hour_all)


st.title("🚲 Dashboard Analisis Bike Sharing 2011–2012")
st.markdown(
    "Dashboard interaktif untuk menjawab dua pertanyaan bisnis tentang pola peminjaman sepeda, "
    "berdasarkan *Bike Sharing Dataset*."
)

if day_df.empty or hour_df.empty:
    st.warning("Tidak ada data untuk kombinasi filter yang dipilih. Silakan ubah filter di sidebar.")
    st.stop()

total_rent = day_df["cnt"].sum()
avg_daily = day_df["cnt"].mean()
share_reg = day_df["registered"].sum() / total_rent * 100
share_cas = day_df["casual"].sum() / total_rent * 100

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Peminjaman", fmt(total_rent))
k2.metric("Rata-rata per Hari", fmt(avg_daily))
k3.metric("Pengguna Terdaftar", f"{share_reg:.1f}%")
k4.metric("Pengguna Kasual", f"{share_cas:.1f}%")

tab_data, tab_q1, tab_q2, tab_adv, tab_conc = st.tabs(
    [
        "Tahapan Data",
        "Pertanyaan 1",
        "Pertanyaan 2",
        "Analisis Lanjutan",
        "Kesimpulan & Rekomendasi",
    ]
)


with tab_data:
    st.subheader("Ringkasan Tahapan Analisis Data")
    st.caption("Insight di bawah ini merupakan hasil dari notebook (seluruh periode 2011–2012).")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Gathering Data")
        show_bullets(INSIGHT_GATHERING)
        st.markdown("#### Assessing Data")
        show_bullets(INSIGHT_ASSESSING)
    with c2:
        st.markdown("#### Cleaning Data")
        show_bullets(INSIGHT_CLEANING)
        st.markdown("#### Exploratory Data Analysis")
        show_bullets(INSIGHT_EDA)

    st.markdown("#### Pertanyaan Bisnis")
    st.info(
        "**Pertanyaan 1:** Bagaimana tren peminjaman sepeda harian (cnt) berdasarkan musim (season) dan kondisi "
        "cuaca (weathersit) sepanjang tahun 2011–2012, serta pada jam berapa (hr) puncak peminjaman terjadi pada "
        "hari kerja dibanding hari libur untuk optimalisasi distribusi unit?"
    )
    st.info(
        "**Pertanyaan 2:** Bagaimana perbedaan perilaku peminjaman antara pengguna kasual (casual) dan terdaftar "
        "(registered) berdasarkan waktu (harian & jam sibuk) untuk merancang program loyalitas pelanggan yang "
        "tepat sasaran?"
    )

    with st.expander("Lihat data (sesuai filter)"):
        st.markdown("**Data harian**")
        st.dataframe(day_df.head(100), use_container_width=True)
        st.markdown("**Data per jam**")
        st.dataframe(hour_df.head(100), use_container_width=True)

# Tab 1: Pertanyaan 1
with tab_q1:
    st.subheader("Pertanyaan 1: Musim, Cuaca, dan Jam Puncak")

    hourly_wd = hour_df.groupby(["workingday_label", "hr"])["cnt"].mean().reset_index()
    peak = {}
    for label in ("Working Day", "Weekend/Holiday"):
        sub = hourly_wd[hourly_wd["workingday_label"] == label]
        if not sub.empty:
            peak[label] = sub.loc[sub["cnt"].idxmax()]

    sw = day_df.groupby(["season_label", "weather_label"])["cnt"].mean().reset_index()
    best = sw.loc[sw["cnt"].idxmax()]
    worst = sw.loc[sw["cnt"].idxmin()]

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Kombinasi Tertinggi", f"{best['season_label']} • {best['weather_label']}",
              f"{fmt(best['cnt'])} /hari", delta_color="off")
    m2.metric("Kombinasi Terendah", f"{worst['season_label']} • {worst['weather_label']}",
              f"{fmt(worst['cnt'])} /hari", delta_color="off")
    if "Working Day" in peak:
        m3.metric("Jam Puncak Hari Kerja", fmt_hr(peak["Working Day"]["hr"]),
                  f"{fmt(peak['Working Day']['cnt'])} /jam", delta_color="off")
    if "Weekend/Holiday" in peak:
        m4.metric("Jam Puncak Hari Libur", fmt_hr(peak["Weekend/Holiday"]["hr"]),
                  f"{fmt(peak['Weekend/Holiday']['cnt'])} /jam", delta_color="off")

    # --- Grafik 1 ---
    st.markdown("##### Tren Peminjaman Harian 2011–2012 per Musim")
    trend = day_df.sort_values("dteday")
    fig, ax = plt.subplots(figsize=(14, 4.5))
    sns.scatterplot(
        data=trend, x="dteday", y="cnt", hue="season_label",
        hue_order=[s for s in SEASON_ORDER if s in selected_seasons],
        palette=SEASON_COLORS,
        s=18, alpha=0.7, ax=ax,
    )
    ax.plot(trend["dteday"], trend["cnt"].rolling(7, min_periods=7).mean(),
            color="black", linewidth=1.5, label="Rata-rata bergerak 7 hari")
    ax.set_title("Tren Peminjaman Harian dan Rata-rata Bergerak 7 Hari", fontsize=12, fontweight="bold")
    ax.set_xlabel("Tanggal", fontsize=10)
    ax.set_ylabel("Jumlah Peminjaman (Unit)", fontsize=10)
    ax.legend(title="Musim", loc="upper left", fontsize=8)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    # --- Grafik 2 & 3 ---
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(16, 6))

    sns.barplot(
        data=day_df, x="season_label", y="cnt", hue="weather_label",
        order=[s for s in SEASON_ORDER if s in selected_seasons],
        hue_order=[w for w in WEATHER_ORDER if w in selected_weathers],
        palette="Blues_d", ax=axes[0], errorbar=None,
    )
    axes[0].set_title("Rata-rata Peminjaman Harian Berdasarkan Musim & Cuaca", fontsize=12, fontweight="bold")
    axes[0].set_xlabel("Musim", fontsize=10)
    axes[0].set_ylabel("Jumlah Peminjaman (Unit)", fontsize=10)
    axes[0].legend(title="Cuaca", fontsize=8)

    sns.lineplot(
        data=hour_df, x="hr", y="cnt", hue="workingday_label",
        palette={"Working Day": COLOR_WORKING, "Weekend/Holiday": COLOR_HOLIDAY},
        marker="o", ax=axes[1],
    )
    axes[1].set_title("Pola Peminjaman Per Jam: Hari Kerja vs Hari Libur", fontsize=12, fontweight="bold")
    axes[1].set_xlabel("Jam (00:00 - 23:00)", fontsize=10)
    axes[1].set_ylabel("Rata-rata Peminjaman Per Jam", fontsize=10)
    axes[1].set_xticks(range(0, 24))
    axes[1].legend(title="Tipe Hari", fontsize=8)

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    st.markdown("#### Insight")
    show_bullets(INSIGHT_Q1)

# Tab 2: Pertanyaan 2
with tab_q2:
    st.subheader("Pertanyaan 2: Pengguna Kasual vs Terdaftar")

    hourly_user = hour_df.groupby(["workingday_label", "hr"])[["casual", "registered"]].mean().reset_index()

    def peak_hr(label, col):
        sub = hourly_user[hourly_user["workingday_label"] == label]
        return None if sub.empty else int(sub.loc[sub[col].idxmax(), "hr"])

    p_reg_wd = peak_hr("Working Day", "registered")
    p_cas_wd = peak_hr("Working Day", "casual")
    p_cas_hd = peak_hr("Weekend/Holiday", "casual")
    cas_share_wd = day_df[day_df["workingday"] == 1]["casual"].sum() / max(day_df[day_df["workingday"] == 1]["cnt"].sum(), 1) * 100
    cas_share_hd = day_df[day_df["workingday"] == 0]["casual"].sum() / max(day_df[day_df["workingday"] == 0]["cnt"].sum(), 1) * 100

    q1c, q2c, q3c, q4c = st.columns(4)
    q1c.metric("Puncak Registered (Hari Kerja)", fmt_hr(p_reg_wd) if p_reg_wd is not None else "-")
    q2c.metric("Puncak Casual (Hari Kerja)", fmt_hr(p_cas_wd) if p_cas_wd is not None else "-")
    q3c.metric("Puncak Casual (Hari Libur)", fmt_hr(p_cas_hd) if p_cas_hd is not None else "-")
    q4c.metric("Porsi Casual: Libur vs Kerja", f"{cas_share_hd:.1f}%", f"{cas_share_hd - cas_share_wd:+.1f} poin vs hari kerja",
               delta_color="off")

    # --- Grafik 1: jam sibuk casual vs registered ---
    st.markdown("##### Distribusi Jam Peminjaman: Casual vs Registered")
    melted = pd.melt(
        hour_df, id_vars=["hr", "workingday_label"],
        value_vars=["casual", "registered"],
        var_name="User_Type", value_name="Avg_Rentals",
    )
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(16, 5), sharey=True)
    for ax, (label, title) in zip(
        axes, [("Working Day", "Hari Kerja"), ("Weekend/Holiday", "Hari Libur")]
    ):
        sub = melted[melted["workingday_label"] == label]
        sns.lineplot(
            data=sub, x="hr", y="Avg_Rentals", hue="User_Type",
            hue_order=["casual", "registered"],
            palette=[COLOR_CASUAL, COLOR_REGISTERED], marker="o", ax=ax,
        )
        ax.set_title(f"Casual vs Registered - {title}", fontsize=12, fontweight="bold")
        ax.set_xlabel("Jam (00:00 - 23:00)", fontsize=10)
        ax.set_ylabel("Rata-rata Peminjaman per Jam", fontsize=10)
        ax.set_xticks(range(0, 24))
        ax.tick_params(axis="x", labelsize=8)
        ax.legend(title="Tipe Pengguna", fontsize=8)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    # --- Grafik 2: perilaku harian ---
    st.markdown("##### Perilaku Harian: Rata-rata Peminjaman per Hari dalam Seminggu")
    weekday = (
        day_df.groupby("day_name")[["casual", "registered"]].mean()
        .reindex(DAY_ORDER).dropna(how="all").reset_index()
        .melt(id_vars="day_name", var_name="User_Type", value_name="Avg_Rentals")
    )
    fig, ax = plt.subplots(figsize=(12, 4.5))
    sns.barplot(
        data=weekday, x="day_name", y="Avg_Rentals", hue="User_Type",
        hue_order=["casual", "registered"], palette=[COLOR_CASUAL, COLOR_REGISTERED], ax=ax,
    )
    ax.set_title("Rata-rata Peminjaman Harian: Casual vs Registered", fontsize=13, fontweight="bold")
    ax.set_xlabel("Hari", fontsize=11)
    ax.set_ylabel("Rata-rata Peminjaman per Hari", fontsize=11)
    ax.legend(title="Tipe Pengguna", fontsize=8)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    st.markdown("#### Insight")
    show_bullets(INSIGHT_Q2)

# Tab 3: Analisis lanjutan (Binning jam + RFM bulanan)
with tab_adv:
    st.subheader("Analisis Lanjutan: Binning Waktu & RFM Bulanan")
    st.markdown(
        "**Tujuan:** *Binning* (clustering non-ML) mengelompokkan jam ke dalam tiga kategori berdasarkan aturan "
        "bisnis untuk melihat kapan permintaan paling tinggi. *RFM adaptif bulanan* merangkum jumlah hari "
        "operasional (*Frequency*), total peminjaman (*Monetary*), dan rata-rata harian untuk melihat pola musiman."
    )

    time_summary = (
        hour_df.groupby("time_category")["cnt"].mean()
        .reindex(TIME_ORDER).dropna().reset_index()
    )
    fig, ax = plt.subplots(figsize=(9, 4))
    sns.barplot(
        data=time_summary, x="time_category", y="cnt", hue="time_category",
        palette=["#1E90FF", "#87CEEB", "#B0C4DE"][: len(time_summary)], legend=False, ax=ax,
    )
    for i, v in enumerate(time_summary["cnt"]):
        ax.text(i, v + 3, f"{v:.0f}", ha="center", fontsize=10, fontweight="bold")
    ax.set_title("Rata-rata Peminjaman per Jam Berdasarkan Kategori Waktu", fontsize=12, fontweight="bold")
    ax.set_xlabel("Kategori Waktu", fontsize=10)
    ax.set_ylabel("Rata-rata Peminjaman per Jam", fontsize=10)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    monthly = (
        day_df.assign(bulan=day_df["dteday"].dt.to_period("M"))
        .groupby("bulan")["cnt"].agg(["count", "sum", "mean"])
    )
    monthly.columns = ["Frequency_Days", "Monetary_Total_Rentals", "Recency_Avg_Daily"]
    monthly.index = monthly.index.astype(str)

    fig, ax1 = plt.subplots(figsize=(14, 4.5))
    ax1.bar(monthly.index, monthly["Monetary_Total_Rentals"], color="#87CEEB", label="Total peminjaman")
    ax1.set_ylabel("Total Peminjaman per Bulan", fontsize=10)
    ax1.tick_params(axis="x", rotation=60)
    ax2 = ax1.twinx()
    ax2.plot(monthly.index, monthly["Recency_Avg_Daily"], color="#FF6347", marker="o", label="Rata-rata harian")
    ax2.set_ylabel("Rata-rata Peminjaman per Hari", fontsize=10)
    ax2.grid(False)
    ax1.set_title("Rangkuman RFM Bulanan: Total dan Rata-rata Harian", fontsize=12, fontweight="bold")
    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1 + h2, l1 + l2, loc="upper left", fontsize=8)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    with st.expander("Tabel RFM bulanan"):
        st.dataframe(
            monthly.style.format({
                "Monetary_Total_Rentals": "{:,.0f}",
                "Recency_Avg_Daily": "{:,.1f}",
            }),
            use_container_width=True,
        )

    st.markdown("#### Insight")
    show_bullets(INSIGHT_ADV)

# Tab 4: Kesimpulan & rekomendasi
with tab_conc:
    st.subheader("Conclusion")
    st.markdown("**Kesimpulan Pertanyaan 1**")
    st.success(CONCLUSION_Q1)
    st.markdown("**Kesimpulan Pertanyaan 2**")
    st.success(CONCLUSION_Q2)
    st.markdown("**Kesimpulan Analisis Lanjutan**")
    st.success(CONCLUSION_ADV)

    st.subheader("Rekomendasi Action Item")
    for i, rec in enumerate(RECOMMENDATIONS, start=1):
        st.markdown(f"{i}. {rec}")

st.caption("© Ilham Maulana • Proyek Analisis Data Dicoding • Bike Sharing Dataset")
