#!/usr/bin/python

import re
import os
import subprocess
import random
import configparser
import argparse
import argcomplete


DEFAULT_CONFIG_PATH = os.path.expanduser('~/.config/termite/config')
DEFAULT_THEMES_DIR = os.path.expanduser('~/.config/termite/base16-termite/themes')
CONFIG_PATH = os.path.expanduser('~/.config/termite-themes')


def get_termite_themes_config():
    try:
        config = configparser.ConfigParser()
        config.read(CONFIG_PATH)
        return {**config['default']}
    except Exception:
        print(f'WARNING: Could not read config at {CONFIG_PATH}. It is either missing or invalid')
        return {
            'config_path': DEFAULT_CONFIG_PATH,
            'themes_dir': DEFAULT_THEMES_DIR,
        }


def read_themes_list(themes_dir):
    try:
        return [
            x.replace('.config', '')
            for x in os.listdir(themes_dir) if '.config' in x
        ]
    except Exception:
        raise Exception(f'Themes directory "{themes_dir}" does not exist!')


def themes_completer(prefix, parsed_args, **kwargs):
    themes = read_themes_list(parsed_args.themes_dir)
    if not prefix:
        return themes
    return [x for x in themes if prefix in x]


def handle_exception(func):
    def wrapped(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            print('Error:', e.args[0])
    return wrapped


def parse_config(config_path: str) -> ([str], [str]):
    """Returns two sections: config before [colors] config and config after [colors]
    """
    with open(config_path) as config_file:
        config_lines = config_file.readlines()
    before_lines = []
    after_lines = []

    BEFORE = 0  # Before colors section
    DURING = 1  # In colors section
    AFTER = 2  # After colors section

    state = BEFORE
    for line in config_lines:
        if line.strip() == '[colors]':
            state = DURING
        elif re.match(r'^\s*\[.+\]\s*', line):
            state = state if state != DURING else AFTER

        if state == BEFORE:
            before_lines.append(line)
        elif state == AFTER:
            after_lines.append(line)
    return before_lines, after_lines


def switch_theme(args, theme):
    themes = read_themes_list(args.themes_dir)
    if theme not in themes:
        raise Exception(f'Theme "{theme}" does not exist in themes dir "{args.themes_dir}"')
    before_colors, after_colors = parse_config(args.config_path)
    theme_lines = open(os.path.join(args.themes_dir, f'{theme}.config')).readlines()

    print('Changing config file..', end='')
    with open(args.config_path, 'w') as config_file:
        config_file.writelines(before_colors)
        config_file.writelines(theme_lines)
        config_file.writelines(after_colors)
    print('DONE')

    print('Refreshing termite instances..', end='')
    subprocess.call(['killall', '-USR1', 'termite'])
    print('DONE')


def init():
    DEFAULT_TERMITE_THEMES_CONFIG = get_termite_themes_config()
    parser = argparse.ArgumentParser(description='Parser for termite-theme-switcher')

    parser.add_argument('--config-path', type=str,
                        default=DEFAULT_TERMITE_THEMES_CONFIG['config_path'],
                        help='Termite config directory')

    parser.add_argument('--themes-dir', type=str,
                        default=DEFAULT_TERMITE_THEMES_CONFIG['themes_dir'],
                        help='Termite themes directory')

    parser.add_argument('--list', action='store_true',
                        help='List available themes')

    parser.add_argument('--random', action='store_true',
                        help='Switch to random theme present in themes directory')

    switch_to_parser = parser.add_argument('--switch-to', type=str, nargs=1,
                        help='The theme name to switch to')

    switch_to_parser.completer = themes_completer
    argcomplete.autocomplete(parser)
    return parser


@handle_exception
def main():
    parser = init()
    args = parser.parse_args()

    if args.list:
        title = 'Available themes:'
        themes = read_themes_list(args.themes_dir)
        print(f'{title}\n{"=" * len(title)}')
        print('\n'.join(themes))
    elif args.random:
        themes = read_themes_list(args.themes_dir)
        random_theme = random.choice(themes)
        print('Applying random theme:', random_theme)
        switch_theme(args, random_theme)
    elif args.switch_to:
        theme = args.switch_to[0]
        switch_theme(args, theme)
    else:
        print('Nothing to do!!\nJust take a deep breath and everything will be at it\'s place..')


if __name__ == '__main__':
    main()
