import torch
import numpy as np
from PIL import Image

class ImageCollageNode:
    @classmethod
    def INPUT_TYPES(cls):
        # La correction principale est ici :
        # On sépare les entrées "requises" (obligatoires) des "optionnelles".
        # Les entrées d'image sont maintenant optionnelles, ce qui permet au
        # node de fonctionner même si seulement une ou quelques-unes sont connectées.
        return {
            "required": {
                "direction": (["horizontal", "vertical"], {"default": "horizontal"}),
                "spacing": ("INT", {"default": 0, "min": 0, "max": 512}),
            },
            "optional": {
                # Crée 8 entrées d'image optionnelles : image_1, image_2, ...
                f"image_{i+1}": ("IMAGE",) for i in range(8)
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "collage"
    CATEGORY = "Colormaster"

    def collage(self, direction, spacing, **kwargs):
        pil_images = []

        # On parcourt les entrées optionnelles dans l'ordre (de 1 à 8)
        # pour s'assurer que le collage est assemblé de manière prévisible.
        for i in range(1, 9):
            image_key = f"image_{i}"
            image_tensor = kwargs.get(image_key)

            # On vérifie si l'entrée d'image optionnelle est connectée (non nulle)
            if image_tensor is not None:
                # Les tenseurs de ComfyUI sont au format (batch, hauteur, largeur, canaux)
                # On prend la première image du batch
                img_np = image_tensor[0].cpu().numpy()
                # On convertit les valeurs de float (0-1) à uint8 (0-255) pour la librairie PIL
                pil_images.append(Image.fromarray((img_np * 255).astype(np.uint8)))

        if not pil_images:
            # S'il n'y a aucune image connectée, on ne peut pas créer de collage.
            # Lancer une erreur est le comportement le plus clair.
            raise ValueError("Le node Image Collage nécessite au moins une image connectée.")

        if direction == 'horizontal':
            # Calcul de la largeur totale et de la hauteur maximale de l'image finale
            # On ne compte l'espacement qu'entre les images
            total_width = sum(img.width for img in pil_images) + spacing * (len(pil_images) - 1 if len(pil_images) > 0 else 0)
            max_height = max(img.height for img in pil_images)
            
            # Création d'une nouvelle image vide avec un fond blanc
            result = Image.new("RGB", (total_width, max_height), (255, 255, 255))

            x_offset = 0
            for img in pil_images:
                # On centre les images verticalement si elles ont des hauteurs différentes
                y_offset = (max_height - img.height) // 2
                result.paste(img, (x_offset, y_offset))
                x_offset += img.width + spacing

        else:  # direction == 'vertical'
            # Calcul de la hauteur totale et de la largeur maximale
            total_height = sum(img.height for img in pil_images) + spacing * (len(pil_images) - 1 if len(pil_images) > 0 else 0)
            max_width = max(img.width for img in pil_images)

            result = Image.new("RGB", (max_width, total_height), (255, 255, 255))

            y_offset = 0
            for img in pil_images:
                # On centre les images horizontalement si elles ont des largeurs différentes
                x_offset = (max_width - img.width) // 2
                result.paste(img, (x_offset, y_offset))
                y_offset += img.height + spacing

        # Conversion de l'image PIL finale en tenseur pour ComfyUI
        result_np = np.array(result).astype(np.float32) / 255.0
        # On ajoute une dimension de batch pour correspondre au format standard (B, H, W, C)
        result_tensor = torch.from_numpy(result_np).unsqueeze(0)

        return (result_tensor,)


# --- Le reste du fichier ne change pas ---
NODE_CLASS_MAPPINGS = {
    "ImageCollageNode": ImageCollageNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageCollageNode": "Image Collage"
}