import src.text_parser as text_parser

import os
import logging
import shutil
from pathlib import Path

def parse_tags(text_entities):

    tags = []
    for obj in text_entities:
        if obj['type'] == 'hashtag':
            tags.append('\n  - ' + obj['text'].lstrip('#'))

    return ' '.join(tags)


def parse_post_photo(post, photo_dir, out_dir):

    '''
    converts photo tag to markdown image link
    '''
    photo_dir = os.path.join(photo_dir, post['photo'])
    post_photo = '![image]({src})\n\n'.format(src=post['photo'])
    destination_path = os.path.join(out_dir, 'photos')
    Path(destination_path).mkdir(parents=True, exist_ok=True)
    shutil.copy(photo_dir, destination_path)

    return post_photo

# TODO: do not parse the sequence 'hashtag' 'plain' 'hashtag' 'plain' $
def parse_post_text(post):
    # TODO: handle reply-to
    post_id = post['id']
    post_raw_text = post['text_entities']
    post_parsed_text = ''

    if isinstance(post_raw_text, str):
        return str(post_raw_text)

    for obj in post_raw_text:
        if isinstance(post_raw_text, str):
            post_parsed_text += obj
        elif (text := text_parser.parse_text_object(post_id, obj)) is not None:
            post_parsed_text += str(text)

    return post_parsed_text

def parse_post_media(post, media_dir):

    '''
    wraps file links to Obsidian link
    '''

    post_media = '![[{src}]]\n\n'.format(src=post['file'])

    return post_media


def parse_post(post, photo_dir, media_dir, out_dir):

    '''
    converts post object to formatted text
    '''

    post_output = ''

    if 'media_type' in post and post['media_type'] == 'sticker':
        return "Stickers output is not supported"
        
    # optional image
    if 'photo' in post:
        post_output += str(parse_post_photo(post, photo_dir, out_dir))

    # optional media
    if 'media_type' in post:
        post_output += str(parse_post_media(post, media_dir))

    # post text
    post_output += str(parse_post_text(post))

    return post_output.strip()