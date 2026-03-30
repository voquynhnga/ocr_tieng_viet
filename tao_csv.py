import json
import csv
import os
from pathlib import Path

BASE_DIR = Path.cwd() / "data_daxuli"  # Adjust if your data is in a different location
SPLITS = ["train", "test", "validation"]

for split in SPLITS:
    manifest_path = BASE_DIR / split / "manifest.json"
    output_csv = BASE_DIR / f"{split}_labels.csv"
    
    if not manifest_path.exists():
        print(f"[SKIP] Not found: {manifest_path}")
        continue
    
    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    rows = []
    for sample in data:
        group = sample["sample"]  # e.g. "test_001"
        for img in sample["images"]:
            # Build absolute path
            img_rel = img["image"]  # e.g. "test/test_001/1.jpg"
            img_abs = BASE_DIR / img_rel
            text = img["text"]
            exists = img_abs.exists()
            rows.append({
                "image_path": str(img_abs),
                "text": text,
                "exists": exists,
                "group": group,
            })
    
    with open(output_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["image_path", "text", "exists", "group"])
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"[OK] {output_csv}  ({len(rows)} rows)")

print("Done.")