#!/usr/bin/env python
# -*- coding: utf-8 -*-

# tg2md.py - converts Telegram JSON to Obsidian Markdown.
# Copyright (c) 2020, Lev Brekalov
# Changes from progxaker, 2021-2024

# TODO summary:
# - replies
# - custom post header

import src.args_parser as args_parser
import src.post_parser as post_parser
import src.frontmatter_creator as frontmatter_creator
import src.metadata_creator as metadata_creator
import src.title_and_filename_creator as title_and_filename_creator

import os
import sys
import json
import logging
from datetime import datetime

log = logging.getLogger(__name__)

base_dir = ""

def set_base_dir():
    global base_dir
    base_dir = os.path.dirname(os.path.abspath(__file__))

def get_config_path(name):
    return os.path.join(base_dir, "configs", name + ".json")

def load_json(args):
    try:
        json_path = os.path.join(args.path, 'result.json')
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        sys.exit('result.json not found.\nPlease, specify right path')  

def parse_raw_posts(raw_posts, args, user_id):
    photo_dir = args.path

    for post in raw_posts:
        if post['type'] == 'message':
            parse_message(post, args, user_id, photo_dir)

        elif post['type'] == 'service' and post['action'] == 'clear_history':
            log.debug("The type of post #%i is 'service' and the action is 'clear_history'.", \
                      post['id'])
            continue
        else:
            log.warning("The type of post #%i is '%s' and it is not supported.", \
                         post['id'], post['type'])


def parse_message(post, args, user_id, photo_dir):
    parsed_text = post_parser.parse_post(post, photo_dir, args.media_dir, args.out_dir)
    post_date = datetime.fromisoformat(post['date'])
    post_filename = title_and_filename_creator.get_filename_based_on_content(parsed_text, False, args.out_dir)
    post_path = os.path.join(args.out_dir, post_filename)

    
    # https://github.com/telegramdesktop/tdesktop/blob/7e071c770f7691ffdbbbd38ac3e17c9aae4d21b3/Telegram/SourceFiles/export/data/export_data_types.cpp#L244
    # const auto text = QString::fromUtf8(data.v);
    with open(post_path, 'w', encoding='utf-8') as f:
        print(frontmatter_creator.create(post, user_id), file=f)
        print(parsed_text, file=f)

    # TODO: correct names for media-only posts
    

def main():
    set_base_dir()
    
    args = args_parser.create().parse_args()

    logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s - %(message)s', \
                        level=args.log_level.upper())

    metadata_creator.check(args.out_dir)
    title_and_filename_creator.initialize(get_config_path("title_replace_symbols"))
    
    try:
        os.mkdir(args.out_dir)
    except FileExistsError:
        pass

    data = load_json(args)

    user_id = data['id']
    raw_posts = data['messages']

    parse_raw_posts(raw_posts, args, user_id)
    metadata_creator.write_metadata(args.out_dir)


if __name__ == '__main__':
    main()
