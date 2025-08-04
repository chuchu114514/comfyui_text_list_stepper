# --------------------------------------------------------------------------------
# Gemini's Text List Processor Node for ComfyUI
#
# Author: Gemini
# Version: 2.0
#
# This node processes a text list. It allows splitting the text by various
# separators, selecting one or more items based on a starting seed,
# and joining the selected items back into a single string with a specified joiner.
# --------------------------------------------------------------------------------

class TextListProcessor:
    """
    A node that selects one or more items from a text list, with configurable
    separators and joiners. This allows for iterating through a list of prompts
    or parameters by setting the seed control to "increment".
    """
    
    @classmethod
    def INPUT_TYPES(s):
        """
        Defines the input types for the node.
        """
        # Define the separator options for the dropdown menu
        separator_options = ["Newline (\\n)", "Comma (,)", "Semicolon (;)", "Pipe (|)", "Space"]
        
        return {
            "required": {
                "text_list": ("STRING", {
                    "multiline": True,
                    "default": "Positive prompt A\nPositive prompt B\nPositive prompt C"
                }),
                "separator": (separator_options, ),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "selection_count": ("INT", {"default": 1, "min": 1, "max": 1024}), # How many items to select
                "join_with": ("STRING", {"multiline": False, "default": "\\n"}) # How to join the selected items
            }
        }

    # Define the output types and names
    RETURN_TYPES = ("STRING", "INT",)
    RETURN_NAMES = ("text", "start_index",)

    # The main function of the node
    FUNCTION = "process_list"

    # Set the category for the node in the ComfyUI menu
    CATEGORY = "Gemini/Text"

    def process_list(self, text_list: str, separator: str, seed: int, selection_count: int, join_with: str):
        """
        The core logic of the node.
        1. Splits the input string into a list based on the chosen separator.
        2. Handles empty or invalid lists gracefully.
        3. Selects 'selection_count' items starting from an index derived from the seed.
        4. Joins the selected items using the 'join_with' string.
        5. Returns the resulting text and the starting index.
        """
        # Map the dropdown option to the actual separator character
        separator_map = {
            "Newline (\\n)": "\n",
            "Comma (,)": ",",
            "Semicolon (;)": ";",
            "Pipe (|)": "|",
            "Space": " "
        }
        split_char = separator_map.get(separator, "\n")

        # Interpret escape sequences like \n in the join_with string
        # This allows user to type "\\n" in the UI to get a real newline
        processed_join_with = join_with.encode().decode('unicode_escape')

        # Split the string into a list and remove any empty or whitespace-only items
        items = [item.strip() for item in text_list.strip().split(split_char) if item.strip()]

        # If the list is empty, return an empty string and an invalid index
        if not items:
            return ("", -1)

        list_length = len(items)
        # Calculate the starting index using the modulo operator to cycle through the list
        start_index = seed % list_length
        
        selected_items = []
        for i in range(selection_count):
            # Calculate the index for each item to select, wrapping around the list
            current_index = (start_index + i) % list_length
            selected_items.append(items[current_index])
            
        # Join the selected items using the specified joiner string
        output_text = processed_join_with.join(selected_items)

        # Return the selected text and the starting index
        return (output_text, start_index)


# --------------------------------------------------------------------------------
# Node Mappings for ComfyUI
# --------------------------------------------------------------------------------
# This is the standard boilerplate that tells ComfyUI about the new node.
NODE_CLASS_MAPPINGS = {
    "TextListProcessor_Gemini": TextListProcessor
}

# This sets the display name of the node in the ComfyUI graph.
NODE_DISPLAY_NAME_MAPPINGS = {
    "TextListProcessor_Gemini": "Text List Processor (Gemini)"
}