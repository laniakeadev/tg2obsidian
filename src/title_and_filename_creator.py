import os
import logging
import re
from datetime import datetime
import json

config = ""

def initialize(config_path):
    global config
    config = load_config(config_path)

def get_filename_based_on_date_and_id(post_date, id):
    return str(post_date) + '-' + str(id) + '.md'

def get_default(post_date, id):
    return get_filename_based_on_date_and_id(post_date, id)


def get_filename_based_on_content(parsed_text, keep_duplicates, output_dir):

    first_line = parsed_text.strip()
    
    # remove extensions if it contains files
    first_line = first_line.replace('.ogg', '').replace('.mp4', '').replace('.jpg', '').replace('.mp4', '')
    
    # Format the file name
    filename_clean = trim(first_line)
    filename_clean = fix_invalid_filename(filename_clean)
    
    if keep_duplicates:
        base_name = filename_clean
        suffix = 1
        while os.path.exists(os.path.join(output_dir, filename_clean + ".md")):
            suffix += 1
            filename_clean = f"{base_name} ({suffix})"

    new_filename = filename_clean + ".md"
    
    return new_filename
        
def trim(text, max_length=80):
    """
    Formats text for use in a file name:
    - Takes the first 2-3 sentences.
    - Limits the length to max_length characters.
    - Replaces invalid symbols/
    - Removes invalid characters except dot, hyphen, and space.
    - Adds a suffix if a file with that name already exists.
    """

    # Split post on sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)
    first_sentences = " ".join(sentences[:3])  # Take first 3 sentences
    
    # Limit the length
    if len(first_sentences) > max_length:
        first_sentences = first_sentences[:max_length].rsplit(' ', 1)[0] + "..."

    return first_sentences    
        
def fix_invalid_filename(text):
    # Replace symbols invalid in Windows
    replace_map = {ord(k): v for k, v in config["replace_map"].items()}
    allowed_chars = set(config["allowed_chars"])
    text = text.translate(replace_map)

    valid_filename = ''.join(c for c in text if c.isalnum() or c in allowed_chars)

    return valid_filename.strip()
    

def load_config(config_path):
    if not os.path.exists(config_path):
        print(f"Файл не найден: {config_path}")
        print(f"Текущая директория: {os.getcwd()}")
    else:
        print(f"Файл найден: {config_path}")
    with open(config_path, "r", encoding="utf-8") as file:
        return json.load(file)