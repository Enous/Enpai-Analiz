import os
import shutil
import threading
import time
import random
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from PIL import Image

# --- CONFIGURATION ---
DEFAULT_DOWNLOADS = str(Path.home() / "Downloads")
DEFAULT_TARGET = "D:\\Enpai_Organized"

CATEGORIES = {
    "Kodlama": [".py", ".js", ".cpp", ".h", ".java", ".html", ".css", ".ts", ".go", ".rs", ".php", ".sql", ".au3", ".ipynb", ".c", ".cs"],
    "Oyun": [".exe", ".msi", ".iso", ".pak", ".vpk", ".rpf", ".bin", ".dat"],
    "Arşiv": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
    "Medya": [".jpg", ".jpeg", ".png", ".gif", ".jfif", ".mp4", ".mkv", ".mov", ".avi", ".mp3", ".wav", ".flac"],
    "Belgeler": [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".md"],
    "3D_Tasarım": [".stl", ".obj", ".fbx", ".3ds", ".dae"]
}

CATEGORY_COLORS = {
    "Kodlama": "#7F00FF",
    "Oyun": "#FF4444",
    "Arşiv": "#FFBB00",
    "Medya": "#00CCFF",
    "Belgeler": "#00FF66",
    "3D_Tasarım": "#FF00FF",
    "Diğer": "#888888",
    "Yazılım": "#AA66CC"
}

GAME_KEYWORDS = ["setup", "game", "crack", "repack", "fitgirl", "dodi", "steam", "launcher"]

# --- LOGIC ---
class FileOrganizerLogic:
    @staticmethod
    def get_category(filename):
        ext = os.path.splitext(filename)[1].lower()
        name_lower = filename.lower()
        
        # Check by extension first
        for category, extensions in CATEGORIES.items():
            if ext in extensions:
                if ext == ".exe" or ext == ".msi":
                    if any(kw in name_lower for kw in GAME_KEYWORDS):
                        return "Oyun"
                    else:
                        return "Yazılım"
                return category
        
        if any(kw in name_lower for kw in GAME_KEYWORDS):
            return "Oyun"
            
        return "Diğer"

    @staticmethod
    def format_size(size_bytes):
        if size_bytes == 0: return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB")
        i = int(os.path.log(size_bytes, 1024)) if size_bytes > 0 else 0
        p = os.path.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_name[i]}"

    @staticmethod
    def get_file_info(filename, downloads_path):
        path = os.path.join(downloads_path, filename)
        try:
            size = os.path.getsize(path)
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024.0:
                    return f"{size:.1f} {unit}"
                size /= 1024.0
            return f"{size:.1f} TB"
        except: return "N/A"

    @staticmethod
    def scan_files(downloads_path):
        if not os.path.exists(downloads_path):
            return []
        
        files = [f for f in os.listdir(downloads_path) if os.path.isfile(os.path.join(downloads_path, f))]
        results = []
        for f in files:
            cat = FileOrganizerLogic.get_category(f)
            size = FileOrganizerLogic.get_file_info(f, downloads_path)
            results.append({"name": f, "category": cat, "size": size})
        return results

    @staticmethod
    def process_files(file_list, downloads_path, target_root, operation_type, progress_callback):
        if not os.path.exists(target_root):
            os.makedirs(target_root, exist_ok=True)

        total = len(file_list)
        processed = 0
        
        def process_one(f_info):
            nonlocal processed
            filename = f_info["name"]
            category = f_info["category"]
            cat_path = os.path.join(target_root, category)
            os.makedirs(cat_path, exist_ok=True)
            
            src = os.path.join(downloads_path, filename)
            dst = os.path.join(cat_path, filename)
            
            if os.path.exists(dst):
                base, ext = os.path.splitext(filename)
                dst = os.path.join(cat_path, f"{base}_{int(time.time())}{ext}")

            try:
                if operation_type == "Taşı": shutil.move(src, dst)
                else: shutil.copy2(src, dst)
            except: pass
            
            processed += 1
            progress_callback(processed / total)

        with ThreadPoolExecutor(max_workers=4) as exe:
            list(exe.map(process_one, file_list))

# --- UI ---
class AuroraApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Enpai Analiz - Dosya Düzenleyici")
        self.geometry("1000x800")
        
        self.pending_files = []
        self.app_state = "IDLE"
        self.src_path = DEFAULT_DOWNLOADS
        self.dst_path = DEFAULT_TARGET
        
        ctk.set_appearance_mode("Dark")
        self.configure(fg_color="#08080A")

        # Background Animation Canvas
        self.canvas = tk.Canvas(self, bg="#08080A", highlightthickness=0)
        self.canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        self.particles = []
        self.create_particles()
        self.animate_bg()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=0, padx=40, pady=30, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Header
        self.title_label = ctk.CTkLabel(self.main_frame, text="ENPAI ANALIZ", font=ctk.CTkFont(family="Orbitron", size=48, weight="bold"), text_color="#7F00FF")
        self.title_label.grid(row=0, column=0, pady=(0, 5))
        
        self.subtitle_label = ctk.CTkLabel(self.main_frame, text="Akıllı Dosya Organizasyon ve Yönetim Sistemi", font=ctk.CTkFont(size=14), text_color="#00CCFF")
        self.subtitle_label.grid(row=1, column=0, pady=(0, 30))

        # Title Animation Variables
        self.colors = ["#7F00FF", "#8E24AA", "#9C27B0", "#BA68C8", "#9C27B0", "#8E24AA"]
        self.current_color_idx = 0
        self.animate_title()

        # Path Selection Frame
        self.path_frame = ctk.CTkFrame(self.main_frame, fg_color="#1A1A1E", corner_radius=15)
        self.path_frame.grid(row=2, column=0, sticky="ew", pady=(0, 20))
        self.path_frame.grid_columnconfigure(1, weight=1)

        # Source
        ctk.CTkLabel(self.path_frame, text="KAYNAK:", font=ctk.CTkFont(size=11, weight="bold"), text_color="#7F00FF").grid(row=0, column=0, padx=20, pady=(15, 5), sticky="w")
        self.src_entry = ctk.CTkEntry(self.path_frame, height=35, fg_color="#121215", border_color="#333333")
        self.src_entry.insert(0, self.src_path)
        self.src_entry.grid(row=1, column=0, columnspan=2, padx=20, pady=(0, 5), sticky="ew")
        self.src_btn = ctk.CTkButton(self.path_frame, text="SEÇ", width=60, height=35, fg_color="#333333", command=self.select_src)
        self.src_btn.grid(row=1, column=2, padx=(0, 20), pady=(0, 5))

        # Destination
        ctk.CTkLabel(self.path_frame, text="HEDEF:", font=ctk.CTkFont(size=11, weight="bold"), text_color="#00CCFF").grid(row=2, column=0, padx=20, pady=(10, 5), sticky="w")
        self.dst_entry = ctk.CTkEntry(self.path_frame, height=35, fg_color="#121215", border_color="#333333")
        self.dst_entry.insert(0, self.dst_path)
        self.dst_entry.grid(row=3, column=0, columnspan=2, padx=20, pady=(0, 15), sticky="ew")
        self.dst_btn = ctk.CTkButton(self.path_frame, text="SEÇ", width=60, height=35, fg_color="#333333", command=self.select_dst)
        self.dst_btn.grid(row=3, column=2, padx=(0, 20), pady=(0, 15))

        # Operation Choice Frame
        self.choice_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.choice_frame.grid(row=3, column=0, pady=(0, 15))
        
        self.op_type = ctk.StringVar(value="Taşı")
        self.move_radio = ctk.CTkRadioButton(self.choice_frame, text="Dosyaları Taşı", variable=self.op_type, value="Taşı", text_color="#E1E1E1", fg_color="#7F00FF", hover_color="#6600CC")
        self.move_radio.pack(side="left", padx=20)
        
        self.copy_radio = ctk.CTkRadioButton(self.choice_frame, text="Dosyaları Kopyala", variable=self.op_type, value="Kopyala", text_color="#E1E1E1", fg_color="#00CCFF", hover_color="#00AAEE")
        self.copy_radio.pack(side="left", padx=20)

        # Progress with Percentage
        self.progress_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.progress_frame.grid(row=4, column=0, sticky="ew", pady=(0, 10))
        self.progress_frame.grid_columnconfigure(0, weight=1)
        
        self.progress_bar = ctk.CTkProgressBar(self.progress_frame, height=14, corner_radius=7, fg_color="#1A1A1E", progress_color="#7F00FF")
        self.progress_bar.set(0)
        self.progress_bar.grid(row=0, column=0, sticky="ew")
        
        self.percent_label = ctk.CTkLabel(self.progress_frame, text="0%", font=ctk.CTkFont(size=12, weight="bold"), text_color="#00CCFF")
        self.percent_label.grid(row=0, column=1, padx=(10, 0))

        # File List Area (Replaces Log Box)
        self.file_list_frame = ctk.CTkScrollableFrame(self.main_frame, height=350, fg_color="#121215", label_text="ANALİZ EDİLEN DOSYALAR", label_font=ctk.CTkFont(size=14, weight="bold"), label_text_color="#AAAAAA")
        self.file_list_frame.grid(row=5, column=0, sticky="nsew", pady=(0, 20))
        
        self.welcome_label = ctk.CTkLabel(self.file_list_frame, text="\n\nHenüz analiz yapılmadı.\nBaşlamak için 'ANALİZ ET' butonuna basın.", text_color="#555555")
        self.welcome_label.pack(pady=50)

        # Action Buttons
        self.btn_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.btn_frame.grid(row=6, column=0, pady=10)

        self.action_btn = ctk.CTkButton(
            self.btn_frame, 
            text="DOSYALARI ANALİZ ET", 
            command=self.handle_action,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#7F00FF",
            hover_color="#6600CC",
            height=50,
            width=250
        )
        self.action_btn.pack(side="left", padx=10)

        self.clear_btn = ctk.CTkButton(
            self.btn_frame, 
            text="TEMİZLE", 
            command=self.reset_ui,
            font=ctk.CTkFont(size=16),
            fg_color="#333333",
            hover_color="#444444",
            height=50,
            width=120
        )
        self.clear_btn.pack(side="left", padx=10)

    def add_stat(self, label, value, col):
        frame = ctk.CTkFrame(self.info_frame, fg_color="transparent")
        frame.grid(row=0, column=col, padx=20, pady=15)
        ctk.CTkLabel(frame, text=label, font=ctk.CTkFont(size=11, weight="bold"), text_color="#555555").pack()
        val_label = ctk.CTkLabel(frame, text=self.truncate(value), font=ctk.CTkFont(size=13))
        val_label.pack()
        self.stat_labels[label] = val_label

    def truncate(self, text):
        return (text[:25] + '...') if len(str(text)) > 25 else text

    def select_src(self):
        path = tk.filedialog.askdirectory(initialdir=self.src_path)
        if path:
            self.src_path = path
            self.src_entry.delete(0, "end")
            self.src_entry.insert(0, path)

    def select_dst(self):
        path = tk.filedialog.askdirectory(initialdir=self.dst_path)
        if path:
            self.dst_path = path
            self.dst_entry.delete(0, "end")
            self.dst_entry.insert(0, path)

    def start_analysis(self):
        self.src_path = self.src_entry.get()
        self.dst_path = self.dst_entry.get()
        
        for widget in self.file_list_frame.winfo_children():
            widget.destroy()
            
        self.pending_files = FileOrganizerLogic.scan_files(self.src_path)
        
        if not self.pending_files:
            ctk.CTkLabel(self.file_list_frame, text="Klasör boş veya bulunamadı.", text_color="#FF4444").pack(pady=20)
            return

        for f_info in self.pending_files:
            self.create_file_card(f_info)
        
        self.action_btn.configure(text=f"ONAYLA VE {self.op_type.get().upper()}MAYI BAŞLAT", fg_color="#00AA00", hover_color="#008800")
        self.app_state = "ANALYZED"

    def create_file_card(self, f_info):
        card = ctk.CTkFrame(self.file_list_frame, fg_color="#1E1E22", height=60, corner_radius=10)
        card.pack(fill="x", padx=5, pady=5)
        
        cat_color = CATEGORY_COLORS.get(f_info["category"], "#888888")
        pill = ctk.CTkFrame(card, fg_color=cat_color, width=90, height=22, corner_radius=11)
        pill.pack(side="left", padx=12, pady=10)
        pill.pack_propagate(False)
        ctk.CTkLabel(pill, text=f_info["category"], font=ctk.CTkFont(size=9, weight="bold"), text_color="white").pack(expand=True)
        
        details_frame = ctk.CTkFrame(card, fg_color="transparent")
        details_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        name_label = ctk.CTkLabel(details_frame, text=self.truncate(f_info["name"]), font=ctk.CTkFont(size=12, weight="bold"), anchor="w")
        name_label.pack(side="top", fill="x", pady=(8, 0))
        
        size_label = ctk.CTkLabel(details_frame, text=f"Boyut: {f_info['size']}  |  Hedef: {self.dst_path}\\{f_info['category']}", font=ctk.CTkFont(size=10), text_color="#666666", anchor="w")
        size_label.pack(side="top", fill="x")

    def run_process_logic(self):
        FileOrganizerLogic.process_files(self.pending_files, self.src_path, self.dst_path, self.op_type.get(), self.update_progress)
        self.after(0, self.finish_moving)

    def finish_moving(self):
        self.action_btn.configure(state="normal", text="İŞLEM TAMAMLANDI", fg_color="#333333")
        self.stat_labels["Bekleyen"].configure(text="0 Dosya")
        for widget in self.file_list_frame.winfo_children():
            widget.destroy()
        ctk.CTkLabel(self.file_list_frame, text="\nEnpai Hızlı Transfer Tamamlandı!", text_color="#00FF66", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=50)
        
        messagebox.showinfo("Başarılı", f"Dosyalar {self.op_type.get().lower()}ndı.\nCPU/I/O Optimizasyonu Kullanıldı.")
        self.app_state = "IDLE"
        self.move_radio.configure(state="normal")
        self.copy_radio.configure(state="normal")

    def create_particles(self):
        for _ in range(30):
            x = random.randint(0, 1000)
            y = random.randint(0, 800)
            size = random.randint(1, 3)
            color = random.choice(["#7F00FF", "#00CCFF", "#1A1A1E"])
            p = self.canvas.create_oval(x, y, x+size, y+size, fill=color, outline="")
            self.particles.append([p, random.uniform(-0.5, 0.5), random.uniform(0.2, 1.0)])

    def animate_bg(self):
        for p_info in self.particles:
            self.canvas.move(p_info[0], p_info[1], p_info[2])
            pos = self.canvas.coords(p_info[0])
            if pos[1] > 800:
                self.canvas.coords(p_info[0], random.randint(0, 1000), -5, random.randint(0, 1000)+2, -3)
        self.after(30, self.animate_bg)

    def reset_ui(self):
        for widget in self.file_list_frame.winfo_children():
            widget.destroy()
        self.welcome_label = ctk.CTkLabel(self.file_list_frame, text="\n\nHenüz analiz yapılmadı.\nBaşlamak için 'ANALİZ ET' butonuna basın.", text_color="#555555")
        self.welcome_label.pack(pady=50)
        self.progress_bar.set(0)
        self.action_btn.configure(text="DOSYALARI ANALİZ ET", fg_color="#7F00FF", state="normal")
        self.stat_labels["Bekleyen"].configure(text="0 Dosya")
        self.app_state = "IDLE"
        self.pending_files = []

    def animate_title(self):
        # Pulsing color effect for the title
        color = self.colors[self.current_color_idx]
        self.title_label.configure(text_color=color)
        self.current_color_idx = (self.current_color_idx + 1) % len(self.colors)
        self.after(150, self.animate_title)

    def animate_fade_in(self):
        # Basic fade-in simulation by moving things or just showing up
        # Real fade-in is hard in standard tkinter without overlays, but we can simulate by grid appearing
        pass

if __name__ == "__main__":
    app = AuroraApp()
    app.mainloop()
