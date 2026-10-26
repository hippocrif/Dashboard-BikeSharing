from pathlib import Path

import matplotlib.pyplot as plt
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

SEASON_MAP = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
WEATHER_MAP = {
    1: "Clear/Partly Cloudy",
    2: "Misty/Cloudy",
    3: "Light Snow/Rain",
    4: "Severe Weather",
}
WORKINGDAY_MAP = {0: "Weekend/Holiday", 1: "Working Day"}

COLOR_HOLIDAY = "#FF6347"
COLOR_WORKING = "#1E90FF"
COLOR_CASUAL = "#FF8C00"
COLOR_REGISTERED = "#1E90FF"


# Memuat & menyiapkan data
def find_file(name: str) -> Path:
    for candidate in (BASE_DIR / name, BASE_DIR.parent / "data" / name, BASE_DIR.parent / name):
        if candidate.exists():
            return candidate
    raise FileNotFoundError(name)


def hr_group(hr: int) -> str:
    """Binning kategori jam (Analisis Lanjutan)"""
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
    if "hr" in df:
        df["time_category"] = df["hr"].apply(hr_group)
    return df


@st.cache_data
def load_data():
    day_df = prepare(pd.read_csv(find_file("day_clean.csv")))
    hour_df = prepare(pd.read_csv(find_file("hour_clean.csv")))
    return day_df, hour_df


def fmt(x) -> str:
    """Bilangan bulat dengan pemisah ribuan titik (gaya Indonesia)."""
    return f"{x:,.0f}".replace(",", ".")


def fmt1(x) -> str:
    """Satu desimal, gaya Indonesia (titik ribuan, koma desimal)."""
    return f"{x:,.1f}".replace(",", "X").replace(".", ",").replace("X", ".")


def fmt_hr(h: int) -> str:
    return f"{int(h):02d}:00"


# Insight
Q1_TEXT = (
    "Bagaimana perbedaan rata-rata penyewaan sepeda harian (cnt) berdasarkan musim (season) dan kondisi cuaca "
    "(weathersit) sepanjang tahun 2011–2012, serta pada jam berapa (hr) puncak peminjaman terjadi pada hari kerja "
    "dibanding hari libur untuk optimalisasi distribusi unit?"
)
Q2_TEXT = (
    "Bagaimana perbandingan rata-rata peminjaman per jam antara pengguna kasual (casual) dan terdaftar "
    "(registered) sepanjang tahun 2011–2012, sebagai dasar perancangan program loyalitas dan strategi konversi "
    "pelanggan yang tepat sasaran?"
)

INSIGHT_GATHERING = [
    "Dataset berhasil dimuat ke dalam dua dataframe, yaitu `day_df` yang berisi data peminjaman sepeda harian dan "
    "`hour_df` yang berisi data peminjaman per jam. Kedua dataset memiliki variabel yang sama seperti musim "
    "(`season`), kondisi cuaca (`weathersit`), suhu (`temp`), kelembapan (`hum`), kecepatan angin (`windspeed`), "
    "serta jumlah peminjaman (`cnt`).",
    "Pada lima baris pertama `day_df`, jumlah peminjaman harian (`cnt`) berkisar antara 801 hingga 1.600 "
    "peminjaman per hari. Sementara itu, pada `hour_df`, jumlah peminjaman per jam (`cnt`) bervariasi dari 1 hingga "
    "40 peminjaman pada beberapa jam pertama tanggal 1 Januari 2011, menunjukkan adanya fluktuasi aktivitas "
    "peminjaman berdasarkan waktu.",
]
INSIGHT_ASSESSING = [
    "Dataset terdiri dari 731 observasi harian dan 17.379 observasi per jam. Tidak ditemukan missing value maupun "
    "data duplikat pada `day_df` dan `hour_df`, sehingga kelengkapan dan konsistensi data secara umum sudah baik.",
    "Jumlah peminjaman per jam (`cnt`) berkisar antara 1 hingga 977 peminjaman, menunjukkan variasi aktivitas yang "
    "signifikan dan potensi adanya jam sibuk tertentu. Selain itu, kolom `dteday` masih bertipe object dan beberapa "
    "variabel kategorikal menggunakan kode numerik, sehingga diperlukan penyesuaian tipe data dan pemahaman kode "
    "kategori untuk memudahkan eksplorasi serta interpretasi hasil analisis.",
]
STEPS_TO_TAKE = [
    "Mengubah kolom `dteday` dari tipe data object menjadi datetime agar analisis berbasis waktu (harian, bulanan, "
    "dan tahunan) lebih mudah dilakukan.",
    "Melakukan validasi serta transformasi kolom kategorikal seperti `season`, `weathersit`, `weekday`, dan `yr` "
    "menjadi label yang lebih informatif agar hasil visualisasi dan analisis lebih mudah dipahami.",
]
INSIGHT_CLEANING = [
    "Proses pembersihan data berhasil dilakukan dengan mengubah kolom `dteday` menjadi format datetime, sehingga "
    "data kini lebih siap untuk analisis berbasis waktu, seperti tren harian, bulanan, maupun tahunan.",
    "Penambahan kolom kategorikal berupa `season_label`, `weather_label`, dan `workingday_label` membuat informasi "
    "yang sebelumnya berbentuk kode numerik menjadi lebih mudah dipahami dan diinterpretasikan, sehingga "
    "mempermudah proses eksplorasi data serta visualisasi pada tahap analisis selanjutnya.",
]
INSIGHT_EDA = [
    "Musim Gugur (**Fall**) dan cuaca **Cerah/Berawan** mencatatkan rata-rata peminjaman harian tertinggi "
    "(mencapai **5.644** dan **4.876** unit/hari), sedangkan cuaca buruk merosotkan peminjaman hingga **1.803** "
    "unit/hari. Selain itu, peminjaman mencapai lonjakan puncak pada jam berangkat kerja (pukul 07:00–08:00).",
    "Pengguna terdaftar (*registered*) mendominasi total peminjaman secara signifikan dibanding pengguna kasual "
    "(*casual*), dengan puncak peminjaman pada jam 08:00 (**337** unit vs **21** unit). Hal ini menunjukkan bahwa "
    "pengguna registered didominasi oleh pekerja komuter harian, sementara pengguna casual lebih aktif pada siang "
    "hingga sore hari untuk aktivitas kasual/rekreasi.",
]
INSIGHT_Q1 = [
    "Musim Gugur (**Fall**) dan kondisi cuaca **Cerah/Berawan** (Clear/Partly Cloudy) menghasilkan rata-rata "
    "peminjaman tertinggi harian, sedangkan cuaca buruk (Light Snow/Rain) menurunkan peminjaman secara drastis.",
    "Pola peminjaman pada **hari kerja** (Working Day) memiliki dua puncak signifikan pada jam komuter berangkat "
    "dan pulang kerja (pukul **08:00** dan **17:00–18:00**), sementara peminjaman pada **hari libur** "
    "(Weekend/Holiday) terdistribusi lebih merata pada siang hingga sore hari (pukul **12:00–16:00**).",
]
INSIGHT_Q2 = [
    "Pengguna terdaftar (*Registered*) secara dominan mendominasi volume peminjaman sepeda dengan puncak tajam pada "
    "jam kerja pagi dan sore hari (pukul **08:00** dan **17:00**).",
    "Sebaliknya, tren peminjaman pengguna kasual (*Casual*) bergerak lebih landai dengan peningkatan bertahap mulai "
    "siang hingga sore hari (pukul **12:00–17:00**), yang mengindikasikan bahwa segmen pengguna terdaftar "
    "berorientasi pada mobilitas harian/rutinitas, sedangkan pengguna kasual berorientasi pada aktivitas rekreasi.",
]
INSIGHT_ADV = [
    "Segmentasi jam menunjukkan bahwa kategori **Rush Hour (Pagi & Sore)** mencatatkan rata-rata peminjaman "
    "tertinggi sebesar **331** unit/jam, diikuti oleh Jam Kerja / Siang sebesar **241** unit/jam. Sebaliknya, "
    "kategori Malam / Dini Hari berada pada tingkat terendah yaitu **77** unit/jam. Hal ini menegaskan bahwa "
    "kebutuhan alokasi dan pemeliharaan unit armada sepeda berada pada titik paling kritis pada waktu berangkat "
    "dan pulang kerja.",
    "Performa penyewaan mencapai puncak tertinggi pada bulan **September 2012** dengan rata-rata harian sebesar "
    "**7.285** unit/hari (Monetary Total: 218.573 unit). Namun, memasuki kuartal keempat (Oktober hingga Desember "
    "2012), terjadi penurunan kinerja harian yang cukup signifikan secara bertahap hingga menyentuh angka "
    "**3.990** unit/hari pada bulan Desember, yang dipengaruhi oleh faktor penurunan suhu dan perubahan musim "
    "menjelang akhir tahun.",
]
CONCLUSION_Q1 = (
    "Penyewaan sepeda sangat dipengaruhi oleh faktor musim, cuaca, dan jam operasional, di mana Musim Gugur (Fall) "
    "dan cuaca Cerah/Berawan (Clear/Partly Cloudy) mencatatkan rata-rata peminjaman harian tertinggi (sebesar "
    "5.644 dan 4.876 unit/hari), sedangkan cuaca buruk (Light Snow/Rain) merosotkan peminjaman hingga 1.803 "
    "unit/hari. Selain itu, peminjaman pada hari kerja mengalami lonjakan tajam pada jam berangkat dan pulang kerja "
    "(pukul 08:00 sebesar 477 unit/jam dan pukul 17:00–18:00 sebesar 525 unit/jam), sementara pada hari libur "
    "puncak peminjaman bergeser lebih merata pada siang hingga sore hari (pukul 12:00–16:00 sekitar 370 unit/jam)."
)
CONCLUSION_Q2 = (
    "Pengguna terdaftar (registered) menjadi kontributor utama peminjaman yang secara signifikan mendominasi "
    "seluruh periode waktu dengan pola komuter harian yang kuat pada jam 08:00 (337 unit/jam) dan jam 17:00 "
    "(387 unit/jam). Sebaliknya, pengguna kasual (casual) memiliki tren peminjaman yang lebih landai dengan puncak "
    "pada siang hingga sore hari (pukul 12:00–16:00 sekitar 68–75 unit/jam), yang menunjukkan perbedaan orientasi "
    "penggunaan antara mobilitas rutinitas harian (registered) dan aktivitas rekreasi (casual)."
)
CONCLUSION_ADV = (
    "Analisis binning waktu menunjukkan bahwa kategori Rush Hour (Pagi & Sore) mencatatkan rata-rata penyewaan "
    "tertinggi sebesar 331 unit/jam, jauh melampaui kategori Jam Kerja/Siang (241 unit/jam) dan Malam/Dini Hari "
    "(77 unit/jam). Sementara itu, analisis RFM adaptif bulanan menunjukkan kinerja peminjaman mencapai puncak "
    "tertinggi pada bulan September 2012 (7.285 unit/hari), sebelum mengalami penurunan bertahap hingga titik "
    "terendah pada bulan Desember 2012 (3.990 unit/hari) akibat perubahan musim dingin."
)
RECOMMENDATIONS = [
    "**Optimalisasi Alokasi Armada pada Jam Sibuk (Rush Hour):** Memaksimalkan ketersediaan armada di stasiun area "
    "perkantoran pada jam 07:00–09:00 dan 17:00–19:00 di hari kerja, serta meredistribusi unit ke area rekreasi "
    "pada jam 12:00–16:00 saat akhir pekan.",
    "**Manajemen Operasional Berbasis Musim dan Cuaca:** Memaksimalkan unit siap pakai pada musim puncak (Musim "
    "Gugur dan Panas), serta menjadwalkan perawatan berkala (maintenance) secara intensif pada Musim Semi dan saat "
    "cuaca buruk ketika peminjaman sedang rendah.",
    "**Strategi Konversi Pengguna Kasual ke Terdaftar:** Mengembangkan program loyalitas dan promosi konversi bagi "
    "pengguna casual, seperti penawaran diskon paket membership komuter harian saat akhir pekan ketika aktivitas "
    "pengguna casual sedang tinggi.",
    "**Kampanye Promosi Penyeimbang Musim (End-of-Year Campaign):** Menyusun strategi promosi penyesuaian tarif "
    "atau program event khusus pada kuartal akhir tahun (Oktober–Desember) untuk mempertahankan tingkat peminjaman "
    "di tengah penurunan suhu dan perubahan musim.",
    "**Personalisasi Layanan Berdasarkan Segmen Pengguna:** Membedakan penawaran produk layanan, seperti Commuter "
    "Pass berlangganan hemat untuk pengguna registered pada hari kerja, dan Weekend Pass / Leisure Pass untuk "
    "pengguna casual pada hari libur.",
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
    st.markdown(
        "**Nama:** Ilham Maulana  \n"
        "**Email:** ilhamaulana1001@gmail.com  \n"
        "**ID Dicoding:** ilham_maulana_hippo"
    )


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

# Tahapan data
with tab_data:
    st.subheader("Ringkasan Tahapan Analisis Data")
    st.caption("Insight di bawah ini merupakan hasil dari notebook (seluruh periode 2011–2012).")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Gathering Data")
        show_bullets(INSIGHT_GATHERING)
        st.markdown("#### Assessing Data")
        show_bullets(INSIGHT_ASSESSING)
        st.markdown("**Steps to Take:**")
        show_bullets(STEPS_TO_TAKE)
    with c2:
        st.markdown("#### Cleaning Data")
        show_bullets(INSIGHT_CLEANING)
        st.markdown("#### Exploratory Data Analysis")
        show_bullets(INSIGHT_EDA)

    st.markdown("#### Pertanyaan Bisnis")
    st.info(f"**Pertanyaan 1:** {Q1_TEXT}")
    st.info(f"**Pertanyaan 2:** {Q2_TEXT}")

    with st.expander("Lihat data (sesuai filter)"):
        st.markdown("**Data harian**")
        st.dataframe(day_df.head(100))
        st.markdown("**Data per jam**")
        st.dataframe(hour_df.head(100))

# Pertanyaan 1
with tab_q1:
    st.subheader("Pertanyaan 1: Musim, Cuaca, dan Jam Puncak")
    st.markdown(Q1_TEXT)

    season_summary = (
        day_df.groupby("season_label")["cnt"].mean()
        .reindex(SEASON_ORDER).dropna().reset_index()
    )
    weather_summary = (
        day_df.groupby("weather_label")["cnt"].mean()
        .reindex(WEATHER_ORDER).dropna().reset_index()
    )
    hourly_workingday = (
        hour_df.groupby(["workingday_label", "hr"])["cnt"].mean().reset_index()
    )

    best_season = season_summary.loc[season_summary["cnt"].idxmax()]
    best_weather = weather_summary.loc[weather_summary["cnt"].idxmax()]
    worst_weather = weather_summary.loc[weather_summary["cnt"].idxmin()]

    a1, a2, a3 = st.columns(3)
    a1.metric("Musim Tertinggi", best_season["season_label"],
              f"{fmt1(best_season['cnt'])} unit/hari", delta_color="off")
    a2.metric("Cuaca Tertinggi", best_weather["weather_label"],
              f"{fmt1(best_weather['cnt'])} unit/hari", delta_color="off")
    a3.metric("Cuaca Terendah", worst_weather["weather_label"],
              f"{fmt1(worst_weather['cnt'])} unit/hari", delta_color="off")

    wd = hourly_workingday[hourly_workingday["workingday_label"] == "Working Day"]
    hd = hourly_workingday[hourly_workingday["workingday_label"] == "Weekend/Holiday"]
    b1, b2 = st.columns(2)
    if not wd.empty:
        morning = wd[wd["hr"] < 12]
        evening = wd[wd["hr"] >= 12]
        if not morning.empty and not evening.empty:
            pm = morning.loc[morning["cnt"].idxmax()]
            pe = evening.loc[evening["cnt"].idxmax()]
            b1.metric("Jam Puncak Hari Kerja (Pagi / Sore)",
                      f"{fmt_hr(pm['hr'])} / {fmt_hr(pe['hr'])}",
                      f"{fmt(pm['cnt'])} / {fmt(pe['cnt'])} unit/jam", delta_color="off")
    if not hd.empty:
        ph = hd.loc[hd["cnt"].idxmax()]
        b2.metric("Jam Puncak Hari Libur", fmt_hr(ph["hr"]),
                  f"{fmt1(ph['cnt'])} unit/jam", delta_color="off")

    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(20, 5))

    # Rata-rata peminjaman berdasarkan musim
    sns.barplot(
        data=season_summary, x="season_label", y="cnt",
        hue="season_label", palette="Blues_d", legend=False, ax=axes[0],
    )
    axes[0].set_title("Rata-rata Peminjaman Harian per Musim", fontsize=12, fontweight="bold")
    axes[0].set_xlabel("Musim", fontsize=10)
    axes[0].set_ylabel("Rata-rata Peminjaman (Unit)", fontsize=10)

    # Rata-rata peminjaman berdasarkan cuaca
    sns.barplot(
        data=weather_summary, x="weather_label", y="cnt",
        hue="weather_label", palette="Reds_d", legend=False, ax=axes[1],
    )
    axes[1].set_title("Rata-rata Peminjaman Harian per Cuaca", fontsize=12, fontweight="bold")
    axes[1].set_xlabel("Kondisi Cuaca", fontsize=10)
    axes[1].set_ylabel("Rata-rata Peminjaman (Unit)", fontsize=10)
    axes[1].tick_params(axis="x", rotation=15)

    # Pola peminjaman per jam: hari kerja vs hari libur
    sns.lineplot(
        data=hourly_workingday, x="hr", y="cnt", hue="workingday_label",
        palette={"Weekend/Holiday": COLOR_HOLIDAY, "Working Day": COLOR_WORKING},
        marker="o", ax=axes[2],
    )
    axes[2].set_title("Pola Jam Puncak: Hari Kerja vs Libur", fontsize=12, fontweight="bold")
    axes[2].set_xlabel("Jam (00:00 - 23:00)", fontsize=10)
    axes[2].set_ylabel("Rata-rata Peminjaman Per Jam", fontsize=10)
    axes[2].set_xticks(range(0, 24, 2))
    axes[2].legend(title="Tipe Hari", fontsize=8)

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    st.markdown("#### Insight")
    show_bullets(INSIGHT_Q1)

# Pertanyaan 2
with tab_q2:
    st.subheader("Pertanyaan 2: Pengguna Kasual vs Terdaftar")
    st.markdown(Q2_TEXT)

    user_type_hourly = hour_df.groupby("hr")[["casual", "registered"]].mean().reset_index()

    reg_morning = user_type_hourly[user_type_hourly["hr"] < 12]
    reg_evening = user_type_hourly[user_type_hourly["hr"] >= 12]
    cas_peak = user_type_hourly.loc[user_type_hourly["casual"].idxmax()]
    ratio = user_type_hourly["registered"].mean() / max(user_type_hourly["casual"].mean(), 1e-9)

    c1, c2, c3, c4 = st.columns(4)
    if not reg_morning.empty:
        pr = reg_morning.loc[reg_morning["registered"].idxmax()]
        c1.metric("Puncak Registered (Pagi)", fmt_hr(pr["hr"]),
                  f"{fmt1(pr['registered'])} unit/jam", delta_color="off")
    if not reg_evening.empty:
        ps = reg_evening.loc[reg_evening["registered"].idxmax()]
        c2.metric("Puncak Registered (Sore)", fmt_hr(ps["hr"]),
                  f"{fmt1(ps['registered'])} unit/jam", delta_color="off")
    c3.metric("Puncak Casual", fmt_hr(cas_peak["hr"]),
              f"{fmt1(cas_peak['casual'])} unit/jam", delta_color="off")
    c4.metric("Registered : Casual", f"{ratio:.1f} : 1", "rata-rata per jam", delta_color="off")

    user_type_melted = pd.melt(
        user_type_hourly, id_vars=["hr"], value_vars=["casual", "registered"],
        var_name="User_Type", value_name="Avg_Rentals",
    )
    user_type_melted["User_Type"] = user_type_melted["User_Type"].map({
        "casual": "Pengguna Kasual (Casual)",
        "registered": "Pengguna Terdaftar (Registered)",
    })

    fig, ax = plt.subplots(figsize=(12, 5))
    sns.lineplot(
        data=user_type_melted, x="hr", y="Avg_Rentals", hue="User_Type",
        hue_order=["Pengguna Kasual (Casual)", "Pengguna Terdaftar (Registered)"],
        palette=[COLOR_CASUAL, COLOR_REGISTERED], linewidth=2.5, marker="o", ax=ax,
    )
    ax.set_title("Perbandingan Rata-rata Peminjaman per Jam: Casual vs Registered (2011–2012)",
                 fontsize=13, fontweight="bold")
    ax.set_xlabel("Jam (00:00 - 23:00)", fontsize=11)
    ax.set_ylabel("Rata-rata Peminjaman Per Jam", fontsize=11)
    ax.set_xticks(range(0, 24))
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend(title="Tipe Pengguna", fontsize=10)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    st.markdown("#### Insight")
    show_bullets(INSIGHT_Q2)

# Analisis lanjutan (binning jam + RFM bulanan)
with tab_adv:
    st.subheader("Analisis Lanjutan: Binning Waktu & RFM Bulanan")
    st.markdown(
        "**Tujuan:** *Binning* (clustering non-ML) mengelompokkan jam ke dalam tiga kategori berdasarkan aturan "
        "bisnis untuk melihat kapan permintaan paling tinggi. *RFM adaptif bulanan* merangkum jumlah hari "
        "operasional (*Frequency*), total peminjaman (*Monetary*), dan rata-rata harian (*Recency_Avg_Daily*) "
        "untuk melihat pola musiman."
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
        ax.text(i, v + 3, fmt1(v), ha="center", fontsize=10, fontweight="bold")
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
            })
        )

    st.markdown("#### Insight")
    show_bullets(INSIGHT_ADV)

# Kesimpulan & rekomendasi
with tab_conc:
    st.subheader("Conclusion")
    st.markdown("**Kesimpulan Pertanyaan 1**")
    st.success(CONCLUSION_Q1)
    st.markdown("**Kesimpulan Pertanyaan 2**")
    st.success(CONCLUSION_Q2)
    st.markdown("**Kesimpulan Analisis Lanjutan**")
    st.success(CONCLUSION_ADV)

    st.subheader("Rekomendasi Action Item")
    for rec in RECOMMENDATIONS:
        st.markdown(f"- {rec}")

st.caption("© Ilham Maulana • Proyek Analisis Data Dicoding • Bike Sharing Dataset")
