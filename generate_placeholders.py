import os
from PIL import Image, ImageDraw

def create_placeholders():
    img_dir = os.path.join('static', 'images')
    os.makedirs(img_dir, exist_ok=True)
    
    # 1. Create a beautiful gradient banner (800x400)
    banner_path = os.path.join(img_dir, 'default-banner.png')
    if not os.path.exists(banner_path):
        # Create gradient image (Indigo to Purple)
        banner = Image.new('RGB', (800, 400), '#6366f1')
        draw = ImageDraw.Draw(banner)
        # Draw a soft visual pattern
        for i in range(400):
            r = int(99 + (167 - 99) * (i / 400))
            g = int(102 + (139 - 102) * (i / 400))
            b = int(241 + (250 - 241) * (i / 400))
            draw.line([(0, i), (800, i)], fill=(r, g, b))
        
        # Add decorative circular shape
        draw.ellipse([450, -50, 950, 450], fill=(139, 92, 246, 128))
        banner.save(banner_path, 'PNG')
        print(f"Created default banner at {banner_path}")

    # 2. Create a default avatar (100x100)
    avatar_path = os.path.join(img_dir, 'default-avatar.png')
    if not os.path.exists(avatar_path):
        # Slate background with a user head profile representation
        avatar = Image.new('RGB', (100, 100), '#64748b')
        draw = ImageDraw.Draw(avatar)
        # Draw soft user shape
        # Head
        draw.ellipse([35, 20, 65, 50], fill='#e2e8f0')
        # Body
        draw.ellipse([15, 60, 85, 120], fill='#e2e8f0')
        avatar.save(avatar_path, 'PNG')
        print(f"Created default avatar at {avatar_path}")

if __name__ == '__main__':
    create_placeholders()
