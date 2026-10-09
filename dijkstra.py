"""
Modul Implementasi Algoritma Dijkstra (Shortest Path)
Konsep Matematika Diskrit:
1. Graf Berbobot G = (V, E, W)
2. Prinsip Greedy: Memilih simpul dengan jarak terkecil pada setiap iterasi
3. Relaksasi Sisi (Edge Relaxation): d(v) = min(d(v), d(u) + w(u, v))
4. Rekonstruksi Lintasan menggunakan Predecessor / Previous Node Tracking
"""

import heapq

def dijkstra(graph, start_node, end_node):
    """
    Menghitung rute terpendek dari start_node ke end_node dalam graf berbobot.
    
    Parameter:
    - graph (dict): Representasi graf dalam bentuk Adjacency List.
    - start_node (str): ID simpul titik awal (misal 'V1').
    - end_node (str): ID simpul titik tujuan (misal 'V11').
    
    Mengembalikan tuple:
    - path (list): Daftar simpul berurutan yang membentuk rute terpendek [start, ..., end].
    - total_distance (float): Total akumulasi bobot jarak terpendek (dalam km).
    - iteration_logs (list): Catatan langkah demi langkah untuk keperluan validasi manual.
    """
    
    # 1. Validasi Keberadaan Simpul
    if start_node not in graph or end_node not in graph:
        raise ValueError(f"Simpul '{start_node}' atau '{end_node}' tidak ditemukan dalam graf.")
        
    # Kasus Khusus: Titik awal sama dengan titik tujuan (Kasus Batas)
    if start_node == end_node:
        return [start_node], 0.0, [{"step": 1, "selected_node": start_node, "current_distance": 0.0, "visited_set": {start_node}, "updated_neighbors": []}]

    # 2. Inisialisasi Struktur Data
    # - distances: menyimpan estimasi jarak terpendek sementara d(v). Awalnya ∞ kecuali d(start)=0.
    distances = {node: float('inf') for node in graph}
    distances[start_node] = 0.0
    
    # - predecessors: menyimpan simpul pendahulu untuk rekonstruksi lintasan
    predecessors = {node: None for node in graph}
    
    # - visited: himpunan simpul yang jarak optimalnya sudah permanen (Himpunan S)
    visited = set()
    
    # - priority_queue: min-heap untuk mengambil simpul dengan jarak minimum secara efisien O(log V)
    #   Format elemen: (jarak_kumulatif, id_simpul)
    pq = [(0.0, start_node)]
    
    # - iteration_logs: mencatat riwayat langkah demi langkah (tabel iterasi matematika diskrit)
    iteration_logs = []
    step_counter = 1

    # 3. Loop Utama Algoritma Dijkstra (Prinsip Greedy)
    while pq:
        current_distance, current_node = heapq.heappop(pq)
        
        # Jika simpul sudah pernah diproses secara optimal, lewati
        if current_node in visited:
            continue
            
        # Tandai simpul saat ini sebagai sudah dikunjungi (masuk ke Himpunan S)
        visited.add(current_node)
        
        # Log iterasi saat ini
        log_entry = {
            "step": step_counter,
            "selected_node": current_node,
            "current_distance": round(current_distance, 2),
            "visited_set": set(visited),
            "updated_neighbors": []
        }
        
        # Jika kita telah mencapai titik tujuan, kita bisa berhenti (optimasi pencarian tujuan tunggal)
        if current_node == end_node:
            iteration_logs.append(log_entry)
            break
            
        # 4. Relaksasi Sisi (Edge Relaxation) untuk Setiap Tetangga
        for neighbor, weight in graph[current_node].items():
            if neighbor not in visited:
                new_distance = round(current_distance + weight, 2)
                
                # Sifat Matematis: d(neighbor) = min(d(neighbor), d(current) + w(current, neighbor))
                if new_distance < distances[neighbor]:
                    old_dist = distances[neighbor]
                    distances[neighbor] = new_distance
                    predecessors[neighbor] = current_node
                    heapq.heappush(pq, (new_distance, neighbor))
                    
                    log_entry["updated_neighbors"].append({
                        "neighbor": neighbor,
                        "old_distance": old_dist if old_dist != float('inf') else "∞",
                        "new_distance": new_distance,
                        "weight": weight
                    })
                    
        iteration_logs.append(log_entry)
        step_counter += 1

    # 5. Rekonstruksi Lintasan Terpendek (Backtracking dari End Node ke Start Node)
    path = []
    curr = end_node
    
    # Jika jarak ke end_node masih tak hingga, berarti tidak ada jalur yang menghubungkan
    if distances[end_node] == float('inf'):
        return [], float('inf'), iteration_logs
        
    while curr is not None:
        path.append(curr)
        curr = predecessors[curr]
        
    # Balikkan urutan lintasan sehingga dari Start -> ... -> End
    path.reverse()
    
    return path, round(distances[end_node], 2), iteration_logs
