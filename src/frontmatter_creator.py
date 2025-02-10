import src.post_parser as post_parser

import logging
from datetime import datetime

def create(post, user_id):

    '''
    returns default post header
    '''

    post_id = post['id']
    post_date = datetime.fromisoformat(post['date'])
    post_tags = post_parser.parse_tags(post['text_entities'])

    # TODO: support for custom header
    post_header = f'---\nid: {post_id}\ndate: {post_date}\n'

    if post_tags:
        post_header += f'tags: {post_tags}\n'

    if 'forwarded_from' in post:
        post_header += "forwarded\\_from: \"'{}\"'\n".format(post['forwarded_from'])

    if 'saved_from' in post:
        post_header += "saved\\_from: \"'{}\"'\n".format(post['saved_from'])

    post_header += '---'

    return post_header