# File: app.py (KODE FINAL - Matplotlib Radix Sort)

import streamlit as st
import pandas as pd
import time
from radix_sort import radix_sort 
import matplotlib.pyplot as plt
import numpy as np

# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="Virtual Lab: Radix Sort",
    layout="wide"
)

st.title("🔢 Virtual Lab: Radix Sort Interaktif (Matplotlib)")
st.markdown("### Visualisasi Algoritma Pengurutan Berdasarkan Digit")

st.sidebar.header("Konfigurasi Data")

# --- Input Pengguna (Tanpa Batas Input) ---
default_data = "170, 45, 75, 90, 802, 24, 2, 66"
input_data_str = st.sidebar.text_input(
    "Masukkan data (pisahkan dengan koma):", 
    default_data
)
speed = st.sidebar.slider("Kecepatan Simulasi (detik)", 0.1, 2.0, 0.5)

# --- Proses Data Input ---
try:
    data_list = [int(x.strip()) for x in input_data_str.split(',') if x.strip()]
    initial_data = list(data_list)
    if not initial_data:
        st.error("Masukkan setidaknya satu angka.")
        st.stop()
except ValueError:
    st.error("Masukkan data dalam format angka (integer) yang dipisahkan oleh koma.")
    st.stop()
    
# --- Penjelasan ---
st.markdown("""
#### Proses Radix Sort (Digit by Digit):
Radix Sort menggunakan Counting Sort berulang kali. Setiap langkah mengurutkan array berdasarkan satu digit (satuan, puluhan, ratusan, dst.).
* **Kuning:** Elemen yang sedang dihitung/ditempatkan.
* **Merah (Count):** Digit yang sedang diproses dalam Count Array.
* **Biru:** Array yang sudah terurut pada digit sebelumnya.
""")

st.write(f"**Data Awal:** {initial_data}")

# --- Fungsi Plot Matplotlib ---
def plot_array(arr, title, highlight_indices, max_val, action_type):
    fig, ax = plt.subplots(figsize=(10, 4))
    n = len(arr)
    x_pos = np.arange(n)
    
    colors = ['#4A86E8'] * n # Default (Biru)
    
    idx_arr, idx_out = highlight_indices
    
    for i in range(n):
        # Kuning: Elemen Input yang sedang dihitung/ditempatkan
        if idx_arr != -1 and i == idx_arr and action_type in ('Hitung Digit', 'Penempatan'):
            colors[i] = '#F1C232'
        # Hijau: Elemen Output yang baru ditempatkan
        elif idx_out != -1 and i == idx_out and action_type == 'Penempatan':
            colors[i] = '#6AA84F'

    # Bar Plot
    ax.bar(x_pos, arr, color=colors)
    
    # Label Nilai di Atas Bar
    for i, height in enumerate(arr):
        ax.text(x_pos[i], height + max_val * 0.02, str(height), ha='center', va='bottom', fontsize=10)
        
    ax.set_ylim(0, max_val * 1.1 if max_val > 0 else 10)
    ax.set_xticks(x_pos)
    ax.set_xticklabels([f'Posisi {i}' for i in range(n)], rotation=0)
    ax.set_xlabel('Index')
    ax.set_title(title, fontsize=12)
    
    plt.close(fig) 
    return fig


# --- Visualisasi Utama ---
if st.button("Mulai Simulasi Radix Sort"):
    
    sorted_result, history = radix_sort(list(data_list))
    max_data_value = max(initial_data) if initial_data else 10
    
    st.markdown("---")
    st.subheader("Visualisasi Langkah Demi Langkah")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        vis_placeholder = st.empty()
        status_placeholder = st.empty() 
    with col2:
        table_placeholder = st.empty()
    
    # --- Loop Simulasi ---
    for step, state in enumerate(history):
        
        current_arr = state['array']
        current_count = state['count']
        current_output = state['output']
        (idx_arr, idx_digit_out, action_type) = state['highlight']
        action = state['action']
        
        # Penentuan Highlight Index untuk Plot:
        idx_arr_highlight = idx_arr
        idx_out_highlight = idx_digit_out if action_type == 'Penempatan' else -1

        # --- Tampilkan Grafik (Matplotlib) ---
        with vis_placeholder.container():
             # Kita hanya memvisualisasikan Input Array yang terus diperbarui oleh Radix Sort
             fig_mpl = plot_array(current_arr, "Array Saat Ini", 
                                  (idx_arr_highlight, idx_out_highlight), 
                                  max_data_value, action_type)
             st.pyplot(fig_mpl, clear_figure=True)
        
        # --- TABEL COUNT ARRAY ---
        with table_placeholder.container():
            st.markdown("##### Detail Count Array (Digit 0-9)")
            
            # Highlight index di Count Array adalah digit yang sedang diproses
            highlight_digit = -1
            if action_type in ('Hitung Digit', 'Akumulasi', 'Penempatan'):
                highlight_digit = idx_digit_out
            
            # Membuat DataFrame Count Array
            df_count = pd.DataFrame({
                'Digit (i)': range(len(current_count)), 
                'Hitungan/Posisi': current_count
            })
            
            # Tampilkan sebagai HTML untuk Custom Highlighting
            def color_row(row):
                # Merah untuk digit yang sedang diproses
                if row['Digit (i)'] == highlight_digit:
                    return ['background-color: #CC0000', 'background-color: #CC0000']
                return [''] * len(row)
            
            st.dataframe(df_count.style.apply(color_row, axis=1), hide_index=True, use_container_width=True)

        with status_placeholder.container():
            st.info(f"**Langkah ke-{step+1}** | **Aksi:** {action_type}")
            st.caption(action)
            
            if action_type == 'Selesai':
                 st.success("Array telah terurut! Proses Radix Sort Selesai.")
        
        # Jeda untuk simulasi
        time.sleep(speed)

    # --- Hasil Akhir Final ---
    st.balloons()
    st.success(f"**Pengurutan Selesai!**")
    st.write(f"**Data Terurut:** {sorted_result}")
    st.info(f"Algoritma Radix Sort selesai dalam **{len(history)-1}** langkah visualisasi.")
