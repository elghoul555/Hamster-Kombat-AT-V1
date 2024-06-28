import time
import threading
import tkinter as tk
from tkinter import ttk, StringVar, OptionMenu, Frame
import pyautogui
from pynput import keyboard
import pyperclip  # Para copiar al portapapeles
from PIL import Image, ImageTk, ImageSequence

class HamsterKombat:
    def __init__(self, master):
        self.master = master
        master.title("Hamster Kombat AT V.1 🐭")

        # Inicialización de variables
        self.energy_levels = list(range(500, 20001, 500))
        self.boost_levels = list(range(1, 1001))
        self.languages = ["English", "Español", "Português", "Italiano", "中文", "台灣", "日本語", "हिंदी"]
        self.translations = {
            "English": {
                "title": "Hamster Kombat AT V.1 🐭",
                "energy": "Hamster Energy 🔋",
                "boost": "Boost ⚡ (Multitap Lvl)",
                "start": "Start Mining (F2)",
                "stop": "Stop (F3)",
                "donation": "If you want to collaborate with a donation TON:",
                "copyright": "El Ghoul @sixsicsix06",
                "status": "Status: ",
                "waiting": "Waiting",
                "mining": "Mining",
                "charging": "Charging",
                "stopped": "Stopped",
            },
            "Español": {
                "title": "Hamster Kombat AT V.1 🐭",
                "energy": "Energía del Hámster 🔋",
                "boost": "Impulso ⚡ (Nivel Multitap)",
                "start": "Iniciar Minería (F2)",
                "stop": "Detener (F3)",
                "donation": "Si quieres colaborar con una donación TON:",
                "copyright": "El Ghoul @sixsicsix06",
                "status": "Estado: ",
                "waiting": "Esperando",
                "mining": "Minando",
                "charging": "Cargando",
                "stopped": "Detenido",
            },
            "Português": {
                "title": "Hamster Kombat AT V.1 🐭",
                "energy": "Energia do Hamster 🔋",
                "boost": "Boost ⚡ (Nível Multitap)",
                "start": "Iniciar Mineração (F2)",
                "stop": "Parar (F3)",
                "donation": "Se você quiser colaborar com uma doação TON:",
                "copyright": "El Ghoul @sixsicsix06",
                "status": "Status: ",
                "waiting": "Aguardando",
                "mining": "Minerando",
                "charging": "Carregando",
                "stopped": "Parado",
            },
            "Italiano": {
                "title": "Hamster Kombat AT V.1 🐭",
                "energy": "Energia del Criceto 🔋",
                "boost": "Boost ⚡ (Livello Multitap)",
                "start": "Inizia Minare (F2)",
                "stop": "Ferma (F3)",
                "donation": "Se vuoi collaborare con una donazione TON:",
                "copyright": "El Ghoul @sixsicsix06",
                "status": "Stato: ",
                "waiting": "In attesa",
                "mining": "Minando",
                "charging": "Caricando",
                "stopped": "Fermato",
            },
            "中文": {
                "title": "Hamster Kombat AT V.1 🐭",
                "energy": "仓鼠能量 🔋",
                "boost": "提升 ⚡ (多点触控级别)",
                "start": "开始挖矿 (F2)",
                "stop": "停止 (F3)",
                "donation": "如果您想通过捐赠 TON 合作:",
                "copyright": "El Ghoul @sixsicsix06",
                "status": "状态: ",
                "waiting": "等待",
                "mining": "采矿",
                "charging": "充电",
                "stopped": "停止",
            },
            "台灣": {
                "title": "Hamster Kombat AT V.1 🐭",
                "energy": "倉鼠能量 🔋",
                "boost": "提升 ⚡ (多點觸控級別)",
                "start": "開始挖礦 (F2)",
                "stop": "停止 (F3)",
                "donation": "如果您想通過捐贈 TON 合作:",
                "copyright": "El Ghoul @sixsicsix06",
                "status": "狀態: ",
                "waiting": "等待",
                "mining": "採礦",
                "charging": "充電",
                "stopped": "停止",
            },
            "日本語": {
                "title": "Hamster Kombat AT V.1 🐭",
                "energy": "ハムスターのエネルギー 🔋",
                "boost": "ブースト ⚡ (マルチタップレベル)",
                "start": "マイニング開始 (F2)",
                "stop": "停止 (F3)",
                "donation": "寄付 TON で協力したい場合:",
                "copyright": "El Ghoul @sixsicsix06",
                "status": "ステータス: ",
                "waiting": "待機中",
                "mining": "採掘中",
                "charging": "充電中",
                "stopped": "停止",
            },
            "हिंदी": {
                "title": "Hamster Kombat AT V.1 🐭",
                "energy": "हम्सटर ऊर्जा 🔋",
                "boost": "बूस्ट ⚡ (मल्टीटैप स्तर)",
                "start": "माइनिंग शुरू करें (F2)",
                "stop": "रुकें (F3)",
                "donation": "यदि आप एक दान TON के साथ सहयोग करना चाहते हैं:",
                "copyright": "El Ghoul @sixsicsix06",
                "status": "स्थिति: ",
                "waiting": "प्रतीक्षा",
                "mining": "माइनिंग",
                "charging": "चार्जिंग",
                "stopped": "रुका हुआ",
            }
        }
        self.current_language = "English"
        self.current_energy = 500
        self.current_boost = 1
        self.energy = 500
        self.running = False
        self.status = StringVar()
        self.status.set(self.translations[self.current_language]["status"] + self.translations[self.current_language]["waiting"])
        self.time_remaining = StringVar()
        self.time_remaining.set("00:00")

        # Widgets de la interfaz de usuario
        self.create_widgets()
        self.update_language(self.current_language)

        # Configuración de hotkeys globales
        self.listener = keyboard.Listener(on_press=self.on_key_press)
        self.listener.start()

    def create_widgets(self):
        # Título
        self.title_label = tk.Label(self.master, text=self.translations[self.current_language]["title"], font=("Arial", 16, "bold"))
        self.title_label.pack()

        # Menú superior para selección de idioma
        self.menu_bar = tk.Menu(self.master)
        self.language_menu = tk.Menu(self.menu_bar, tearoff=0)
        for lang in self.languages:
            self.language_menu.add_command(label=lang, command=lambda l=lang: self.update_language(l))
        self.menu_bar.add_cascade(label="Language", menu=self.language_menu)
        self.master.config(menu=self.menu_bar)

        # Selección de energía
        self.energy_label = tk.Label(self.master, text=self.translations[self.current_language]["energy"])
        self.energy_label.pack()
        self.energy_var = StringVar()
        self.energy_var.set(self.energy_levels[0])
        self.energy_menu = ttk.Combobox(self.master, textvariable=self.energy_var, values=self.energy_levels, state="readonly")
        self.energy_menu.pack()
        self.energy_menu.bind("<<ComboboxSelected>>", self.update_energy)

        # Selección de boost
        self.boost_label = tk.Label(self.master, text=self.translations[self.current_language]["boost"])
        self.boost_label.pack()
        self.boost_var = StringVar()
        self.boost_var.set(self.boost_levels[0])
        self.boost_menu = ttk.Combobox(self.master, textvariable=self.boost_var, values=self.boost_levels, state="readonly")
        self.boost_menu.pack()
        self.boost_menu.bind("<<ComboboxSelected>>", self.update_boost)

        # Estado y barra de progreso
        self.status_label = tk.Label(self.master, textvariable=self.status)
        self.status_label.pack()

        self.progress = ttk.Progressbar(self.master, orient="horizontal", length=200, mode="determinate")
        self.progress.pack()

        self.time_label = tk.Label(self.master, textvariable=self.time_remaining)
        self.time_label.pack()

        # Botones de control
        self.button_frame = tk.Frame(self.master)
        self.button_frame.pack()

        self.start_button = tk.Button(self.button_frame, text=self.translations[self.current_language]["start"], command=self.start_mining)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(self.button_frame, text=self.translations[self.current_language]["stop"], command=self.stop_mining)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        # Sección de donaciones
        self.donation_label = tk.Label(self.master, text=self.translations[self.current_language]["donation"], fg="dark blue")
        self.donation_label.pack()

        self.wallet_address = "UQAxHLuuXTR5BusIOykegLKWDKCvmDzl9Mmls6cLIT5FA120"
        self.wallet_entry = tk.Entry(self.master, width=50)
        self.wallet_entry.insert(0, self.wallet_address)
        self.wallet_entry.configure(state='readonly')
        self.wallet_entry.pack()

        self.copy_button = tk.Button(self.master, text="Copy Wallet Address", command=self.copy_wallet_address)
        self.copy_button.pack()

        # Footer con copyright
        self.footer_frame = tk.Frame(self.master)
        self.footer_frame.pack(side="bottom", fill="x")

        self.gif_label = tk.Label(self.footer_frame)
        self.gif_label.pack()

        self.load_gif()

        self.create_copyright_label()

    def load_gif(self):
        self.gif_image = Image.open("hamster_dance.gif")
        self.gif_image = self.gif_image.resize((32, 32), Image.LANCZOS)
        self.frames = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(self.gif_image)]
        self.animate_gif(0)

    def animate_gif(self, frame_index):
        frame = self.frames[frame_index]
        self.gif_label.config(image=frame)
        next_frame_index = (frame_index + 1) % len(self.frames)
        self.master.after(100, self.animate_gif, next_frame_index)

    def copy_wallet_address(self):
        pyperclip.copy(self.wallet_address)

    def update_language(self, value):
        self.current_language = value
        self.title_label.config(text=self.translations[value]["title"])
        self.energy_label.config(text=self.translations[value]["energy"])
        self.boost_label.config(text=self.translations[value]["boost"])
        self.start_button.config(text=self.translations[value]["start"])
        self.stop_button.config(text=self.translations[value]["stop"])
        self.donation_label.config(text=self.translations[value]["donation"])
        self.status.set(self.translations[value]["status"] + self.translations[value]["waiting"])
        self.copy_button.config(text="Copy Wallet Address")
        self.wallet_entry.config(state='normal')
        self.wallet_entry.delete(0, tk.END)
        self.wallet_entry.insert(0, self.wallet_address)
        self.wallet_entry.config(state='readonly')
        self.update_copyright_label()

    def create_copyright_label(self):
        self.copyright_label = tk.Label(self.footer_frame, text=self.translations[self.current_language]["copyright"], fg="dark blue")
        self.gif_label.pack_forget()
        self.gif_label.pack()
        self.copyright_label.pack()

    def update_copyright_label(self):
        for widget in self.footer_frame.winfo_children():
            if isinstance(widget, tk.Label) and widget != self.gif_label:
                widget.destroy()
        self.create_copyright_label()

    def update_energy(self, event):
        self.current_energy = int(self.energy_var.get())
        self.energy = self.current_energy

    def update_boost(self, event):
        self.current_boost = int(self.boost_var.get())

    def start_mining(self):
        if not self.running:
            self.running = True
            self.status.set(self.translations[self.current_language]["status"] + self.translations[self.current_language]["mining"])
            threading.Thread(target=self.mine).start()

    def stop_mining(self):
        self.running = False
        self.status.set(self.translations[self.current_language]["status"] + self.translations[self.current_language]["stopped"])

    def mine(self):
        while self.running:
            self.status.set(self.translations[self.current_language]["status"] + self.translations[self.current_language]["mining"])
            threading.Thread(target=self.auto_click).start()
            deficit_per_second = (6.67 * self.current_boost) - 1
            total_time = self.current_energy / deficit_per_second
            start_time = time.time()

            while self.running and self.energy > 0:
                elapsed_time = time.time() - start_time
                self.energy = self.current_energy - deficit_per_second * elapsed_time
                self.update_progress(elapsed_time, total_time)
                remaining_time = total_time - elapsed_time
                self.time_remaining.set(time.strftime("%M:%S", time.gmtime(remaining_time)))

                if self.energy <= 0:
                    self.energy = 0
                    self.status.set(self.translations[self.current_language]["status"] + self.translations[self.current_language]["charging"])
                    self.recharge_energy()
                    break

                time.sleep(0.15)  # 150 ms para autoclic

    def recharge_energy(self):
        total_recharge_time = self.current_energy
        start_time = time.time()

        while self.running and self.energy < self.current_energy:
            elapsed_time = time.time() - start_time
            self.energy = min(self.current_energy, elapsed_time)
            self.update_progress(elapsed_time, total_recharge_time, charging=True)
            remaining_time = total_recharge_time - elapsed_time
            self.time_remaining.set(time.strftime("%M:%S", time.gmtime(remaining_time)))

            if self.energy >= self.current_energy:
                self.energy = self.current_energy
                self.status.set(self.translations[self.current_language]["status"] + self.translations[self.current_language]["mining"])
                threading.Thread(target=self.auto_click).start()
                break

            time.sleep(1)

    def update_progress(self, elapsed_time, total_time, charging=False):
        progress = elapsed_time / total_time * 100
        self.progress['value'] = progress
        if charging:
            self.progress['style'] = 'green.Horizontal.TProgressbar'
        else:
            self.progress['style'] = 'orange.Horizontal.TProgressbar'

    def auto_click(self):
        while self.running and self.status.get() == self.translations[self.current_language]["status"] + self.translations[self.current_language]["mining"]:
            pyautogui.doubleClick()
            time.sleep(0.15)  # 150 ms entre clics

    def on_key_press(self, key):
        try:
            if key == keyboard.Key.f2:
                self.start_mining()
            elif key == keyboard.Key.f3:
                self.stop_mining()
        except AttributeError:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    my_gui = HamsterKombat(root)
    root.mainloop()
