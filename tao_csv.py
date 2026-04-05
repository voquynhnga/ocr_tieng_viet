import json
import csv
from pathlib import Path

BASE_DIR = Path.cwd() / "data_daxuli"
SPLITS = ["train", "test", "validation"] # test_new thường sẽ trống sau khi chia nên có thể bỏ qua

for split in SPLITS:
    manifest_path = BASE_DIR / split / "manifest.json"
    output_csv = BASE_DIR / f"{split}_labels.csv"
    
    if not manifest_path.exists():
        print(f"[SKIP] Not found: {manifest_path}")
        continue
    
    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    rows = []

    # Xử lý cấu trúc List (cho cả dữ liệu cũ và dữ liệu mới từ test_new)
    if isinstance(data, list):
        for sample in data:
            # Lấy tên group (có thể là 'test_038' hoặc 'from_test_new_902')
            group_name = sample.get("sample", "unknown")
            
            for img_entry in sample.get("images", []):
                # 'image' trong JSON thường là "test/test_038/44.jpg" hoặc "test/0123.png"
                img_rel_path = img_entry.get("image")
                
                if img_rel_path:
                    # Đường dẫn tuyệt đối dựa trên BASE_DIR (data_daxuli)
                    img_abs = BASE_DIR / img_rel_path
                    
                    rows.append({
                        "image_path": str(img_abs),
                        "text": img_entry.get("text", ""),
                        "exists": img_abs.exists(),
                        "group": group_name,
                    })
    
    # Ghi file CSV
    if rows:
        with open(output_csv, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["image_path", "text", "exists", "group"])
            writer.writeheader()
            writer.writerows(rows)
        print(f"[OK] {output_csv} ({len(rows)} hàng)")
    else:
        print(f"[WARN] Không có dữ liệu hợp lệ trong {split}")

print("Hoàn thành tạo file CSV.")