"""
Dataset Graf untuk Proyek Smart Route Optimization - Kota Medan
Sumber Data: TomTom Routing API (Rute Tercepat, Hindari Tol)
Dibuat oleh Peran A2 (Data & Model Specialist) untuk A1 (Programmer)

Karakteristik Graf:
- Tipe: Graf Berbobot Tak Berarah (Undirected Weighted Graph)
- Jumlah Simpul (V): 11 Simpul (Lokasi Strategis di Kota Medan)
- Jumlah Sisi (E): 19 Sisi Jalan Utama
- Satuan Bobot: Jarak dalam Kilometer (km)
"""

# Pemetaan ID Simpul (V1 - V11) ke Nama Lokasi Riil di Kota Medan
NODE_NAMES = {
    "V1": "Marelan Square",
    "V2": "Lapangan Merdeka",
    "V3": "Thamrin Plaza",
    "V4": "Istana Maimun",
    "V5": "Sun Plaza",
    "V6": "Centre Point Mall",
    "V7": "USU (Padang Bulan)",
    "V8": "RSUP H. Adam Malik",
    "V9": "Terminal Amplas",
    "V10": "Unimed (Kampus 1)",
    "V11": "Cambridge City Square"
}

names = NODE_NAMES

# Representasi Graf Berbobot G = (V, E, W) dalam bentuk Adjacency List
GRAPH = {
    "V1": {"V2": 13.5, "V3": 15.2, "V10": 15.5},
    "V2": {"V1": 13.5, "V3": 3.0, "V4": 2.9, "V5": 2.4},
    "V3": {"V1": 15.2, "V2": 3.0, "V6": 2.6},
    "V4": {"V2": 2.9, "V6": 2.4, "V10": 7.7},
    "V5": {"V2": 2.4, "V7": 3.4, "V8": 13.0, "V11": 0.9},
    "V6": {"V3": 2.6, "V4": 2.4, "V10": 6.4},
    "V7": {"V5": 3.4, "V8": 10.1, "V10": 10.8, "V11": 3.1},
    "V8": {"V5": 13.0, "V7": 10.1, "V9": 14.2},
    "V9": {"V8": 14.2, "V10": 11.3},
    "V10": {"V1": 15.5, "V4": 7.7, "V6": 6.4, "V7": 10.8, "V9": 11.3, "V11": 10.7},
    "V11": {"V5": 0.9, "V7": 3.1, "V10": 10.7}
}

graph = GRAPH

# Tata Letak Topologi Geometris Presisi (Mencegah Tumpang Tindih)
POSITIONS = {
    "V1":  (0.0, 5.2),    # Marelan (Paling Utara)
    "V2":  (0.0, 2.7),    # Lap. Merdeka (Pusat Kota)
    "V3":  (2.8, 3.6),    # Thamrin Plaza (Timur-Utara)
    "V6":  (4.8, 2.4),    # Centre Point (Timur)
    "V10": (7.0, 1.2),    # Unimed (Paling Timur)
    "V4":  (2.2, 0.7),    # Istana Maimun (Selatan Pusat)
    "V11": (-4.2, 2.7),   # Cambridge (Barat)
    "V5":  (-1.8, 1.5),   # Sun Plaza (Barat Daya Pusat)
    "V7":  (-2.8, -1.0),  # USU Padang Bulan (Barat Daya)
    "V8":  (-5.5, -2.6),  # RSUP Adam Malik (Ujung Barat Daya)
    "V9":  (5.0, -2.4),   # Terminal Amplas (Ujung Tenggara)
}

# Skenario Test Cases Resmi Validasi Manual A2
test_cases = [
    ("V1", "V11", ["V1", "V2", "V5", "V11"], 16.8),
    ("V1", "V8", ["V1", "V2", "V5", "V8"], 28.9),
    ("V10", "V10", ["V10"], 0.0)
]
