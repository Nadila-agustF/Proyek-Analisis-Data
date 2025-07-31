# 🚀Dashboard Visualisasi Data Penyewaan Sepeda

## 📌 Deskripsi
Proyek ini bertujuan untuk menganalisis dan memvisualisasikan data penyewaan sepeda menggunakan Python. Data dianalisis dan ditampilkan melalui dashboard interaktif dengan **Streamlit**.

### Membuat dan Mengaktifkan Virtual Environment:
*env\Scripts\activate

### 🔧Menginstall library yang diperlukan
*pip install pandas
*pip install matplotlib
*pip install seaborn
*pip install streamlit
*pip install datetime
*pip install babel

## 🛠️ Library yang Digunakan
- **pandas** → Mengelola dan menganalisis data
- **matplotlib** → Membuat grafik dasar
- **seaborn** → Visualisasi data yang lebih menarik
- **streamlit** → Membuat dashboard interaktif
- **datetime** → Mengelola tanggal dan waktu
- **babel** → Format angka dan mata uang sesuai lokal

### Menambahkan dataset
- pd.read_csv("all_data(1)")

### Menjalankan file dashboard
*streamlit run dasboard.py

Link dashboard : [link](https://dashboard-rental.streamlit.app/)

### Struktur Proyek
📦Projek akhir
 ┣ 📂dashboard
 ┃ ┣ 📜all_data(1).csv
 ┃ ┗ 📜dashboard.py
 ┣ 📂data
 ┃ ┣ 📜day.csv
 ┃ ┗ 📜hour.csv
 ┣ 📜Proyek_Akhir_Analisis_Data.ipynb
 ┣ 📜README.MD
 ┗ 📜requirements.txt
