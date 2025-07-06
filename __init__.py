# __init__.py

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

# Color Palette Extractor
try:
    from .color_palette_node import NODE_CLASS_MAPPINGS as PALETTE_CLASSES
    from .color_palette_node import NODE_DISPLAY_NAME_MAPPINGS as PALETTE_NAMES
    NODE_CLASS_MAPPINGS.update(PALETTE_CLASSES)
    NODE_DISPLAY_NAME_MAPPINGS.update(PALETTE_NAMES)
except Exception as e:
    print(f"[Colormaster] Erreur lors du chargement de color_palette_node: {e}")

# Hex Color to Image
try:
    from .hex_color_to_image import NODE_CLASS_MAPPINGS as HEXIMG_CLASSES
    from .hex_color_to_image import NODE_DISPLAY_NAME_MAPPINGS as HEXIMG_NAMES
    NODE_CLASS_MAPPINGS.update(HEXIMG_CLASSES)
    NODE_DISPLAY_NAME_MAPPINGS.update(HEXIMG_NAMES)
except Exception as e:
    print(f"[Colormaster] Erreur lors du chargement de hex_color_to_image: {e}")

# Select Hex Line
try:
    from .select_hex_line_node import NODE_CLASS_MAPPINGS as SELECT_HEX
    NODE_CLASS_MAPPINGS.update(SELECT_HEX)
    from .select_hex_line_node import NODE_DISPLAY_NAME_MAPPINGS as SELECT_HEX_NAME
    NODE_DISPLAY_NAME_MAPPINGS.update(SELECT_HEX_NAME)
except Exception as e:
    print(f"[Colormaster] Erreur chargement select_hex_line_node: {e}")

# Annotate Hex Lines
try:
    from .annotate_hex_lines_node import NODE_CLASS_MAPPINGS as ANNOTATE_HEX
    NODE_CLASS_MAPPINGS.update(ANNOTATE_HEX)
    from .annotate_hex_lines_node import NODE_DISPLAY_NAME_MAPPINGS as ANNOTATE_HEX_NAME
    NODE_DISPLAY_NAME_MAPPINGS.update(ANNOTATE_HEX_NAME)
except Exception as e:
    print(f"[Colormaster] Erreur chargement annotate_hex_lines_node: {e}")

# ImageCollageNode
try:
    from .image_collage_node import NODE_CLASS_MAPPINGS as COLLAGE_CLASSES
    from .image_collage_node import NODE_DISPLAY_NAME_MAPPINGS as COLLAGE_NAMES
    NODE_CLASS_MAPPINGS.update(COLLAGE_CLASSES)
    NODE_DISPLAY_NAME_MAPPINGS.update(COLLAGE_NAMES)
except Exception as e:
    print(f"[Colormaster] Erreur lors du chargement de image_collage_node: {e}")

