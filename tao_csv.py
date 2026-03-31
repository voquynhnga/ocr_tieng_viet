import json
import csv
from pathlib import Path

BASE_DIR = Path.cwd() / "data_daxuli"
SPLITS = ["train", "test", "validation", "test_new"]

for split in SPLITS:
    manifest_path = BASE_DIR / split / "manifest.json"
    output_csv = BASE_DIR / f"{split}_labels.csv"
    
    if not manifest_path.exists():
        print(f"[SKIP] Not found: {manifest_path}")
        continue
    
    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    rows = []

    # TRƯỜNG HỢP 1: Cấu trúc của test_new (Dictionary)
    if isinstance(data, dict):
        for img_name, text in data.items():
            # Giả định đường dẫn ảnh nằm trong thư mục của split đó
            # e.g. "data_daxuli/test_new/1.jpg"
            img_rel = Path(split) / img_name
            img_abs = BASE_DIR / img_rel
            
            rows.append({
                "image_path": str(img_abs),
                "text": text,
                "exists": img_abs.exists(),
                "group": "", # test_new không có 'sample' group rõ ràng nên đặt mặc định
            })

    # TRƯỜNG HỢP 2: Cấu trúc của train, test, validation (List)
    elif isinstance(data, list):
        for sample in data:
            group = sample.get("sample", "unknown")
            for img in sample.get("images", []):
                img_rel = img["image"]
                img_abs = BASE_DIR / img_rel
                
                rows.append({
                    "image_path": str(img_abs),
                    "text": img["text"],
                    "exists": img_abs.exists(),
                    "group": group,
                })
    
    # Ghi file CSV
    if rows:
        with open(output_csv, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["image_path", "text", "exists", "group"])
            writer.writeheader()
            writer.writerows(rows)
        print(f"[OK] {output_csv} ({len(rows)} rows)")
    else:
        print(f"[WARN] No data found for {split}")

print("Done.")