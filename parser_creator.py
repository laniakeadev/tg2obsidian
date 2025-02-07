import argparse
import logging
from datetime import datetime

log = logging.getLogger(__name__)

def create():
    parser = argparse.ArgumentParser(
            usage='%(prog)s [options] json_file',
            description='Convert exported Telegram channel data json to \
                    bunch of markdown posts ready to use with Obsidian')
    parser.add_argument(
            'path', metavar='path',
            help='folder that contains result.json file from telegram export')
    parser.add_argument(
            '--out-dir', metavar='out_dir',
            nargs='?', default='formatted_posts',
            help='output directory for markdown files\
                    (default: formatted_posts)')
    parser.add_argument(
            '--log-level', metavar='log_level',
            nargs='?', default='warn',
            help='Set the logging level (e.g., debug, info, warning,\
                    error, critical)')
    args_wip = parser.add_argument_group('work in progress')
    args_wip.add_argument(
            '--post-header', metavar='post_header',
            nargs='?',
            help='yaml front matter for your posts \
                    (now doesn\'t work)')
    args_wip.add_argument(
            '--photo-dir', metavar='photo_dir',
            nargs='?', default='photos',
            help='location of image files. this changes only links\
                    to photos in markdown text, so specify your\
                    desired location (default: photos)')
    args_wip.add_argument(
            '--media-dir', metavar='media_dir',
            nargs='?', default='files',
            help='location of media files. this changes only links\
                    to files in markdown text, so specify your \
                    desired location (default: files)')
    args_wip.add_argument(
            '--stickers-dir', metavar='stickers_dir',
            nargs='?', default='stickers',
            help='location of sticker files. this changes only links\
                    to stickers in markdown text, so specify your \
                    desired location (default: stickers)')
    
    return parser