"""
Program Utama: Smart Route Optimization (Shortest Path)
Mata Kuliah: 3KOM40106 - Matematika Diskrit
Studi Kasus: Peta Jaringan Rute Strategis Kota Medan (11 Simpul, 19 Sisi)
Sumber Dataset: TomTom Routing API (Peran A2)

Fitur Utama:
1. Menampilkan daftar lokasi dan graf ketetanggaan Kota Medan
2. Menerima input Titik Awal & Titik Tujuan dari pengguna
3. Menjalankan Algoritma Dijkstra dan mencetak rute terpendek & rincian per segmen
4. Menampilkan log langkah iterasi matematis (Relaksasi Sisi & Himpunan S)
5. Membangkitkan visualisasi grafik rute terpendek presisi tinggi tanpa tabrakan label
"""

import sys
from graph_data import GRAPH, NODE_NAMES, POSITIONS
from dijkstra import dijkstra

# Konfigurasi penempatan label nama lokasi (dx, dy, horizontal_alignment, vertical_alignment)
NODE_LABEL_CONFIG = {
    "V1":  (0.0, 0.48, 'center', 'bottom'),     # Marelan: Di atas
    "V2":  (-0.45, 0.42, 'right', 'bottom'),    # Lap. Merdeka: Di kiri-atas
    "V3":  (0.0, 0.48, 'center', 'bottom'),     # Thamrin: Di atas
    "V6":  (0.0, 0.48, 'center', 'bottom'),     # Centre Point: Di atas
    "V10": (0.45, 0.0, 'left', 'center'),       # Unimed: Di kanan
    "V4":  (0.0, -0.48, 'center', 'top'),       # Istana Maimun: Di bawah
    "V11": (-0.45, 0.0, 'right', 'center'),     # Cambridge: Di kiri
    "V5":  (-0.45, -0.35, 'right', 'top'),      # Sun Plaza: Di kiri-bawah
    "V7":  (-0.45, -0.25, 'right', 'top'),      # USU: Di kiri-bawah
    "V8":  (0.0, -0.48, 'center', 'top'),       # RSUP Adam Malik: Di bawah
    "V9":  (0.0, -0.48, 'center', 'top'),       # Terminal Amplas: Di bawah
}

# Orientasi kelengkungan sisi jalur jauh (rad)
CURVED_EDGES = {
    ("V1", "V10"): 0.30,
    ("V10", "V1"): -0.30,
    ("V11", "V10"): 0.38,
    ("V10", "V11"): -0.38,
    ("V7", "V10"): -0.32,
    ("V10", "V7"): 0.32,
    ("V8", "V5"): -0.22,
    ("V5", "V8"): 0.22,
}

# Faktor posisi label sepanjang sisi t in (0, 1)
EDGE_LABEL_T = {
    ("V1", "V10"): 0.50,
    ("V11", "V10"): 0.50,
    ("V7", "V10"): 0.50,
    ("V8", "V5"): 0.50,
    ("V2", "V3"): 0.50,
    ("V2", "V4"): 0.50,
    ("V3", "V6"): 0.50,
    ("V4", "V6"): 0.50,
    ("V5", "V7"): 0.50,
    ("V7", "V11"): 0.50,
    ("V7", "V8"): 0.50,
    ("V8", "V9"): 0.50,
    ("V9", "V10"): 0.50,
    ("V4", "V10"): 0.50,
    ("V6", "V10"): 0.50,
    ("V1", "V2"): 0.50,
    ("V1", "V3"): 0.48,
    ("V2", "V5"): 0.50,
    ("V5", "V11"): 0.50,
}

def get_arc3_point(p0, p1, rad, t=0.5):
    """Menghitung koordinat eksak titik pada kurva bezier arc3 matplotlib pada parameter t."""
    x0, y0 = p0
    x1, y1 = p1
    if rad == 0:
        return (x0 + t * (x1 - x0), y0 + t * (y1 - y0))
    dx = x1 - x0
    dy = y1 - y0
    xc = (x0 + x1)/2.0 - rad * dy
    yc = (y0 + y1)/2.0 + rad * dx
    
    xt = (1-t)**2 * x0 + 2*(1-t)*t * xc + t**2 * x1
    yt = (1-t)**2 * y0 + 2*(1-t)*t * yc + t**2 * y1
    return (xt, yt)

def print_banner():
    print("=" * 75)
    print("      SMART ROUTE OPTIMIZATION - SISTEM RUTE TERPENDEK KOTA MEDAN")
    print("       Implementasi Algoritma Dijkstra (Matematika Diskrit)")
    print("=" * 75)

def print_available_nodes():
    print("\n📍 DAFTAR SIMPUL LOKASI KOTA MEDAN (V):")
    print("-" * 75)
    for node_id, node_name in NODE_NAMES.items():
        neighbors = [f"{nb} ({w} km)" for nb, w in GRAPH[node_id].items()]
        neighbors_str = ", ".join(neighbors)
        print(f"  [{node_id:3s}] {node_name:<28s} -> Terhubung ke: {neighbors_str}")
    print("-" * 75)

def display_route_summary(start_node, end_node, path, total_dist, logs):
    print("\n" + "═" * 75)
    print("                 HASIL PERHITUNGAN RUTE TERPENDEK")
    print("═" * 75)
    
    if not path:
        print(f"❌ Tidak ditemukan jalur dari [{start_node}] ke [{end_node}].")
        return

    start_name = NODE_NAMES.get(start_node, start_node)
    end_name = NODE_NAMES.get(end_node, end_node)
    
    print(f" Titik Awal   : [{start_node}] {start_name}")
    print(f" Titik Tujuan : [{end_node}] {end_name}")
    print("─" * 75)
    
    # Cetak Rute Lengkap
    path_formatted = " ➔ ".join([f"[{n}] {NODE_NAMES.get(n, n)}" for n in path])
    print(f" Rute Terpilih:\n  {path_formatted}")
    print("─" * 75)
    
    # Rincian Segmen Jarak
    print(" Rincian Segmen Perjalanan:")
    if len(path) == 1:
        print(f"  1. [{path[0]}] {NODE_NAMES[path[0]]} (Titik Awal = Titik Tujuan) : 0.0 km")
    else:
        accumulated = 0.0
        for i in range(len(path) - 1):
            u, v = path[i], path[i+1]
            weight = GRAPH[u][v]
            accumulated = round(accumulated + weight, 2)
            print(f"  {i+1}. [{u}] {NODE_NAMES[u]:<23s} ➔ [{v}] {NODE_NAMES[v]:<23s} : +{weight:.1f} km (Kumulatif: {accumulated:.1f} km)")
    
    print("─" * 75)
    print(f" TOTAL JARAK TERPENDEK : {total_dist:.1f} km")
    print("═" * 75)

def print_iteration_logs(logs):
    print("\n🔍 LOG LANGKAH ITERASI MATEMATIKA DISKRIT (DIJKSTRA):")
    print("-" * 75)
    print(f"{'Step':<6}{'Simpul (u)':<15}{'Jarak d(u)':<12}{'Himpunan S':<20}{'Pembaruan Tetangga'}")
    print("-" * 75)
    for entry in logs:
        step = entry["step"]
        node = f"[{entry['selected_node']}]"
        dist = f"{entry['current_distance']} km"
        s_set = "{" + ", ".join(sorted(list(entry["visited_set"]))) + "}"
        
        updates = []
        for upd in entry.get("updated_neighbors", []):
            updates.append(f"d({upd['neighbor']})={upd['new_distance']}km")
        updates_str = ", ".join(updates) if updates else "-"
        
        print(f"{step:<6}{node:<15}{dist:<12}{s_set:<20}{updates_str}")
    print("-" * 75)

def visualize_graph(path, total_dist, start_node="V1", end_node="V11", save_path="hasil_rute_graf.png"):
    """
    Visualisasi graf berkualitas tinggi dengan penempatan label presisi pada garis dan simpul.
    """
    try:
        import networkx as nx
        import matplotlib.pyplot as plt
        import matplotlib.patches as patches
    except ImportError:
        print("\n💡 Info: Modul 'networkx' dan 'matplotlib' tidak ditemukan.")
        print("   Gunakan venv proyek untuk membangkitkan visualisasi grafik.")
        return

    G = nx.Graph()
    for u in GRAPH:
        for v, w in GRAPH[u].items():
            G.add_edge(u, v, weight=w)

    fig, (ax, ax_info) = plt.subplots(1, 2, figsize=(18, 10), gridspec_kw={'width_ratios': [2.75, 1.25]})
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#FFFFFF')
    ax_info.set_facecolor('#EDF2F7')
    
    pos = POSITIONS
    
    path_edges_set = set()
    if path and len(path) > 1:
        for i in range(len(path)-1):
            path_edges_set.add((path[i], path[i+1]))
            path_edges_set.add((path[i+1], path[i]))
            
    # 1. Gambar Sisi (Edges) dan Label Bobot Eksak
    drawn_edges = set()
    for u, v, data in G.edges(data=True):
        if (u, v) in drawn_edges or (v, u) in drawn_edges:
            continue
        drawn_edges.add((u, v))
        
        w = data['weight']
        is_path = (u, v) in path_edges_set
        
        rad = CURVED_EDGES.get((u, v), 0.0)
        if rad == 0.0 and (v, u) in CURVED_EDGES:
            rad = -CURVED_EDGES[(v, u)]
            
        edge_color = "#E53E3E" if is_path else "#CBD5E0"
        width = 4.2 if is_path else 1.4
        style = "solid" if is_path else "dashed"
        alpha = 1.0 if is_path else 0.8
        zorder = 5 if is_path else 2
        
        arrow = patches.FancyArrowPatch(
            pos[u], pos[v],
            connectionstyle=f"arc3,rad={rad}",
            color=edge_color,
            linewidth=width,
            linestyle=style,
            alpha=alpha,
            zorder=zorder,
            arrowstyle='-'
        )
        ax.add_patch(arrow)
        
        t_param = EDGE_LABEL_T.get((u, v), EDGE_LABEL_T.get((v, u), 0.5))
        x_badge, y_badge = get_arc3_point(pos[u], pos[v], rad, t=t_param)
        
        badge_bg = "#FFF5F5" if is_path else "#FFFFFF"
        badge_border = "#FEB2B2" if is_path else "#E2E8F0"
        text_color = "#C53030" if is_path else "#4A5568"
        font_weight = "bold" if is_path else "normal"
        
        ax.text(x_badge, y_badge, f"{w:.1f} km", fontsize=8, fontweight=font_weight,
                color=text_color, ha='center', va='center', zorder=6,
                bbox=dict(boxstyle="round,pad=0.22", facecolor=badge_bg, edgecolor=badge_border, alpha=0.95, linewidth=0.8))

    # 2. Gambar Simpul (Nodes)
    for n in G.nodes():
        x, y = pos[n]
        if n in path:
            if n == path[0] and n == path[-1]:
                bg_col = "#38A169" # Start = Goal (Hijau)
                border_col = "#22543D"
            elif n == path[0]:
                bg_col = "#38A169" # Titik Awal (Hijau)
                border_col = "#22543D"
            elif n == path[-1]:
                bg_col = "#E53E3E" # Titik Tujuan (Merah)
                border_col = "#742A2A"
            else:
                bg_col = "#3182CE" # Simpul Rute (Biru)
                border_col = "#2B6CB0"
            text_col = "#FFFFFF"
        else:
            bg_col = "#EDF2F7"
            border_col = "#4A5568"
            text_col = "#2D3748"
            
        circle = plt.Circle((x, y), 0.28, facecolor=bg_col, edgecolor=border_col, linewidth=2.0, zorder=8)
        ax.add_patch(circle)
        ax.text(x, y, n, fontsize=10, fontweight="bold", color=text_col, ha='center', va='center', zorder=9)

    # 3. Gambar Label Nama Lokasi (Menempel di Dekat Simpul)
    for n, (dx, dy, ha, va) in NODE_LABEL_CONFIG.items():
        x, y = pos[n]
        name = NODE_NAMES[n]
        is_in_path = n in path
        fw = "bold" if is_in_path else "normal"
        fc = "#1A365D" if is_in_path else "#4A5568"
        box_bg = "#EBF8FF" if is_in_path else "#FFFFFF"
        box_border = "#3182CE" if is_in_path else "#CBD5E0"
        
        ax.text(x + dx, y + dy, name, fontsize=8.5, fontweight=fw, color=fc, ha=ha, va=va, zorder=10,
                bbox=dict(boxstyle="round,pad=0.25", facecolor=box_bg, edgecolor=box_border, alpha=0.95, linewidth=1.1 if is_in_path else 0.7))

    ax.set_xlim(-7.2, 8.8)
    ax.set_ylim(-4.0, 7.0)
    ax.set_aspect('equal')
    ax.set_title("TOPOLOGI GRAF BERBOBOT & RUTE OPTIMAL KOTA MEDAN\n(Implementasi Algoritma Dijkstra - Matematika Diskrit)", 
                 fontsize=13, fontweight='bold', color="#1A365D", pad=15)
    ax.axis("off")
    
    # 4. Info Panel Sisi Kanan (Kartu Ringkasan & Legenda)
    ax_info.axis("off")
    card_bg = patches.FancyBboxPatch((0.02, 0.02), 0.96, 0.96,
                                     boxstyle="round,pad=0.03,rounding_size=0.04",
                                     facecolor="#FFFFFF", edgecolor="#CBD5E0", linewidth=1.2,
                                     transform=ax_info.transAxes, zorder=1)
    ax_info.add_patch(card_bg)
    
    start_label = NODE_NAMES.get(start_node, start_node)
    end_label = NODE_NAMES.get(end_node, end_node)
    
    info_lines = [
        "================================",
        "     HASIL OPTIMASI RUTE",
        "================================",
        f"Titik Awal   : [{start_node}] {start_label}",
        f"Titik Tujuan : [{end_node}] {end_label}",
        f"Total Jarak  : {total_dist:.1f} km",
        "--------------------------------",
        "Rute Terpilih (Shortest Path):"
    ]
    
    if len(path) == 1:
        info_lines.append(f" 1. [{path[0]}] {NODE_NAMES.get(path[0], path[0])} (0.0 km)")
    else:
        for i in range(len(path) - 1):
            u, v = path[i], path[i+1]
            w = GRAPH[u][v]
            info_lines.append(f" {i+1}. [{u}] -> [{v}] ({w:.1f} km)")
        
    info_lines.append("--------------------------------")
    info_lines.append("LEGENDA SIMPUL (V):")
    for n in sorted(NODE_NAMES.keys(), key=lambda x: int(x[1:])):
        if n == start_node and n == end_node:
            tag = "[START/GOAL]"
        elif n == start_node:
            tag = "[START]"
        elif n == end_node:
            tag = "[GOAL]"
        elif n in path:
            tag = "[RUTE]"
        else:
            tag = "[LOKASI]"
        info_lines.append(f"{n:3s}: {NODE_NAMES[n]:<22s} {tag}")
    info_lines.append("================================")
    info_lines.append("Total Simpul: 11 | Total Sisi: 19")
    info_lines.append("Sumber Data : TomTom Routing API")
    info_lines.append("================================")
    
    ax_info.text(0.06, 0.95, "\n".join(info_lines), transform=ax_info.transAxes, fontsize=8.2, verticalalignment='top', 
                 fontfamily='monospace', color="#1A202C", linespacing=1.22, zorder=2)
                 
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"\n🖼️  Visualisasi graf presisi tinggi berhasil disimpan sebagai: '{save_path}'")

def run_interactive():
    print_banner()
    print_available_nodes()
    
    while True:
        print("\n--- PILIH RUTE PERJALANAN ---")
        start = input("Masukkan ID Simpul Titik Awal (misal V1) [ketik 'q' untuk keluar]: ").strip().upper()
        if start == 'Q':
            print("\nTerima kasih! Program selesai.")
            break
            
        if start not in GRAPH:
            print(f"⚠️ Simpul '{start}' tidak valid. Silakan pilih ID dari V1 hingga V11.")
            continue
            
        end = input("Masukkan ID Simpul Titik Tujuan (misal V11): ").strip().upper()
        if end not in GRAPH:
            print(f"⚠️ Simpul '{end}' tidak valid. Silakan pilih ID dari V1 hingga V11.")
            continue
            
        # Eksekusi Algoritma Dijkstra
        path, total_dist, logs = dijkstra(GRAPH, start, end)
        
        # Tampilkan Hasil
        display_route_summary(start, end, path, total_dist, logs)
        
        # Tanyakan apakah ingin melihat log matematis
        show_logs = input("\nTampilkan tabel log iterasi matematis? (y/n): ").strip().lower()
        if show_logs == 'y':
            print_iteration_logs(logs)
            
        # Bangkitkan visualisasi grafik jika diinginkan
        show_vis = input("Bangkitkan dan simpan file gambar graf visual? (y/n): ").strip().lower()
        if show_vis == 'y':
            filename = f"rute_{start}_ke_{end}.png"
            visualize_graph(path, total_dist, start_node=start, end_node=end, save_path=filename)

if __name__ == "__main__":
    run_interactive()
