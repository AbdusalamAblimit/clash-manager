#!/bin/bash

# 列出所有名为"clash-screen"的screen窗口，并将其PID存储到变量中
SCREEN_IDS=$(screen -ls | grep "clash-screen" | awk '{print $1}')

# 如果存在名为"clash-screen"的screen窗口，则询问用户是否要关闭这些窗口
if [[ ! -z "$SCREEN_IDS" ]]; then
    MESSAGE="Do you want to close the following screen windows:\n\n$SCREEN_IDS"
    zenity --question --text="$MESSAGE"
    if [[ $? -eq 0 ]]; then
        for ID in $SCREEN_IDS; do
            screen -S "${ID}" -X quit
        done
    fi
else
    MESSAGE="No screen windows found"
    zenity --info --text="$MESSAGE"
fi

