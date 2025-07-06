import numpy as np
from PIL import Image, ImageDraw, ImageFont
from sklearn.cluster import KMeans
import torch
import math

def tensor2pil(images):
    out = []
    for img_tensor in images:
        img_np = (img_tensor * 255.0).clamp(0, 255).cpu().numpy().astype(np.uint8)
        if img_np.shape[2] == 1:
            img_np = np.repeat(img_np, 3, axis=2)
        image = Image.fromarray(img_np, mode="RGB")
        out.append(image)
    return out

def pil2tensor(images):
    if not isinstance(images, list):
        images = [images]
    out = []
    for image in images:
        img_np = np.array(image).astype(np.float32) / 255.0
        img_tensor = torch.from_numpy(img_np)
        out.append(img_tensor)
    return torch.stack(out, dim=0)

class ColorPaletteExtractor:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "num_colors": ("INT", {"default": 6, "min": 1, "max": 20}),
                "resolution": ("INT", {"default": 1024, "min": 100, "max": 4096}),
                "style": (["grid", "line"],),
                "show_hex": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("STRING", "IMAGE")
    RETURN_NAMES = ("hex_palette", "preview")
    FUNCTION = "extract_palette"
    CATEGORY = "Colormaster"

    def extract_palette(self, image, num_colors=6, resolution=1024, style="grid", show_hex=True):
        img = tensor2pil(image)[0].resize((150, 150))
        pixels = np.array(img).reshape(-1, 3)

        kmeans = KMeans(n_clusters=num_colors, n_init="auto", random_state=0)
        kmeans.fit(pixels)
        colors = sorted(kmeans.cluster_centers_, key=lambda c: 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2])
        hex_colors = ['#%02x%02x%02x' % tuple(map(int, color)) for color in colors]

        try:
            font = ImageFont.truetype("arial.ttf", resolution // 40)
        except:
            font = ImageFont.load_default()

        if style == "line":
            sw = resolution // num_colors
            sh = sw // 2
            pw, ph = sw * num_colors, sh
        else:  # style == "grid"
            cols = math.ceil(math.sqrt(num_colors))
            rows = math.ceil(num_colors / cols)
            sw = resolution // cols
            sh = sw // 2
            pw, ph = sw * cols, sh * rows

        preview = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
        draw = ImageDraw.Draw(preview)

        for i in range(num_colors):
            color = tuple(map(int, colors[i])) + (255,)

            if style == "line":
                x = i * sw
                y = 0
            else:
                x = (i % cols) * sw
                y = (i // cols) * sh

            block = Image.new("RGBA", (sw, sh), color)
            preview.paste(block, (x, y))

            if show_hex:
                text = hex_colors[i]
                bbox = draw.textbbox((0, 0), text, font=font)
                tw = bbox[2] - bbox[0]
                th = bbox[3] - bbox[1]
                draw.text(
                    (x + (sw - tw) / 2, y + (sh - th) / 2),
                    text,
                    fill=(255, 255, 255, 255),
                    font=font
                )

        return ("\n".join(hex_colors), pil2tensor(preview))

NODE_CLASS_MAPPINGS = {
    "ColorPaletteExtractor": ColorPaletteExtractor
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ColorPaletteExtractor": "🎨 Color Palette Extractor"
}
