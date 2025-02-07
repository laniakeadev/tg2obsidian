#!/usr/bin/env python
# -*- coding: utf-8 -*-

# tg2md.py - converts Telegram JSON to Obsidian Markdown.
# Copyright (c) 2020, Lev Brekalov
# Changes from progxaker, 2021-2024

# TODO summary:
# - replies
# - custom post header

import parser_creator
import text_parser

import os
import sys
import json
import logging
import shutil
from pathlib import Path
from datetime import datetime

log = logging.getLogger(__name__)

def parse_tags(text_entities):

    tags = []
    for obj in text_entities:
        if obj['type'] == 'hashtag':
            tags.append(obj['text'])

    return ' '.join(tags)

def print_default_post_header(post, user_id):

    '''
    returns default post header
    '''

    post_title = post['id']
    post_date = datetime.fromisoformat(post['date'])
    post_tags = parse_tags(post['text_entities'])

    # TODO: support for custom header
    post_header = f'---\ntitle: {post_title}\ndate: {post_date}\n'

    if post_tags:
        post_header += f'tags: {post_tags}\n'

    if 'from_id' in post:
        if post['from_id'] != f'user{user_id}':
            from_header = "from: \"'{name}' ({user_id})\"\n"
            post_header += from_header.format(name=post['from'], user_id=post['from_id'])

    if 'forwarded_from' in post:
        post_header += "forwarded\\_from: \"'{}\"'\n".format(post['forwarded_from'])

    if 'saved_from' in post:
        post_header += "saved\\_from: \"'{}\"'\n".format(post['saved_from'])

    post_header += 'layout: post\n'\
                   '---'

    return post_header


def print_custom_post_header(post_header_file, *args):

    '''
    now unusable (i dunno how it may work)
    '''

    with post_header_file as f:
        post_header_content = read(post_header_file)
    for arg in args:
        pass
    return post_header_content


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
def parse_post_text(post, stickers_dir):
    # TODO: handle reply-to
    post_id = post['id']
    post_raw_text = post['text_entities']
    post_parsed_text = ''

    if isinstance(post_raw_text, str):
        return str(post_raw_text)

    for obj in post_raw_text:
        if isinstance(post_raw_text, str):
            post_parsed_text += obj
        elif (text := text_parser.parse_text_object(post_id, obj, stickers_dir)) is not None:
            post_parsed_text += str(text)

    return post_parsed_text

def parse_post_media(post, media_dir):

    '''
    wraps file links to Obsidian link
    '''

    post_media = '![[{src}]]\n\n'.format(src=post['file'])

    return post_media


def parse_post(post, photo_dir, media_dir, stickers_dir, out_dir):

    '''
    converts post object to formatted text
    '''

    post_output = ''

    # optional image
    if 'photo' in post:
        post_output += str(parse_post_photo(post, photo_dir, out_dir))

    # optional media
    if 'media_type' in post:
        post_output += str(parse_post_media(post, media_dir))

    # post text
    post_output += str(parse_post_text(post, stickers_dir))

    return post_output


def main():

    args = parser_creator.create().parse_args()

    logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s - %(message)s', \
                        level=args.log_level.upper())

    try:
        os.mkdir(args.out_dir)
    except FileExistsError:
        pass

    # load json file
    try:
        json_path = os.path.join(args.path, 'result.json')
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        sys.exit('result.json not found.\nPlease, specify right file')

    # load messages and user_id
    user_id = data['id']
    raw_posts = data['messages']

    photo_dir = args.path

    for post in raw_posts:
        if post['type'] == 'message':

            post_date = datetime.fromisoformat(post['date'])
            post_filename = str(post_date.date()) + '-' + str(post['id']) + '.md'
            post_path = os.path.join(args.out_dir, post_filename)

            # https://github.com/telegramdesktop/tdesktop/blob/7e071c770f7691ffdbbbd38ac3e17c9aae4d21b3/Telegram/SourceFiles/export/data/export_data_types.cpp#L244
            # const auto text = QString::fromUtf8(data.v);
            with open(post_path, 'w', encoding='utf-8') as f:
                print(print_default_post_header(post, user_id), file=f)
                print(parse_post(post, photo_dir, args.media_dir, args.stickers_dir, args.out_dir), file=f)

        elif post['type'] == 'service' and post['action'] == 'clear_history':
            log.debug("The type of post #%i is 'service' and the action is 'clear_history'.", \
                      post['id'])
            continue
        else:
            log.warning("The type of post #%i is '%s' and it is not supported.", \
                         post['id'], post['type'])

if __name__ == '__main__':
    main()
