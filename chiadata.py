import os
import shutil
import random
import json

# 1. Cấu hình đường dẫn
root_dir = 'data_daxuli'
source_dir = os.path.join(root_dir, 'test_new')
manifest_src = os.path.join(source_dir, 'manifest.json')

splits = {'train': 0.7, 'validation': 0.15, 'test': 0.15}

if not os.path.exists(manifest_src):
    print(f"Không tìm thấy file nguồn: {manifest_src}")
    exit()

with open(manifest_src, 'r', encoding='utf-8') as f:
    full_manifest = json.load(f)

image_files = list(full_manifest.keys())
random.seed(42)
random.shuffle(image_files)

# 2. Chia file
total = len(image_files)
train_end = int(total * splits['train'])
val_end = train_end + int(total * splits['validation'])

split_files = {
    'train': image_files[:train_end],
    'validation': image_files[train_end:val_end],
    'test': image_files[val_end:]
}

# 3. Thực hiện nối tiếp (Append) dữ liệu
for split_name, files in split_files.items():
    target_path = os.path.join(root_dir, split_name)
    manifest_dest = os.path.join(target_path, 'manifest.json')
    os.makedirs(target_path, exist_ok=True)
    
    # --- Đọc dữ liệu cũ ---
    current_data = []
    if os.path.exists(manifest_dest):
        try:
            with open(manifest_dest, 'r', encoding='utf-8') as f:
                current_data = json.load(f)
        except json.JSONDecodeError:
            current_data = []

    # Tạo một group mới cho đợt import này từ test_new
    new_group = {
        "sample": f"from_test_new_{random.randint(100, 999)}",
        "images": []
    }

    for img_name in files:
        src_img_path = os.path.join(source_dir, img_name)
        dst_img_path = os.path.join(target_path, img_name)
        
        if os.path.exists(src_img_path):
            shutil.move(src_img_path, dst_img_path)
            
            img_info = {
                "split": split_name,
                "new_sample": new_group["sample"],
                "image_name": img_name,
                "image": f"{split_name}/{img_name}",
                "text": full_manifest[img_name]
            }
            new_group["images"].append(img_info)

    # --- Nối tiếp dữ liệu mới vào List cũ ---
    if new_group["images"]:
        current_data.append(new_group)

    # Ghi lại file manifest.json (đã bao gồm cả cũ và mới)
    with open(manifest_dest, 'w', encoding='utf-8') as f:
        json.dump(current_data, f, ensure_ascii=False, indent=2)

print("Đã nối tiếp dữ liệu từ test_new vào các file manifest cũ thành công!")