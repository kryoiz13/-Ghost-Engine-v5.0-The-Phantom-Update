import tkinter as tk
from tkinter import scrolledtext
import threading
import pyautogui as pg
import time
import re
import random
from youtube_transcript_api import YouTubeTranscriptApi

class UltraFixEngine:
    def __init__(self, root):
        self.root = root
        self.root.title("Ghost Engine v5.0 - PRO")
        self.root.geometry("500x550")
        self.root.attributes('-topmost', True) 
        self.root.configure(bg="#0a0a0a")

        pg.FAILSAFE = True 
        self.is_running = False
        self.is_paused = False

        # --- UI ---
        tk.Label(root, text="LYRIC GHOST ENGINE", fg="#00ffcc", bg="#0a0a0a", font=("Consolas", 16, "bold")).pack(pady=10)
        
        self.url_entry = tk.Entry(root, width=50, bg="#1a1a1a", fg="#00ffcc", insertbackground="white")
        self.url_entry.insert(0, "Paste YouTube Link Here")
        self.url_entry.pack(pady=5)

        btn_f = tk.Frame(root, bg="#0a0a0a")
        btn_f.pack(pady=10)
        tk.Button(btn_f, text="START (F1)", bg="#111", fg="#00ffcc", command=self.start_thread, width=10).grid(row=0, column=0, padx=5)
        tk.Button(btn_f, text="PAUSE (F2)", bg="#111", fg="#f1c40f", command=self.toggle_pause, width=10).grid(row=0, column=1, padx=5)
        tk.Button(btn_f, text="STOP (ESC)", bg="#111", fg="#e74c3c", command=self.stop_engine, width=10).grid(row=0, column=2, padx=5)

        self.log = scrolledtext.ScrolledText(root, height=12, width=60, bg="#000", fg="#00ffcc", font=("Consolas", 9))
        self.log.pack(padx=10, pady=10)

        self.status_bar = tk.Label(root, text="SYSTEM READY", fg="#00ffcc", bg="#111", width=60)
        self.status_bar.pack(side="bottom")

        self.root.bind('<F1>', lambda e: self.start_thread())
        self.root.bind('<F2>', lambda e: self.toggle_pause())
        self.root.bind('<Escape>', lambda e: self.stop_engine())

    def log_msg(self, msg):
        self.log.insert(tk.END, f">> {msg}\n")
        self.log.see(tk.END)

    def clean_url(self, url):
        if "list=" in url:
            url = url.split("list=")[0].rstrip("&").rstrip("?")
        video_id = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url)
        return video_id.group(1) if video_id else None

    def run_engine(self):
        url = self.url_entry.get()
        v_id = self.clean_url(url)
        
        if not v_id:
            self.log_msg("❌ ERROR: Link invalid.")
            return

        try:
            self.log_msg("📡 Extracting Music Data...")
            transcript = YouTubeTranscriptApi.get_transcript(v_id)
            full_text = " ".join([i['text'] for i in transcript])
            full_text = re.sub(r'\[.*?\]', '', full_text) 
            chunks = re.split(r'(?<=[.!?]) +', full_text.replace('\n', ' '))
            
            self.log_msg(f"✅ Ready! CLICK THE WHATSAPP CHAT NOW.")
            for i in range(5, 0, -1):
                self.status_bar.config(text=f"IGNITION IN {i}s...", fg="red")
                time.sleep(1)

            self.is_running = True
            self.status_bar.config(text="TYPING...", fg="#00ffcc")

            for i in range(0, len(chunks), 3): 
                if not self.is_running: break
                while self.is_paused: time.sleep(0.5)

                chunk = " ".join(chunks[i:i+3]).strip()
                if not chunk: continue

                self.log_msg(f"Sending: {chunk[:20]}...")
                for char in chunk:
                    if not self.is_running: break
                    pg.write(char)
                    time.sleep(random.uniform(0.01, 0.04)) 
                
                pg.press("enter")
                time.sleep(random.uniform(1.5, 3.0))

            self.log_msg("🏁 MISSION COMPLETE.")
            self.is_running = False
            self.status_bar.config(text="IDLE", fg="#00ffcc")

        except Exception as e:
            self.log_msg(f"⚠️ BUG: {str(e)}")
            self.is_running = False

    def start_thread(self):
        if not self.is_running:
            threading.Thread(target=self.run_engine, daemon=True).start()

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        self.log_msg("⏸ PAUSED" if self.is_paused else "▶ RESUMED")

    def stop_engine(self):
        self.is_running = False
        self.log_msg("🛑 EMERGENCY STOP.")

if __name__ == "__main__":
    root = tk.Tk()
    app = UltraFixEngine(root)
    root.mainloop()
