import os
from PIL import Image

def check_dimensions(directory_path):
    print(f"Checking images in: {directory_path}")
    for filename in os.listdir(directory_path):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            file_path = os.path.join(directory_path, filename)
            try:
                with Image.open(file_path) as img:
                    width, height = img.size
                    ratio = width / height
                    print(f"{filename}: {width}x{height} (Ratio: {ratio:.2f})")
            except Exception as e:
                print(f"Error reading {filename}: {e}")

if __name__ == "__main__":
    check_dimensions(r'C:\Users\Rabbi\Desktop\Tawhid\tahwillclothing-oss.github.io\img_items\Jersey')
