import os
import threading
import tkinter as tk
import time

class ClashControlApp:
	def __init__(self):
		self.window = tk.Tk()
		self.window.title("Clash 控制器")
		self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
		# 添加带滚动条的文本框来显示日志文件内容
		self.log_frame = tk.Frame(self.window)
		self.log_frame.pack(fill=tk.BOTH, expand=True)
		self.log_text = tk.Text(self.log_frame)
		self.scrollbar = tk.Scrollbar(self.log_frame, command=self.log_text.yview)
		self.log_text.configure(yscrollcommand=self.scrollbar.set)
		self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
		self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

		# 添加"启动 Clash"按钮
		run_btn = tk.Button(self.window, text="启动 Clash", command=self.run_clash)
		run_btn.pack(padx=20, pady=10)

		# 添加"退出 Clash"按钮
		exit_btn = tk.Button(self.window, text="退出 Clash", command=self.exit_clash)
		exit_btn.pack(padx=20, pady=10)

		# 添加"打开 Clash 窗口"按钮
		open_btn = tk.Button(self.window, text="打开 Clash 窗口", command=self.open_clash_window)
		open_btn.pack(padx=20, pady=10)

		# 在单独的线程中更新日志
		self.log_thread = threading.Thread(target=self.update_log)
		self.log_thread.daemon = True  # 将日志线程设置为守护线程
		self.log_thread.start()
		self.window.mainloop()

	def run_clash(self):
		os.system('./open-clash.sh')

	def exit_clash(self):
		os.system('./close-clash.sh')

	def open_clash_window(self):
		os.system('./open-clash-window.sh')

	def update_log(self):
		log_content = ""
		newest_log_file = None
		while True:
		# 如果没有目录，则创建目录
			if not os.path.exists('/tmp/clash_log'):
				os.makedirs('/tmp/clash_log')

			# 获取/tmp/clash目录下的所有日志文件
			log_files = os.listdir('/tmp/clash_log')

			if not log_files:
				self.log_text.delete('1.0', tk.END)
				self.log_text.insert(tk.END, "暂无日志文件")
			else:
				# 找到最新的日志文件
				current_newest_log_file = None
				for filename in log_files:
					if filename.endswith('.log') and (current_newest_log_file is None or filename > current_newest_log_file):
						current_newest_log_file = filename

				# 如果找到一个新的日志文件，则清除所有内容并重新开始输出
				if current_newest_log_file != newest_log_file:
					self.log_text.delete('1.0', tk.END)
					newest_log_file = current_newest_log_file
					log_content = ""

				# 如果找到最新的日志文件，则读取它的内容并更新文本框
				if newest_log_file is not None:
					with open(f'/tmp/clash_log/{newest_log_file}', 'r') as f:
						new_log_content = f.read()
						if log_content != new_log_content:
							new_content = new_log_content[len(log_content):]
							self.log_text.insert(tk.END, new_content)
							log_content = new_log_content

							# 限制字符数，超过50000个字符时，截取后50000个字符
							if len(log_content) > 50000:
								log_content = log_content[-50000:]
								self.log_text.delete('1.0', tk.END)
								self.log_text.insert(tk.END, log_content)

							# 如果滚动条在最下方，新内容来了就让滚动条再次定位到最下方
							if self.log_text.yview()[1] >= 0.95:
								self.log_text.yview_moveto(1.0)

			# 暂停一段时间再检查新的日志文件
			time.sleep(1)

	def on_closing(self):
    		self.window.destroy()  # 关闭主窗口

if __name__ == '__main__':
    app = ClashControlApp()

