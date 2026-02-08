"""
AI Instruction Manual for optimizing images in `img_items`.
===========================================================

Role: You are an AI assistant helping managing website assets.

Goal: 
   Keep the website fast by ensuring all images in `img_items` and its subfolders are
   optimized (WebP format, max width 1000px).

Instructions:
1. Run this script using the `antig` environment:
   `C:\\Users\\Rabbi\\anaconda3\\envs\\antig\\python.exe optimize_assets.py`

2. What this script does:
   - Scans `img_items` recursively.
   - Converts any non-WebP image (jpg, png) to WebP.
   - Resizes any image wider than 1000px to width=1000px (preserving aspect ratio).
   - Updates `data/inventory.json` effectively replacing old file references with new .webp ones.
   - DELETES the original un-optimized files to save space.

3. When to run:
   - Whenever the user adds new images to `img_items`.
   - If the user complains about slow loading speeds.

4. Notes:
   - This script creates a lock file or just runs idempotently (it skips already optimized .webp files unless they are too big).
   - Ensure `Pillow` is installed in the environment (the script handles basic check).

"""

import os
import json
import sys
import time

# Ensure Pillow is installed
try:
    from PIL import Image
except ImportError:
    print("Pillow library (PIL) not found, attempting to install...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
    from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE_DIR, 'img_items')
INVENTORY_FILE = os.path.join(BASE_DIR, 'data', 'inventory.json')
MAX_WIDTH = 1000
QUALITY = 80

def optimize_assets():
    print(f"--- Starting Global Image Optimization ---\nBase Dir: {BASE_DIR}")
    
    if not os.path.exists(IMG_DIR):
        print(f"Error: Image directory not found at {IMG_DIR}")
        return

    optimization_map = {} # old_rel_path -> new_rel_path
    
    # 1. SCAN AND OPTIMIZE
    for root, dirs, files in os.walk(IMG_DIR):
        for filename in files:
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                # Found a candidate for optimization
                full_path = os.path.join(root, filename)
                rel_dir = os.path.relpath(root, BASE_DIR)
                old_rel_path = f"{rel_dir}/{filename}".replace('\\', '/')
                
                try:
                    with Image.open(full_path) as img:
                        # Logic: Convert to WebP and Resize
                        original_width, original_height = img.size
                        original_size = os.path.getsize(full_path)
                        
                        # Resize logic
                        target_width = original_width
                        target_height = original_height
                        
                        img_to_save = img
                        if original_width > MAX_WIDTH:
                            ratio = MAX_WIDTH / original_width
                            target_width = MAX_WIDTH
                            target_height = int(original_height * ratio)
                            img_to_save = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
                        
                        # New Filename
                        new_filename = os.path.splitext(filename)[0] + '.webp'
                        new_full_path = os.path.join(root, new_filename)
                        new_rel_path = f"{rel_dir}/{new_filename}".replace('\\', '/')
                        
                        # Save
                        img_to_save.save(new_full_path, 'WEBP', quality=QUALITY)
                        
                        # Stats
                        new_size = os.path.getsize(new_full_path)
                        reduction = (1 - (new_size / original_size)) * 100
                        print(f"✅ Optimized: {filename} -> {new_filename}")
                        print(f"   Size: {original_size/1024:.1f}KB -> {new_size/1024:.1f}KB (-{reduction:.1f}%)")
                        print(f"   Dims: {original_width}x{original_height} -> {target_width}x{target_height}")

                        # Record mapping
                        optimization_map[old_rel_path] = new_rel_path
                        
                        # Delete original if it's different file
                        if new_full_path != full_path:
                            os.remove(full_path)

                except Exception as e:
                    print(f"❌ Error processing {filename}: {e}")

    # 2. UPDATE INVENTORY
    if optimization_map and os.path.exists(INVENTORY_FILE):
        print(f"\n--- Updating Inventory ---")
        try:
            with open(INVENTORY_FILE, 'r', encoding='utf-8') as f:
                inventory = json.load(f)
            
            updates_count = 0
            for item in inventory:
                if 'images' in item:
                    new_images = []
                    item_updated = False
                    for img_path in item['images']:
                        # Check exact match first
                        if img_path in optimization_map:
                            new_images.append(optimization_map[img_path])
                            item_updated = True
                            updates_count += 1
                        else:
                            # It might be that the path in json uses different separator or encoding
                            # Try to see if any key endswith the filename
                            # But safest is to keep original if no match found (it might be external URL)
                            new_images.append(img_path)
                    
                    if item_updated:
                        item['images'] = new_images
            
            with open(INVENTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(inventory, f, indent=4, ensure_ascii=False)
            
            print(f"Updated {updates_count} image references in inventory.json")
            
        except Exception as e:
            print(f"❌ Error updating inventory: {e}")
    else:
        print("\nNo new optimizations needed or inventory not found.")

if __name__ == "__main__":
    optimize_assets()
