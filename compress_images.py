
import os
from PIL import Image

start_dir = r'd:\doctor_xcx\static\product_images\235443596'

print(f"Compressing images in {start_dir}...")

for filename in os.listdir(start_dir):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        full_path = os.path.join(start_dir, filename)
        try:
            with Image.open(full_path) as img:
                # Convert to RGB (if png)
                if img.mode in ("RGBA", "P"): 
                    img = img.convert("RGB")
                
                # Resize if too big (width > 800)
                if img.width > 800:
                   ratio = 800 / img.width
                   new_height = int(img.height * ratio)
                   img = img.resize((800, new_height), Image.Resampling.LANCZOS)
                
                # Save with compression
                img.save(full_path, "JPEG", quality=70, optimize=True)
                print(f"Compressed: {filename}")
        except Exception as e:
            print(f"Failed to compress {filename}: {e}")

print("Compression complete.")
