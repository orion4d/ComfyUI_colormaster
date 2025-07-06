import torch
import numpy as np
from PIL import Image

class HexColorToImage:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "hex_color": ("STRING", {"default": "#ffffff"}),
                "width": ("INT", {"default": 1024, "min": 1, "max": 8192}),
                "height": ("INT", {"default": 1024, "min": 1, "max": 8192}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "create_image"
    CATEGORY = "Colormaster"          # même rubrique que l’autre node

    # ---------- util ----------
    def hex_to_rgb(self, hex_code):
        h = hex_code.lstrip("#")
        if len(h) == 3:                # ex : #f0a → #ff00aa
            h = "".join(c * 2 for c in h)
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

    # ---------- logique principale ----------
    def create_image(self, hex_color, width, height):
        try:
            rgb = self.hex_to_rgb(hex_color)
        except Exception:
            rgb = (255, 255, 255)      # fallback blanc si mauvais hex

        pil_img = Image.new("RGB", (width, height), rgb)

        # PIL → numpy → tensor (B, H, W, C) float32 entre 0-1
        np_img = np.array(pil_img).astype(np.float32) / 255.0          # (H, W, C)
        t_img = torch.from_numpy(np_img)                               # (H, W, C)
        t_img = t_img.unsqueeze(0)                                     # (1, H, W, C)

        return (t_img,)

# ---------- mappings ----------
NODE_CLASS_MAPPINGS = {
    "HexColorToImage": HexColorToImage
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "HexColorToImage": "🟥 Hex Color → Image"
}
