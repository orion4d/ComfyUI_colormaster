class SelectHexLine:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "hex_list": ("STRING", {"multiline": True}),
                "line_number": ("INT", {"default": 1, "min": 1, "step": 1}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("selected_hex",)
    FUNCTION = "select_line"
    CATEGORY = "Colormaster"

    def select_line(self, hex_list, line_number):
        lines = hex_list.strip().splitlines()
        if 0 < line_number <= len(lines):
            return (lines[line_number - 1].strip(),)
        else:
            return ("#000000",)  # fallback

NODE_CLASS_MAPPINGS = {
    "SelectHexLine": SelectHexLine
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "SelectHexLine": "🎯 Select Hex Line"
}
