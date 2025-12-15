# File: radix_sort.py (KODE FINAL)

# List global untuk menyimpan riwayat langkah
HISTORY = []

def counting_sort_by_digit(arr, exp, max_val, phase_digit):
    """
    Mengimplementasikan Counting Sort berdasarkan digit yang ditentukan oleh 'exp'.
    """
    n = len(arr)
    output = [0] * n
    # Rentang Count Array selalu 0-9 untuk digit desimal
    count = [0] * 10
    
    # 1. Hitung Frekuensi
    for i in range(n):
        # Cari digit pada posisi 'exp'
        index = arr[i] // exp
        digit = index % 10
        count[digit] += 1
        
        # Catat langkah Hitung Frekuensi
        HISTORY.append({
            'array': arr[:],
            'output': output[:],
            'count': count[:],
            'highlight': (i, digit, 'Hitung Digit'), # i: index array, digit: digit 0-9
            'action': f"Fase {phase_digit}: Hitung frekuensi digit '{digit}' dari elemen {arr[i]} (Indeks {i})."
        })

    # 2. Akumulasi (Kumulatif Sum)
    for i in range(1, 10):
        count[i] += count[i - 1]
        
        # Catat langkah Akumulasi
        HISTORY.append({
            'array': arr[:],
            'output': output[:],
            'count': count[:],
            'highlight': (i, -1, 'Akumulasi'), # i: index digit 0-9
            'action': f"Fase {phase_digit}: Akumulasi Count[{i}]. Posisi akhir digit {i} adalah {count[i]}"
        })

    # 3. Pembangunan Output Array (Loop mundur untuk stabilitas)
    for i in range(n - 1, -1, -1):
        index = arr[i] // exp
        digit = index % 10
        
        # Posisi di output_arr
        output_pos = count[digit] - 1
        
        # Tempatkan elemen ke output_arr
        output[output_pos] = arr[i]
        
        # Kurangi count (untuk stabilitas)
        count[digit] -= 1
        
        # Catat langkah Penempatan
        HISTORY.append({
            'array': arr[:],
            'output': output[:],
            'count': count[:],
            'highlight': (i, output_pos, 'Penempatan'), # i: index arr, output_pos: index output
            'action': f"Fase {phase_digit}: Elemen {arr[i]} ditempatkan di output[{output_pos}] berdasarkan digit '{digit}'."
        })
        
    # Salin Output kembali ke arr untuk iterasi berikutnya
    for i in range(n):
        arr[i] = output[i]
        
    # Catat Array setelah disalin kembali (Akhir dari fase digit)
    HISTORY.append({
        'array': arr[:],
        'output': output[:],
        'count': count[:],
        'highlight': (-1, -1, 'Fase Selesai'),
        'action': f"Fase {phase_digit}: Array berhasil diurutkan berdasarkan digit ini. Lanjut ke digit berikutnya."
    })


def radix_sort(data_list):
    """
    Fungsi utama Radix Sort.
    """
    global HISTORY
    HISTORY = []
    
    arr = data_list[:]
    if not arr:
        return [], HISTORY
    
    max_val = max(arr)
    
    HISTORY.append({
        'array': arr[:],
        'output': [0] * len(arr),
        'count': [0] * 10,
        'highlight': (-1, -1, 'Start'),
        'action': f'Memulai Radix Sort. Nilai Maksimum: {max_val}'
    })

    # Iterasi melalui setiap digit (satuan, puluhan, ratusan, dst.)
    exp = 1
    phase_count = 1
    while max_val // exp > 0:
        HISTORY.append({
            'array': arr[:],
            'output': [0] * len(arr),
            'count': [0] * 10,
            'highlight': (-1, -1, 'Digit Baru'),
            'action': f'--- Memulai pengurutan berdasarkan digit: {exp} ---'
        })
        
        # Panggil Counting Sort sebagai subrutin
        counting_sort_by_digit(arr, exp, max_val, phase_count)
        
        exp *= 10
        phase_count += 1

    # STATUS SELESAI DICATAT SETELAH SEMUA DIGIT TUNTAS
    HISTORY.append({
        'array': arr[:],
        'output': arr[:],
        'count': [0] * 10,
        'highlight': (-1, -1, 'Selesai'),
        'action': 'Pengurutan Radix Sort Selesai. Semua digit telah diproses.'
    })
    
    return arr, HISTORY
