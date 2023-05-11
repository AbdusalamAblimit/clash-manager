# Clash控制器

## 背景

​		因为在ubuntu打开bash运行Clash的话, 窗口不能关掉, 很烦.

​		基于screen多重视窗管理程序, 可以实现clash的后台隐藏运行.

​		但是, 每次敲好几个命令隐藏它, 想关闭时又得敲命令调出来. 所以基于shell命令和python写了窗体程序方便地在后台运行Clash，又可以方便地把clash窗口调出来。

​		**自用的小程序，很粗糙劣质。网上当然有更好的，但是这个更符合我自己的使用习惯。**

## 结构

- clash-manager.py

​		主程序，用`python3`运行程序就会出现管理窗口。每一个按钮对应一个`.sh`脚本。包含一个日志窗口，动态更新显示clash日志。

- open-clash.sh

​		实现启动Clash的功能的脚本。

- close-clash.sh

​		实现关闭Clash的功能的脚本。

- open-clash-window.sh

​		能够调出后台正在运行的Clash窗口的脚本。

- clash-icon.png

​		clash图标，用于生成程序在桌面的快捷入口。

## 部署

​		首先确保`/etc/clash/`目录存在，同时该目录下存在clash程序或者clash的链接，文件名或链接名为clash。

1. 输入`sudo apt install screen`来安装screen。
2. 输入`git clone https://github.com/AbdusalamAblimit/clash-manager.git`下载项目。
3. 输入`rm -rf ./clash-manager/.git/`删除git仓库相关的文件。
4. 输入`sudo mv ./clash-manager/ /etc/clash/`将程序移动到目标目录。
5. 在桌面创建一个名为`ClashManager.desktop`的文件，并通过文本编辑器打开，输入以下内容：

```bash
[Desktop Entry]
Name=ClashManager
Exec=bash -c 'cd /etc/clash/clash-manager/ && /bin/python3 ./clash-manager.py'
Icon=/etc/clash/clash-manager/clash-icon.png
Terminal=false
Type=Application
Categories=Utility;
```

4. 鼠标右键点击桌面`ClashManager`，点击`属性`，点击`权限`，点击`允许执行文件`
5. 鼠标右键点击桌面`ClashManager`，点击`允许运行`

​		按照上述步骤操作后，应该可以看到一个简单的窗体程序，点击各个按钮使用即可。可以随时关闭窗口，关闭后clash不会停止运行。

<img src="https://abdusalam-typora.oss-cn-beijing.aliyuncs.com/img-for-typora/image-20230417211856589.png" alt="image-20230417211856589" style="zoom: 67%;" />

## 可能遇到的问题

​		以后在新环境使用过程中遇到什么问题会及时在这里更新，下面是一个已知的可行思路。

### 点击桌面图标没有反应

​		这种情况下，可以打开终端输入`python3 /etc/clash/clash-manager/clash-manager.py`查看python程序有没有报错。根据报错信息进行相应处理。
