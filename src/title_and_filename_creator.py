import os
import logging
import re
from datetime import datetime

def get_filename_based_on_date_and_id(post_date, id):
    return str(post_date) + '-' + str(id) + '.md'

def get_default(post_date, id):
    return get_filename_based_on_date_and_id(post_date, id)


def rename_file_based_on_content(file_path, parsed_text, keep_duplicates, output_dir="."):

    first_line = parsed_text.strip()
    
    # remove extensions if it contains files
    first_line = first_line.replace('.ogg', '').replace('.mp4', '').replace('.jpg', '').replace('.mp4', '')
    
    # Format the file name
    filename_clean = get_filename_based_on_content(first_line)
    filename_clean = fix_invalid_filename(filename_clean)
    new_filename = filename_clean + ".md"
    
    # Create new path
    dir_path = os.path.dirname(file_path)
    new_file_path = os.path.join(dir_path, new_filename)
    
    if keep_duplicates:
        # If the new name matches the existing one, skip it
        base_name = filename_clean
        suffix = 1
        while os.path.exists(os.path.join(output_dir, filename_clean + ".md")):
            suffix += 1
            filename_clean = f"{base_name} ({suffix})"

    new_filename = filename_clean + ".md"
    dir_path = os.path.dirname(file_path)
    new_file_path = os.path.join(dir_path, new_filename)
    
    try:
        if not keep_duplicates:
            if os.path.exists(new_file_path):
                os.remove(new_file_path)
        os.rename(file_path, new_file_path)
        #print(f"File was renamed: {file_path} -> {new_file_path}")
    except Exception as e:
        print(f"Error renaming {file_path}: {e}")
        
def get_filename_based_on_content(text, max_length=80):
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
    text = text.replace('>', '-')
    text = text.replace('<', '-')
    text = text.replace('[', '-')
    text = text.replace(']', '-')
    text = text.replace('(', '-')
    text = text.replace(')', '-')
    text = text.replace('\\', '-')
    text = text.replace('/', '-')
    text = text.replace(':', '.')
    text = text.replace('—', ' - ')

    valid_filename = ''.join(c for c in text if c.isalnum() or c in ('_', '-', '.',', ', ' '))

    return valid_filename.strip()
    