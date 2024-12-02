import tkinter as tk
from tkinter import scrolledtext, simpledialog
import requests

SERVER_URL = "http://127.0.0.1:5000"  # Адрес сервера

class SimpleChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Chat")
        self.root.geometry("400x500")

        # Установка имени пользователя
        self.username = simpledialog.askstring("Username", "Введите имя пользователя:")
        if not self.username:
            self.username = "Anonymous"

        # Список сообщений
        self.chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled')
        self.chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Поле ввода текста
        self.message_input = tk.Entry(root, font=("Arial", 14))
        self.message_input.pack(padx=10, pady=(0, 10), fill=tk.X)
        self.message_input.bind("<Return>", self.send_message)

        # Кнопка отправки
        self.send_button = tk.Button(root, text="Send", command=self.send_message)
        self.send_button.pack(padx=10, pady=10)

        # Кнопка изменения имени
        self.change_name_button = tk.Button(root, text="Change Name", command=self.change_name)
        self.change_name_button.pack(padx=10, pady=10)

        # Загрузка существующих сообщений
        self.load_messages()

    def load_messages(self):
        try:
            response = requests.get(f"{SERVER_URL}/messages")
            if response.status_code == 200:
                messages = response.json()
                for message in messages:
                    self.display_message(message["username"], message["text"])
        except Exception as e:
            self.display_message("System", f"Ошибка загрузки сообщений: {e}")

    def send_message(self, event=None):
        message = self.message_input.get().strip()
        if message:
            try:
                response = requests.post(f"{SERVER_URL}/messages", json={"username": self.username, "text": message})
                if response.status_code == 201:
                    self.display_message(self.username, message)
                    self.message_input.delete(0, tk.END)
                else:
                    self.display_message("System", "Ошибка отправки сообщения")
            except Exception as e:
                self.display_message("System", f"Ошибка соединения: {e}")

    def change_name(self):
        new_name = simpledialog.askstring("Username", "Введите новое имя пользователя:")
        if new_name:
            self.username = new_name
            self.display_message("System", f"Ваше имя изменено на {self.username}")

    def display_message(self, sender, message):
        self.chat_display.configure(state='normal')
        self.chat_display.insert(tk.END, f"{sender}: {message}\n")
        self.chat_display.see(tk.END)
        self.chat_display.configure(state='disabled')


if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleChatApp(root)
    root.mainloop()
