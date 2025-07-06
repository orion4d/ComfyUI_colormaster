class AnnotateHexLines:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "hex_list": ("STRING", {"multiline": True}),
                "prefix": ("STRING", {"default": "(", "multiline": False}),
                "suffix": ("STRING", {"default": ")", "multiline": False}),
                "space": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("annotated_list",)
    FUNCTION = "annotate"
    CATEGORY = "Colormaster"

    def annotate(self, hex_list, prefix="(", suffix=")", space=True):
        lines = hex_list.strip().splitlines()
        spacer = " " if space else ""
        annotated = [
            f"{prefix}{i+1}{suffix}{spacer}{line.strip()}"
            for i, line in enumerate(lines)
        ]
        return ("\n".join(annotated),)

NODE_CLASS_MAPPINGS = {
    "AnnotateHexLines": AnnotateHexLines
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "AnnotateHexLines": "🧮 Annotate Hex Lines"
}
