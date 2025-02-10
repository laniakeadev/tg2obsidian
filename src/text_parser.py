import os
import sys
import argparse
import json
import logging
import re
from datetime import datetime

log = logging.getLogger(__name__)

def text_format(string, fmt):

    '''
    wraps string in markdown-styled formatting
    '''

    if fmt in ('*', '**', '***', '`', '```'):
        output = '{fmt}{txt}{fmt}'
    elif fmt == '```':
        output = '{fmt}\n{txt}\n{fmt}'
    else:
        output = '<{fmt}>{txt}</{fmt}>'

    output = output.format(fmt=fmt, txt=string.strip())
    output += '\n' * string.split('\n').count('') * string.endswith('\n')
    return output

# Deserialization based on tdesktop source code
# https://github.com/telegramdesktop/tdesktop/blob/7e071c770f7691ffdbbbd38ac3e17c9aae4d21b3/Telegram/SourceFiles/export/output/export_output_json.cpp#L26-L70
#
# TODO: Implement the last two 'if else' statements.
def deserialize_string(text):

    text.replace(r'\n', '\n')
    text.replace(r'\r', '\r')
    text.replace(r'\t', '\t')
    text.replace(r'\"', '"')
    text.replace(r'\\', '\\')

    return text


# TODO: Put the inline image to the end of the Markdown file.
def text_link_format(text, link):

    '''
    formats links
    '''

    # FIXME: Process text such as [.\n](link)
    if text in ('\u200b', '\u200b\u200b', '\xa0'):
        log.debug('The text is zero-width space, process as an inline image.')
        link_fmt = f'> ![]({link})\n\n'
    else:
        # convert telegram links to anchors
        # this implies that telegram links are pointing to the same channel
        if link.startswith('https://t.me/c/'):
            link = '#' + link.split('/')[-1]
        link_fmt = '[{text}]({href})'
        link_fmt = link_fmt.format(text=text, href=link)
        link_fmt += '\n' * text.count('\n') * text.endswith('\n')

    return link_fmt

def parse_text_object(post_id, obj):

    # https://github.com/telegramdesktop/tdesktop/blob/7e071c770f7691ffdbbbd38ac3e17c9aae4d21b3/Telegram/SourceFiles/export/output/export_output_json.cpp#L164-L189
    '''
    unknown, mention, hashtag, bot_command, link, email
    bold, italic, code, pre, plain, text_link, mention_name
    phone, cashtag, underline, strikethrough, blockquote
    bank_card, spoiler, custom_emoji
    '''

    '''
    detects type of text object and wraps it in corresponding formatting
    '''

    obj_type = obj['type']
    obj_text = deserialize_string(obj['text'])

    log.debug("Process the '%s' object of the post #%i with the content %r.", \
               obj_type, post_id, obj)

    if obj_type == 'text_link':
        return text_link_format(obj_text, obj['href'])

    elif obj_type in ('link', 'email'):
        link = obj_text.strip()
        link = 'https://' * (obj_type == 'link') * \
            (1 - link.startswith('https://')) + link
        return f'<{link}>'

    elif obj_type == 'phone':
        return obj_text

    elif obj_type == 'italic':
        return text_format(obj_text, '*')

    elif obj_type == 'bold':
        return text_format(obj_text, '**')

    elif obj_type == 'code':
        return text_format(obj_text, '`')

    elif obj_type == 'pre':
        return text_format(obj_text, '```')

    elif obj_type == 'underline':
        return text_format(obj_text, 'u')

    elif obj_type == 'strikethrough':
        return text_format(obj_text, 's')

    elif obj_type == 'plain':
        return obj_text

    elif obj_type == 'bank_card':
        return obj_text

    elif obj_type == 'mention':
        return 'https://t.me/{}'.format(obj_text[1:])

    elif obj_type == 'blockquote':
        return f'> {obj_text}'

    elif obj_type == 'custom_emoji':
        document_id = obj['document_id']
        document_id = re.sub(r'( |\\|/|\(|\))', r'\\\g<1>', obj['document_id'])
        return f'![{obj_text}]({document_id})\n\n'

    elif obj_type == 'spoiler':
        return f'> [!info]\n> {obj_text}\n\n'

    elif obj_type == 'hashtag':
        return None

    else:
        log.warning("Cannot format the '%s' object type of the post #%i.", obj_type, post_id)
        return None