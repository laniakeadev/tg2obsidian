import argparse
import logging

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
            '--name-style', metavar='name_style',
            nargs='?', default='first_sentences',
            help='***')
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
    
    return parser