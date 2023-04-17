#!/bin/bash

# 定义screen窗口名称和命令
WINDOW_NAME="clash-screen"
COMMAND="clash"

# 列出所有名为"clash-screen"的screen窗口，并将其PID存储到变量中
SCREEN_IDS=$(screen -ls | grep "clash-screen" | awk '{print $1}')

if [[ -z "$SCREEN_IDS" ]]; then
    # 如果不存在，则显示通知消息
    MESSAGE="没有正在运行的Clash窗口."
    zenity --notification --text="$MESSAGE"
else
    # 如果已存在，则在新的终端窗口中运行screen -r命令以重新连接到已存在的screen会话
    gnome-terminal -- bash -c "screen -r $WINDOW_NAME; exec bash"
fi
