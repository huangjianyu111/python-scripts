import os
import tkinter as tk
from tkinter import messagebox
import magic  # 第三方库，用于判断文件类型

searching = False  # 标志位，表示当前是否在搜索中

def is_text_file(file_path):
    """
    判断文件是否为文本文件
    """
    mime = magic.Magic(mime=True)
    file_mime_type = mime.from_file(file_path)
    return file_mime_type.startswith('text') or file_path.endswith('.pdf')

def search_files(directory, keyword, filename):
    """
    在目录中搜索包含关键字的文件
    """
    global searching  # 使用全局变量
    found_files = []
    for root, dirs, files in os.walk(directory):
        if not searching:  # 如果点击取消按钮，停止搜索
            break
        for file in files:
            if not searching:  # 如果点击取消按钮，停止搜索
                break
            file_path = os.path.join(root, file)

            if os.path.isfile(file_path):
                if is_text_file(file_path):  # 判断文件是否为文本文件
                    try:
                        with open(file_path, 'r') as f:
                            content = f.read()
                        isKeywordOk = keyword and keyword in content
                        isFilenameOk = filename in file
                        if keyword and filename and (isKeywordOk and isFilenameOk):
                            found_files.append(file_path)
                        elif keyword and isKeywordOk:
                            found_files.append(file_path)
                        elif filename and isFilenameOk:
                            found_files.append(file_path)
                    except Exception as e:
                        result_text.tag_configure("red", foreground="red")  # 配置标签，将文字设置为红色
                        result_text.insert(tk.END, f"{file_path} (读取错误)\n", "red")  # 以红色字体输出文件路径
                        result_text.insert(tk.END, f"错误信息：{str(e)}\n\n", "red")  # 输出错误信息
            else:
                continue
    return found_files


def search_button_clicked():
    """
    当点击搜索按钮时执行搜索操作
    """
    global searching  # 使用全局变量
    if not searching:
        searching = True  # 标记为正在搜索
        directory = directory_entry.get()
        keyword = keyword_entry.get()
        filename = filename_entry.get()

        if not directory:  # 如果目录输入框为空，则遍历所有目录
            directory = 'D:\\'  # 默认从 D 盘根目录开始搜索

        if keyword or filename:
            result_text.insert(tk.END, f"开始在目录 {directory} 中搜索...\n")  # 输出开始搜索消息
            found_files = search_files(directory, keyword, filename)
            if found_files:
                result_text.delete(1.0, tk.END)  # 清空之前的搜索结果
                for file in found_files:
                    result_text.insert(tk.END, file + '\n')
            else:
                messagebox.showinfo("搜索结果", "未找到匹配的文件。")
        else:
            messagebox.showinfo("提示", "关键字和文件名不能同时为空！")
        searching = False  # 搜索结束后重置标志位

def cancel_button_clicked():
    """
    当点击取消按钮时执行取消操作
    """
    global searching  # 使用全局变量
    if searching:  # 如果正在搜索，询问用户是否确认停止搜索
        if messagebox.askyesno("停止搜索", "确定要停止搜索吗？"):
            searching = False  # 停止搜索
            result_text.insert(tk.END, "搜索已结束。\n")  # 输出搜索结束消息
            messagebox.showinfo("提示", "搜索已结束。")
    else:
        messagebox.showinfo("提示", "当前没有进行搜索！")

def clear_button_clicked():
    """
    当点击清除按钮时执行清除搜索框信息操作
    """
    directory_entry.delete(0, tk.END)
    keyword_entry.delete(0, tk.END)
    filename_entry.delete(0, tk.END)
    result_text.delete(1.0, tk.END)

# 创建主窗口
root = tk.Tk()
root.title("文件搜索工具")

# 添加目录输入框
directory_label = tk.Label(root, text="目录：")
directory_label.grid(row=0, column=0, padx=5, pady=5)
directory_entry = tk.Entry(root)
directory_entry.grid(row=0, column=1, padx=5, pady=5)

# 添加关键字输入框
keyword_label = tk.Label(root, text="关键字：")
keyword_label.grid(row=1, column=0, padx=5, pady=5)
keyword_entry = tk.Entry(root)
keyword_entry.grid(row=1, column=1, padx=5, pady=5)

# 添加文件名输入框
filename_label = tk.Label(root, text="文件名：")
filename_label.grid(row=2, column=0, padx=5, pady=5)
filename_entry = tk.Entry(root)
filename_entry.grid(row=2, column=1, padx=5, pady=5)

# 添加确定按钮
search_button = tk.Button(root, text="确定", command=search_button_clicked)
search_button.grid(row=3, column=0, padx=5, pady=5)

# 添加取消按钮
cancel_button = tk.Button(root, text="取消", command=cancel_button_clicked)
cancel_button.grid(row=3, column=1, padx=5, pady=5)

# 添加清除按钮
clear_button = tk.Button(root, text="清除", command=clear_button_clicked)
clear_button.grid(row=3, column=2, padx=5, pady=5)

# 添加结果框
result_text = tk.Text(root, height=10, width=50)
result_text.grid(row=4, columnspan=3, padx=5, pady=5)

# 启动主循环
root.mainloop()
