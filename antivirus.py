import os
import subprocess
import sys
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, simpledialog, filedialog
import winreg


class AntivirusWinRE:
    def __init__(self, root):
        self.root = root
        self.root.title("MTTUnlocker - Антивирус для WinRE")
        self.root.geometry("1000x700")
        self.root.configure(bg='#2b2b2b')

        # Переменная для пути к целевой Windows
        self.target_drive = tk.StringVar(value="C:")

        self.create_widgets()

    def resource_path(self, relative_path):
        """Получить путь к ресурсу, работает для dev и для PyInstaller."""
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_path, relative_path)

    def run_batch(self, batch_file, *args):
        """Запускает batch-файл из папки helper_scripts и возвращает вывод."""
        try:
            batch_path = self.resource_path(os.path.join("helper_scripts", batch_file))
            if not os.path.exists(batch_path):
                return f"Batch файл не найден: {batch_path}"

            cmd = [batch_path] + list(args)
            result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
            return result.stdout + result.stderr
        except Exception as e:
            return f"Ошибка запуска batch: {e}"

    def create_widgets(self):
        # Верхняя панель с выбором диска
        top_frame = tk.Frame(self.root, bg='#3c3f41', height=40)
        top_frame.pack(fill=tk.X, padx=5, pady=5)
        top_frame.pack_propagate(False)

        tk.Label(top_frame, text="Диск с Windows:", bg='#3c3f41', fg='white', font=('Arial', 10)).pack(side=tk.LEFT,
                                                                                                       padx=10)
        drive_entry = tk.Entry(top_frame, textvariable=self.target_drive, width=5, font=('Arial', 10), bg='#1e1e1e',
                               fg='white', insertbackground='white')
        drive_entry.pack(side=tk.LEFT, padx=5)

        tk.Button(top_frame, text="Загрузить реестр", command=self.load_registry_hives,
                  bg='#4CAF50', fg='white', font=('Arial', 9, 'bold'), padx=10).pack(side=tk.LEFT, padx=20)

        tk.Button(top_frame, text="Выход", command=self.root.quit,
                  bg='#f44336', fg='white', font=('Arial', 9, 'bold'), padx=10).pack(side=tk.RIGHT, padx=10)

        # Основная область
        main_frame = tk.Frame(self.root, bg='#2b2b2b')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Левая панель с кнопками (используем Canvas + Scrollbar)
        left_canvas = tk.Canvas(main_frame, bg='#2b2b2b', highlightthickness=0, width=280)
        left_canvas.pack(side=tk.LEFT, fill=tk.Y)

        scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=left_canvas.yview)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y)

        left_canvas.configure(yscrollcommand=scrollbar.set)

        btn_frame = tk.Frame(left_canvas, bg='#2b2b2b')
        left_canvas.create_window((0, 0), window=btn_frame, anchor='nw', width=260)

        # Правая панель с выводом информации
        right_frame = tk.Frame(main_frame, bg='#2b2b2b')
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Заголовок вывода
        output_label = tk.Label(right_frame, text="Информация:", bg='#2b2b2b', fg='#ffa500',
                                font=('Arial', 12, 'bold'), anchor='w')
        output_label.pack(fill=tk.X, padx=5, pady=(0, 5))

        # Текстовое поле для вывода
        self.output = scrolledtext.ScrolledText(right_frame, bg='#1e1e1e', fg='#d4d4d4',
                                                insertbackground='white', wrap=tk.WORD, font=('Consolas', 9))
        self.output.pack(fill=tk.BOTH, expand=True)

        # Строка статуса
        self.status = tk.Label(self.root, text="Готов", bd=1, relief=tk.SUNKEN, anchor=tk.W,
                               bg='#3c3f41', fg='white', font=('Arial', 9))
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

        # Группы кнопок
        categories = [
            ("🔧 СИСТЕМА", [
                ("📝 Редактор реестра", self.open_regedit),
                ("👥 Менеджер пользователей", self.manage_users),
                ("📊 Диспетчер задач", self.task_manager),
                ("🚀 Автозапуск", self.startup_manager),
                ("📁 Файловый менеджер", self.file_manager),
                ("🐞 Дебаггеры", self.debuggers),
                ("🪟 Winlogon", self.winlogon_info),
            ]),
            ("🛡️ ДИАГНОСТИКА", [
                ("🔍 Сканирование на вирусы", self.scan_viruses),
                ("⚙️ Управление службами", self.manage_services),
                ("🌐 Сетевые соединения", self.network_connections),
                ("📋 Проверка hosts", self.check_hosts),
                ("🛠️ SFC Scan", self.sfc_scan),
                ("⏰ Планировщик задач", self.scheduled_tasks),
                ("💽 Анализ MBR", self.check_mbr),
            ]),
            ("⚡ ДОПОЛНИТЕЛЬНО", [
                ("🧹 Очистка временных файлов", self.clean_temp),
                ("📦 Карантин", self.open_quarantine),
                ("ℹ️ О программе", self.about),
            ]),
        ]

        row = 0
        for cat_name, func_list in categories:
            label = tk.Label(btn_frame, text=cat_name, bg='#2b2b2b', fg='#ffa500',
                             font=('Arial', 11, 'bold'), anchor='w')
            label.grid(row=row, column=0, pady=(15, 5), padx=10, sticky='w')
            row += 1

            for text, command in func_list:
                btn = tk.Button(btn_frame, text=text, width=30, height=1, command=command,
                                bg='#3c3f41', fg='white', font=('Arial', 9),
                                activebackground='#4c4c4c', activeforeground='white',
                                bd=1, relief=tk.RAISED)
                btn.grid(row=row, column=0, pady=2, padx=5, sticky='w')
                row += 1

        btn_frame.update_idletasks()
        left_canvas.configure(scrollregion=left_canvas.bbox('all'))

        def on_mousewheel(event):
            left_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        left_canvas.bind_all("<MouseWheel>", on_mousewheel)

    def log(self, message):
        self.output.insert(tk.END, message + "\n")
        self.output.see(tk.END)
        self.root.update()

    def set_status(self, text):
        self.status.config(text=text)
        self.root.update()

    def show_output_window(self, title, text):
        win = tk.Toplevel(self.root)
        win.title(title)
        win.geometry("700x500")
        win.configure(bg='#2b2b2b')

        txt = scrolledtext.ScrolledText(win, bg='#1e1e1e', fg='#d4d4d4', font=('Consolas', 9))
        txt.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        txt.insert(tk.END, text)

    def load_registry_hives(self):
        drive = self.target_drive.get().rstrip('\\')
        system_hive = f"{drive}\\Windows\\System32\\config\\SYSTEM"
        software_hive = f"{drive}\\Windows\\System32\\config\\SOFTWARE"

        if not os.path.exists(system_hive) or not os.path.exists(software_hive):
            messagebox.showerror("Ошибка", "Не найдены файлы кустов реестра!\n"
                                           "Убедитесь, что указан правильный диск с Windows.")
            return

        self.set_status("Загрузка кустов реестра...")
        self.log("🔄 Загрузка кустов реестра...")

        try:
            subprocess.run("reg.exe unload HKLM\\Temp_SYSTEM", shell=True, stderr=subprocess.DEVNULL)
            subprocess.run("reg.exe unload HKLM\\Temp_SOFTWARE", shell=True, stderr=subprocess.DEVNULL)
        except:
            pass

        try:
            subprocess.run(f'reg.exe load HKLM\\Temp_SYSTEM "{system_hive}"', check=True, shell=True)
            subprocess.run(f'reg.exe load HKLM\\Temp_SOFTWARE "{software_hive}"', check=True, shell=True)
            self.log("✅ Кусты реестра загружены в HKLM\\Temp_SYSTEM и HKLM\\Temp_SOFTWARE")
            self.set_status("Реестр загружен")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить кусты: {e}")
            self.set_status("Ошибка загрузки реестра")

    # ---------- Функции ----------

    def open_regedit(self):
        self.log("📝 Запуск regedit.exe (перейдите к HKLM\\Temp_SYSTEM и Temp_SOFTWARE)")
        subprocess.Popen("regedit.exe")

    def manage_users(self):
        win = tk.Toplevel(self.root)
        win.title("👥 Менеджер пользователей")
        win.geometry("700x500")
        win.configure(bg='#2b2b2b')

        # Список пользователей
        list_frame = tk.Frame(win, bg='#2b2b2b')
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        listbox = tk.Listbox(list_frame, bg='#1e1e1e', fg='#d4d4d4', font=('Consolas', 9))
        scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL, command=listbox.yview)
        listbox.configure(yscrollcommand=scrollbar.set)

        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Кнопки
        btn_frame = tk.Frame(win, bg='#2b2b2b')
        btn_frame.pack(fill=tk.X, padx=5, pady=5)

        buttons = [
            ("🔄 Обновить", lambda: self.refresh_users(listbox)),
            ("➕ Добавить", lambda: self.add_user_dialog(listbox)),
            ("❌ Удалить", lambda: self.delete_user(listbox)),
            ("🔒 Заблокировать", lambda: self.disable_user(listbox)),
            ("🔓 Разблокировать", lambda: self.enable_user(listbox)),
            ("🔑 Сменить пароль", lambda: self.change_password(listbox)),
        ]

        for text, cmd in buttons:
            tk.Button(btn_frame, text=text, command=cmd, bg='#3c3f41', fg='white',
                      font=('Arial', 9), padx=10).pack(side=tk.LEFT, padx=2)

        self.refresh_users(listbox)

    def refresh_users(self, listbox):
        listbox.delete(0, tk.END)
        output = self.run_batch("list_users.bat")
        lines = output.splitlines()
        for line in lines:
            if line.strip():
                listbox.insert(tk.END, line)

    def add_user_dialog(self, listbox):
        username = simpledialog.askstring("➕ Добавление пользователя", "Имя пользователя:")
        if not username:
            return
        password = simpledialog.askstring("➕ Добавление пользователя", "Пароль:", show='*')
        if password is None:
            return

        output = self.run_batch("add_user.bat", username, password)
        messagebox.showinfo("Результат", output)
        self.refresh_users(listbox)

    def delete_user(self, listbox):
        selection = listbox.curselection()
        if not selection:
            messagebox.showwarning("Внимание", "Выберите пользователя из списка")
            return

        line = listbox.get(selection[0])
        username = line.split()[0] if line.split() else ""

        if messagebox.askyesno("Подтверждение", f"Удалить пользователя {username}?"):
            output = self.run_batch("delete_user.bat", username)
            messagebox.showinfo("Результат", output)
            self.refresh_users(listbox)

    def disable_user(self, listbox):
        selection = listbox.curselection()
        if not selection:
            return
        username = listbox.get(selection[0]).split()[0]
        output = self.run_batch("disable_user.bat", username)
        messagebox.showinfo("Результат", output)
        self.refresh_users(listbox)

    def enable_user(self, listbox):
        selection = listbox.curselection()
        if not selection:
            return
        username = listbox.get(selection[0]).split()[0]
        output = self.run_batch("enable_user.bat", username)
        messagebox.showinfo("Результат", output)
        self.refresh_users(listbox)

    def change_password(self, listbox):
        selection = listbox.curselection()
        if not selection:
            return
        username = listbox.get(selection[0]).split()[0]
        password = simpledialog.askstring("🔑 Смена пароля", "Новый пароль:", show='*')
        if password:
            output = self.run_batch("change_password.bat", username, password)
            messagebox.showinfo("Результат", output)

    def task_manager(self):
        win = tk.Toplevel(self.root)
        win.title("📊 Диспетчер задач")
        win.geometry("900x500")
        win.configure(bg='#2b2b2b')

        # Таблица процессов
        columns = ('PID', 'Имя', 'Сессия', 'Память', 'Состояние')
        tree = ttk.Treeview(win, columns=columns, show='headings', height=20)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)

        scrollbar = ttk.Scrollbar(win, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=5)

        btn_frame = tk.Frame(win, bg='#2b2b2b')
        btn_frame.pack(fill=tk.X, padx=5, pady=5)

        def refresh():
            for row in tree.get_children():
                tree.delete(row)

            output = self.run_batch("list_processes.bat")
            lines = output.splitlines()

            for line in lines[3:]:  # Пропускаем заголовки
                parts = line.split()
                if len(parts) >= 8:
                    name = parts[0]
                    pid = parts[1] if len(parts) > 1 else ''
                    session = parts[2] if len(parts) > 2 else ''
                    mem = parts[4] if len(parts) > 4 else ''
                    status = parts[7] if len(parts) > 7 else ''
                    tree.insert('', tk.END, values=(pid, name, session, mem, status))

        def kill_selected():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Внимание", "Выберите процесс")
                return
            values = tree.item(selected[0], 'values')
            pid = values[0]
            if messagebox.askyesno("Подтверждение", f"Завершить процесс PID {pid}?"):
                output = self.run_batch("kill_process.bat", pid)
                messagebox.showinfo("Результат", output)
                refresh()

        tk.Button(btn_frame, text="🔄 Обновить", command=refresh,
                  bg='#3c3f41', fg='white', padx=15).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="⛔ Завершить процесс", command=kill_selected,
                  bg='#f44336', fg='white', padx=15).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="👁️ Проверить скрытые",
                  command=lambda: self.show_output_window("Скрытые процессы",
                                                          self.run_batch("check_hidden_processes.bat")),
                  bg='#3c3f41', fg='white', padx=15).pack(side=tk.LEFT, padx=2)

        refresh()

    def startup_manager(self):
        win = tk.Toplevel(self.root)
        win.title("🚀 Автозагрузка")
        win.geometry("900x600")
        win.configure(bg='#2b2b2b')

        text = scrolledtext.ScrolledText(win, bg='#1e1e1e', fg='#d4d4d4', font=('Consolas', 9))
        text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        output = self.run_batch("startup_places.bat", self.target_drive.get())
        text.insert(tk.END, output)

        btn_frame = tk.Frame(win, bg='#2b2b2b')
        btn_frame.pack(fill=tk.X, padx=5, pady=5)

        tk.Button(btn_frame, text="🔄 Обновить",
                  command=lambda: [text.delete(1.0, tk.END),
                                   text.insert(tk.END, self.run_batch("startup_places.bat", self.target_drive.get()))],
                  bg='#3c3f41', fg='white', padx=15).pack(side=tk.LEFT, padx=2)

    def file_manager(self):
        win = tk.Toplevel(self.root)
        win.title("📁 Файловый менеджер")
        win.geometry("900x600")
        win.configure(bg='#2b2b2b')

        current_path = tk.StringVar(value=self.target_drive.get() + "\\")

        # Адресная строка
        addr_frame = tk.Frame(win, bg='#2b2b2b')
        addr_frame.pack(fill=tk.X, padx=5, pady=5)

        tk.Entry(addr_frame, textvariable=current_path, bg='#1e1e1e', fg='white',
                 insertbackground='white', font=('Arial', 9)).pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Button(addr_frame, text="Перейти", command=lambda: load_dir(),
                  bg='#3c3f41', fg='white').pack(side=tk.RIGHT, padx=2)

        # Список файлов
        list_frame = tk.Frame(win, bg='#2b2b2b')
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        listbox = tk.Listbox(list_frame, bg='#1e1e1e', fg='#d4d4d4', font=('Consolas', 9))
        scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL, command=listbox.yview)
        listbox.configure(yscrollcommand=scrollbar.set)

        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Кнопки действий
        btn_frame = tk.Frame(win, bg='#2b2b2b')
        btn_frame.pack(fill=tk.X, padx=5, pady=5)

        def load_dir():
            path = current_path.get()
            listbox.delete(0, tk.END)
            try:
                items = os.listdir(path)
                for item in sorted(items):
                    listbox.insert(tk.END, item)
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))

        def on_double_click(event):
            selection = listbox.curselection()
            if not selection:
                return
            item = listbox.get(selection[0])
            new_path = os.path.join(current_path.get(), item)
            if os.path.isdir(new_path):
                current_path.set(new_path)
                load_dir()
            else:
                self.show_output_window("Информация о файле",
                                        f"Файл: {new_path}\nРазмер: {os.path.getsize(new_path)} байт\n"
                                        f"Дата изменения: {os.path.getmtime(new_path)}")

        listbox.bind('<Double-Button-1>', on_double_click)

        def delete_selected():
            selection = listbox.curselection()
            if not selection:
                return
            item = listbox.get(selection[0])
            full = os.path.join(current_path.get(), item)
            if messagebox.askyesno("Подтверждение", f"Удалить {item}?"):
                try:
                    if os.path.isdir(full):
                        os.rmdir(full)
                    else:
                        os.remove(full)
                    load_dir()
                except Exception as e:
                    messagebox.showerror("Ошибка", str(e))

        def quarantine_selected():
            selection = listbox.curselection()
            if not selection:
                return
            item = listbox.get(selection[0])
            full = os.path.join(current_path.get(), item)
            output = self.run_batch("quarantine.bat", self.target_drive.get(), full)
            messagebox.showinfo("Результат", output)
            load_dir()

        tk.Button(btn_frame, text="❌ Удалить", command=delete_selected,
                  bg='#f44336', fg='white', padx=10).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="📦 В карантин", command=quarantine_selected,
                  bg='#ff9800', fg='white', padx=10).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="ℹ️ Свойства",
                  command=lambda: properties_selected() if listbox.curselection() else None,
                  bg='#3c3f41', fg='white', padx=10).pack(side=tk.LEFT, padx=2)

        def properties_selected():
            selection = listbox.curselection()
            if not selection:
                return
            item = listbox.get(selection[0])
            full = os.path.join(current_path.get(), item)
            info = f"Имя: {item}\n"
            info += f"Путь: {full}\n"
            if os.path.exists(full):
                info += f"Размер: {os.path.getsize(full)} байт\n"
                info += f"Дата изменения: {os.path.getmtime(full)}"
            self.show_output_window("Свойства", info)

        load_dir()

    def debuggers(self):
        output = self.run_batch("check_debuggers.bat")
        self.show_output_window("🐞 Дебаггеры и руткиты", output)

    def winlogon_info(self):
        output = self.run_batch("winlogon_info.bat")
        win = tk.Toplevel(self.root)
        win.title("🪟 Winlogon")
        win.geometry("800x500")
        win.configure(bg='#2b2b2b')

        text = scrolledtext.ScrolledText(win, bg='#1e1e1e', fg='#d4d4d4', font=('Consolas', 9))
        text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        text.insert(tk.END, output)

        tk.Button(win, text="🔄 Восстановить по умолчанию",
                  command=lambda: self.run_batch("restore_winlogon.bat"),
                  bg='#4CAF50', fg='white', padx=15, pady=5).pack(pady=5)

    def scan_viruses(self):
        self.log("🔍 Запуск сканирования на вирусы...")
        self.set_status("Сканирование...")
        output = self.run_batch("scan_virus.bat", self.target_drive.get())
        self.show_output_window("Результаты сканирования", output)
        self.set_status("Сканирование завершено")

    def manage_services(self):
        output = self.run_batch("list_services.bat")
        win = tk.Toplevel(self.root)
        win.title("⚙️ Службы")
        win.geometry("900x600")
        win.configure(bg='#2b2b2b')

        text = scrolledtext.ScrolledText(win, bg='#1e1e1e', fg='#d4d4d4', font=('Consolas', 9))
        text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        text.insert(tk.END, output)

    def network_connections(self):
        output = self.run_batch("netstat_an.bat")
        self.show_output_window("🌐 Сетевые соединения", output)

    def check_hosts(self):
        output = self.run_batch("check_hosts.bat", self.target_drive.get())
        self.show_output_window("📋 Файл hosts", output)

    def sfc_scan(self):
        self.log("🛠️ Запуск SFC Scan...")
        self.set_status("SFC Scan...")
        output = self.run_batch("sfc_scan.bat", self.target_drive.get())
        self.show_output_window("SFC Scan", output)
        self.set_status("SFC Scan завершён")

    def scheduled_tasks(self):
        output = self.run_batch("list_tasks.bat")
        self.show_output_window("⏰ Планировщик задач", output)

    def check_mbr(self):
        output = self.run_batch("check_mbr.bat")
        self.show_output_window("💽 Анализ MBR", output)

    def clean_temp(self):
        if messagebox.askyesno("Очистка", "Очистить временные файлы?"):
            self.log("🧹 Очистка временных файлов...")
            try:
                temp_dirs = [
                    f"{self.target_drive.get()}\\Windows\\Temp",
                    f"{self.target_drive.get()}\\Users\\*\\AppData\\Local\\Temp"
                ]
                for temp_dir in temp_dirs:
                    self.run_batch("clean_temp.bat", temp_dir)
                self.log("✅ Очистка завершена")
            except Exception as e:
                self.log(f"❌ Ошибка: {e}")

    def open_quarantine(self):
        quarantine_path = f"{self.target_drive.get()}\\quarantine"
        if os.path.exists(quarantine_path):
            os.startfile(quarantine_path)
        else:
            messagebox.showinfo("Карантин", "Папка карантина не найдена")

    def about(self):
        about_text = """
MTTUnlocker - Антивирус для WinRE
Версия: 2.0
Разработано для работы в среде восстановления Windows

Функции:
• Редактор реестра
• Менеджер пользователей
• Диспетчер задач
• Управление автозагрузкой
• Файловый менеджер
• Дебаггеры и руткиты
• Сканирование на вирусы
• Управление службами
• И многое другое

© 2026 MTTUnlocker Team
        """
        messagebox.showinfo("ℹ️ О программе", about_text)


if __name__ == "__main__":
    root = tk.Tk()
    app = AntivirusWinRE(root)
    root.mainloop()