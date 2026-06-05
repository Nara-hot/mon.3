import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox


class GreetingApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Greeting Bot с историей")
        self.root.geometry("600x450")

        # Переменные для хранения данных
        self.history_file = "history.txt"
        self.full_history = []  # Все записи из файла
        self.favorites = []  # Список любимых имен
        self.last_name = None  # Имя из последнего приветствия

        # --- ИНТЕРФЕЙС ---

        # Блок ввода имени и генерации приветствия
        input_frame = tk.Frame(root)
        input_frame.pack(pady=10, fill=tk.X, padx=10)

        tk.Label(input_frame, text="Введите имя:").pack(side=tk.LEFT, padx=5)
        self.name_entry = tk.Entry(input_frame, font=("Arial", 12))
        self.name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        greet_btn = tk.Button(
            input_frame, text="Приветствовать", command=self.generate_greeting
        )
        greet_btn.pack(side=tk.LEFT, padx=5)

        # Главный экран для вывода последнего приветствия
        self.output_label = tk.Label(
            root, text="", font=("Arial", 14, "bold"), fg="darkgreen", pady=10
        )
        self.output_label.pack()

        # Кнопка Избранного (Задача 2)
        self.fav_btn = tk.Button(
            root,
            text="⭐ Добавить имя в избранное",
            state=tk.DISABLED,
            command=self.add_to_favorites,
        )
        self.fav_btn.pack(pady=5)

        # Основной контент: История и Избранное
        content_frame = tk.Frame(root)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Левая колонка: История и фильтры
        history_frame = tk.LabelFrame(content_frame, text="История приветствий")
        history_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        # Кнопки фильтрации времени (Задача 3)
        filter_frame = tk.Frame(history_frame)
        filter_frame.pack(fill=tk.X, pady=2)
        tk.Button(
            filter_frame, text="Утро (<12:00)", command=lambda: self.filter_history("morning")
        ).pack(side=tk.LEFT, expand=True, fill=tk.X)
        tk.Button(
            filter_frame, text="Вечер (≥12:00)", command=lambda: self.filter_history("evening")
        ).pack(side=tk.LEFT, expand=True, fill=tk.X)
        tk.Button(
            filter_frame, text="Сбросить", command=lambda: self.filter_history("all")
        ).pack(side=tk.LEFT, expand=True, fill=tk.X)

        self.history_listbox = tk.Listbox(history_frame, font=("Courier", 10))
        self.history_listbox.pack(fill=tk.BOTH, expand=True, pady=5)

        # Правая колонка: Избранные имена
        fav_frame = tk.LabelFrame(content_frame, text="⭐ Любимые имена")
        fav_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

        self.fav_listbox = tk.Listbox(fav_frame, font=("Arial", 10), fg="blue")
        self.fav_listbox.pack(fill=tk.BOTH, expand=True, pady=5)

        # Автоматическая загрузка истории при старте (Задача 1)
        self.load_history_from_file()

    # --- ЛОГИКА И СТРУКТУРА ЗАДАЧ ---

    # 1 & 4. Генерация, запись, срезы и лимиты
    def generate_greeting(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Ошибка", "Имя не может быть пустым!")
            return

        self.last_name = name  # Запоминаем для Избранного
        self.fav_btn.config(state=tk.NORMAL)  # Активируем кнопку "В избранное"

        # Формируем строку приветствия с текущим временем
        now = datetime.now()
        time_str = now.strftime("%H:%M:%S")
        greeting_text = f"Привет, {name}!"

        # Обновляем главный лейбл
        self.output_label.config(text=greeting_text)
        self.name_entry.delete(0, tk.END)

        # Логическая запись для истории
        history_entry = f"[{time_str}] {greeting_text}"

        # Сохраняем в файл (Задача 1)
        with open(self.history_file, "a", encoding="utf-8") as f:
            f.write(history_entry + "\n")

        # Добавляем в оперативную память и срезаем до последних 5 (Задача 4)
        self.full_history.append(history_entry)
        self.full_history = self.full_history[-5:]

        # Синхронизируем файл (перезаписываем только актуальный топ-5)
        with open(self.history_file, "w", encoding="utf-8") as f:
            for line in self.full_history:
                f.write(line + "\n")

        # Обновляем UI
        self.update_history_ui(self.full_history)

    # 1. Чтение файла при запуске
    def load_history_from_file(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, "r", encoding="utf-8") as f:
                # Читаем строки, удаляя пробелы по краям
                lines = [line.strip() for line in f.readlines() if line.strip()]
                # Применяем ограничение в 5 элементов сразу на старте
                self.full_history = lines[-5:]

            self.update_history_ui(self.full_history)

    # 2. Добавление в Избранное
    def add_to_favorites(self):
        if self.last_name and self.last_name not in self.favorites:
            self.favorites.append(self.last_name)

            # Обновление ListView интерфейса
            self.fav_listbox.delete(0, tk.END)
            for fav in self.favorites:
                self.fav_listbox.insert(tk.END, f"  👤 {fav}")

            self.fav_btn.config(state=tk.DISABLED)  # Деактивируем повтор

    # 3. Фильтрация по времени
    def filter_history(self, filter_type):
        if filter_type == "all":
            self.update_history_ui(self.full_history)
            return

        filtered_list = []
        for entry in self.full_history:
            try:
                # Извлекаем "[HH:MM:SS]" -> парсим только часы
                time_part = entry.split("]")[0].replace("[", "")
                hour = int(time_part.split(":")[0])

                if filter_type == "morning" and hour < 12:
                    filtered_list.append(entry)
                elif filter_type == "evening" and hour >= 12:
                    filtered_list.append(entry)
            except (ValueError, IndexError):
                continue  # Пропускаем поврежденные строки

        self.update_history_ui(filtered_list)

    # Вспомогательная функция обновления интерфейса истории
    def update_history_ui(self, records_list):
        self.history_listbox.delete(0, tk.END)
        for record in records_list:
            self.history_listbox.insert(tk.END, record)


if __name__ == "__main__":
    root = tk.Tk()
    app = GreetingApp(root)
    root.mainloop()
