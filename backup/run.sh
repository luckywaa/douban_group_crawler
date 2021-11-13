#!/bin/bash

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/mnt/data1/datadir/homedir/KB/kb/appdir/anaconda3_common/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/mnt/data1/datadir/homedir/KB/kb/appdir/anaconda3_common/etc/profile.d/conda.sh" ]; then
        . "/mnt/data1/datadir/homedir/KB/kb/appdir/anaconda3_common/etc/profile.d/conda.sh"
    else
        export PATH="/mnt/data1/datadir/homedir/KB/kb/appdir/anaconda3_common/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<

conda activate douban_crawler
python crawler.py
