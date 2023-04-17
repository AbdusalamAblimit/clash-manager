#!/bin/bash

# 定义screen窗口名称和日志文件路径
WINDOW_NAME="clash-screen"
LOG_DIR="/tmp/clash_log"
LOG_FILE="${LOG_DIR}/$(date '+%Y%m%d-%H%M%S').log"

# 如果日志目录不存在，则创建目录
mkdir -p "$LOG_DIR"

# 检查是否已存在具有相同名称的screen窗口
SCREEN_IDS=$(screen -ls | grep "${WINDOW_NAME}" | awk '{print $1}')
if [[ ! -z "$SCREEN_IDS" ]]; then
    MESSAGE="已经存在具有相同名称的窗口，将不创建新窗口。"
    zenity --warning --text="$MESSAGE"
    exit 1
else
    # 启动一个名为"clash-screen"的screen窗口，并将输出重定向到日志文件
    screen -dmS "$WINDOW_NAME" bash -c "/etc/clash/clash 2>&1 | tee $LOG_FILE"
    sleep 0.5
    # 等待日志文件中出现"Listening at"字符串，表示clash启动成功
    while true; do
        if grep -q "listening at" "$LOG_FILE"; then
            MESSAGE="成功启动clash."
            zenity --notification  --text="$MESSAGE"
            break
        elif grep -q "error" "$LOG_FILE"; then
            MESSAGE="启动clash失败."
            zenity --notification  --text="$MESSAGE"
            # 删除刚刚创建的窗口
            screen -S "$WINDOW_NAME" -X quit
            break
        else
            sleep 1
        fi
    done
fi
