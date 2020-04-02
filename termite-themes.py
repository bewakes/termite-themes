#!/usr/bin/python

import re
import os
import subprocess
import argparse

parser = argparse.ArgumentParser(description='Parser for termite-theme-switcher')

parser.add_argument('--config-path', type=str,
                    default=os.path.expanduser('~/.config/termite/config'),
                    help='Termite config directory')

parser.add_argument('--themes-dir', type=str,
                    default=os.path.expanduser('~/.config/termite/base16-termite/themes'),
                    help='Termite themes directory')

parser.add_argument('--list', action='store_true',
                    help='List available themes')

parser.add_argument('--switch-to', type=str, nargs=1,
                    help='The theme name to switch to')

# https://github.com/khamer/base16-termite

def handle_exception(func):
    def wrapped(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            print('Error:', e.args[0])
    return wrapped


def read_themes_list(themes_dir):
    try:
        return [
            x.replace('.config', '')
            for x in os.listdir(themes_dir) if '.config' in x
        ]
    except Exception:
        raise Exception(f'Themes directory "{themes_dir}" does not exist!')


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
        elif re.match('^\s*\[.+\]\s*', line):
            state = state if state != DURING else AFTER

        if state == BEFORE:
            before_lines.append(line)
        elif state == AFTER:
            after_lines.append(line)
    return before_lines, after_lines



def switch_theme(args):
    themes = read_themes_list(args.themes_dir)
    theme = args.switch_to[0]
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


@handle_exception
def main():
    args = parser.parse_args()

    if args.list:
        title = 'Available themes:'
        themes = read_themes_list(args.themes_dir)
        print(f'{title}\n{"=" * len(title)}')
        print('\n'.join(themes))
    elif args.switch_to:
        switch_theme(args)
    else:
        print('Nothing to do')


if __name__ == '__main__':
    main()
