"""
Script Pengujian Otomatis (Automated Test Runner)
Untuk memverifikasi 3 Test Case resmi proyek Smart Route Optimization - Kota Medan.
Data Skenario dan Hasil Acuan berasal dari perhitungan manual peran A2 (Data & Model Specialist).
"""

from graph_data import GRAPH, NODE_NAMES, test_cases
from dijkstra import dijkstra

TEST_CASES_DETAILED = [
    {
        "id": 1,
        "name": "Kasus Normal (Marelan Square ke Cambridge City Square)",
        "start": "V1",
        "end": "V11",
        "expected_path": ["V1", "V2", "V5", "V11"],
        "expected_dist": 16.8
    },
    {
        "id": 2,
        "name": "Kasus Kompleks / Terjauh (Marelan Square ke RSUP H. Adam Malik)",
        "start": "V1",
        "end": "V8",
        "expected_path": ["V1", "V2", "V5", "V8"],
        "expected_dist": 28.9
    },
    {
        "id": 3,
        "name": "Kasus Batas / Titik Sama (Unimed Kampus 1 ke Unimed Kampus 1)",
        "start": "V10",
        "end": "V10",
        "expected_path": ["V10"],
        "expected_dist": 0.0
    }
]

def run_all_tests():
    print("=" * 80)
    print("        EKSEKUSI PENGUJIAN OTOMATIS TEST CASES (DATASET KOTA MEDAN)")
    print("=" * 80)
    
    passed_count = 0
    
    for tc in TEST_CASES_DETAILED:
        tc_id = tc["id"]
        tc_name = tc["name"]
        start = tc["start"]
        end = tc["end"]
        exp_path = tc["expected_path"]
        exp_dist = tc["expected_dist"]
        
        path, dist, logs = dijkstra(GRAPH, start, end)
        
        path_match = (path == exp_path)
        dist_match = (abs(dist - exp_dist) < 1e-6)
        is_pass = path_match and dist_match
        
        if is_pass:
            passed_count += 1
            status_str = "✅ PASS (SESUAI)"
        else:
            status_str = "❌ FAIL (TIDAK SESUAI)"
            
        print(f"\n[Test Case {tc_id}] {tc_name}")
        print(f"  Titik Uji        : [{start}] {NODE_NAMES[start]} ➔ [{end}] {NODE_NAMES[end]}")
        print(f"  Expected Path    : {' -> '.join(exp_path)} (Jarak: {exp_dist:.1f} km)")
        print(f"  Actual Path      : {' -> '.join(path)} (Jarak: {dist:.1f} km)")
        print(f"  Status Pengujian : {status_str}")
        
    print("\n" + "=" * 80)
    print(f" HASIL AKHIR: {passed_count}/{len(TEST_CASES_DETAILED)} Test Cases Berhasil Lolos 100%.")
    print("=" * 80)

if __name__ == "__main__":
    run_all_tests()
