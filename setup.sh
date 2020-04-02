#!/bin/bash

echo Setting up termite.
echo ===================

DEFAULT_CONFIG_PATH=~/.config/termite/config
DEFAULT_CONFIG_DIR=`dirname $DEFAULT_CONFIG_PATH`

read -p "Termite config path[Default: $DEFAULT_CONFIG_PATH] ?" TMP_DEFAULT

if [[ ! -z $TMP_DEFAULT ]]; then
    DEFAULT_CONFIG_PATH=$TMP_DEFAULT
fi

echo Looking for themes in config path
themes_dir=`ls $DEFAULT_CONFIG_DIR | grep -E 'base16-termite'`
echo $themes_dir
if [[ -z $themes_dir ]]; then
    read -p "Seems like there are no themes currently. Want to download from https://github.com/khamer/base16-termite(Y/n)?" yesorno
    if [[ -z $yesorno ]]; then
        yesorno=y
    fi
    if [[ $yesorno == 'y' || $yesorno == 'Y' ]]; then
        dir=`dirname $DEFAULT_CONFIG_PATH`
        echo Cloning base16-termite to $dir
        git clone https://github.com/khamer/base16-termite $dir/base16-termite
        echo setting default themes_dir $dir/base16-termite/themes
        DEFAULT_THEMES_DIR=$dir/base16-termite/themes
    fi
else
    DEFAULT_THEMES_DIR=$DEFAULT_CONFIG_DIR/base16-termite/themes
    echo "Dir exists for themes";
fi

config_path=~/.config/termite-themes
echo Writing config to "$config_path"
echo [default] >> $config_path
echo config_path = $DEFAULT_CONFIG_PATH >> $config_path
echo themes_dir = $DEFAULT_THEMES_DIR >> $config_path

# TODO: install on path
echo Done!!