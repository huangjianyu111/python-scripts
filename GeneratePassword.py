import tkinter as tk
from tkinter import messagebox
import random
import string


def generate_password(length, use_letters=True, use_digits=True, special_option="random"):
    characters = ''
    if use_letters:
        characters += string.ascii_letters
    if use_digits:
        characters += string.digits
    if special_option == "random":
        characters += string.punctuation
    elif special_option == "fixed":
        characters += "@#￥"

    password = ''.join(random.choice(characters) for _ in range(length))
    # 确保生成的密码包含所选规则的字符
    if use_letters and not any(char.isalpha() for char in password):
        password += random.choice(string.ascii_letters)
    if use_digits and not any(char.isdigit() for char in password):
        password += random.choice(string.digits)

    return password


def generate_and_fill_password():
    try:
        length = int(length_entry.get())
        if length <= 0:
            messagebox.showerror("错误", "密码长度必须是一个正整数。")
            return

        use_letters = letters_var.get()
        use_digits = digits_var.get()
        special_option = special_option_var.get()

        password = generate_password(length, use_letters, use_digits, special_option)
        password_entry.delete(0, tk.END)
        password_entry.insert(0, password)
    except ValueError:
        messagebox.showerror("错误", "请输入一个有效的整数作为密码长度。")


def on_window_open():
    # 获取当前鼠标位置
    x = root.winfo_pointerx()
    y = root.winfo_pointery()
    # 设置窗口位置在光标附近
    root.geometry(f"+{x}+{y}")
    # 调整窗口大小为原来的两倍
    root.geometry("x".join(str(int(dim) * 2) for dim in root.geometry().split("+")[0].split("x")))


# 创建主窗口
root = tk.Tk()
root.title("密码生成器")

# 创建密码长度输入框和标签
length_label = tk.Label(root, text="密码长度：")
length_label.grid(row=0, column=0, padx=5, pady=5)
length_entry = tk.Entry(root)
length_entry.grid(row=0, column=1, padx=5, pady=5)

# 创建复选框以选择密码规则
letters_var = tk.BooleanVar()
letters_var.set(True)
letters_checkbutton = tk.Checkbutton(root, text="字母", variable=letters_var)
letters_checkbutton.grid(row=1, column=0, padx=5, pady=5)

digits_var = tk.BooleanVar()
digits_var.set(True)
digits_checkbutton = tk.Checkbutton(root, text="数字", variable=digits_var)
digits_checkbutton.grid(row=1, column=1, padx=5, pady=5)

special_option_var = tk.StringVar()
special_option_var.set("random")
special_option_label = tk.Label(root, text="特殊字符：")
special_option_label.grid(row=2, column=0, padx=5, pady=5)
special_option_menu = tk.OptionMenu(root, special_option_var, "random", "fixed")
special_option_menu.grid(row=2, column=1, columnspan=2, padx=5, pady=5)

# 创建生成密码按钮
generate_button = tk.Button(root, text="生成密码", command=generate_and_fill_password)
generate_button.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

# 创建显示密码的文本框
password_entry = tk.Entry(root)
password_entry.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

# 设置窗口位置在光标附近
root.update()
root.after(0, on_window_open)

# 运行主循环
root.mainloop()
