import os
import sys
import queue
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext

# If bundled as .exe without console, stdout/stderr are None. whisper/tqdm write to them.
if sys.stdout is None:
    sys.stdout = open(os.devnull, "w", encoding="utf-8")
if sys.stderr is None:
    sys.stderr = open(os.devnull, "w", encoding="utf-8")

APP_DIR = os.path.dirname(sys.executable if getattr(sys, "frozen", False) else os.path.abspath(__file__))
os.environ["PATH"] = APP_DIR + os.pathsep + os.environ.get("PATH", "")

EXTENSIONS = ('.wav', '.mp3', '.m4a', '.flac', '.ogg', '.mp4', '.mkv', '.webm', '.aac', '.wma')

MODELS = ["tiny", "base", "small", "medium", "large", "turbo"]

LANGUAGES = {
    "Auto-detect": None,
    "English": "en",
    "Українська": "uk",
    "Русский": "ru",
    "Polski": "pl",
    "Deutsch": "de",
    "Français": "fr",
    "Español": "es",
    "Italiano": "it",
    "Português": "pt",
    "Čeština": "cs",
    "Türkçe": "tr",
    "日本語": "ja",
    "中文": "zh",
}

TASKS = {
    "Transcribe (original language)": "transcribe",
    "Translate to English": "translate",
}

DEVICES = {
    "Auto": "auto",
    "GPU (CUDA)": "cuda",
    "CPU": "cpu",
}


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("WhisperBatcher GUI")
        self.geometry("720x640")
        self.minsize(640, 560)

        self.log_queue = queue.Queue()
        self.stop_flag = threading.Event()
        self.worker = None
        self.model = None
        self.model_key = None

        self._build_ui()
        self.after(100, self._poll_queue)

    # ---------- UI ----------
    def _build_ui(self):
        pad = {"padx": 8, "pady": 4}

        # Folders
        frm_paths = ttk.LabelFrame(self, text="Folders")
        frm_paths.pack(fill="x", padx=10, pady=(10, 4))
        frm_paths.columnconfigure(1, weight=1)

        self.var_input = tk.StringVar(value=os.getcwd())
        self.var_output = tk.StringVar(value=os.path.join(os.getcwd(), "output"))

        ttk.Label(frm_paths, text="Input folder:").grid(row=0, column=0, sticky="w", **pad)
        ttk.Entry(frm_paths, textvariable=self.var_input).grid(row=0, column=1, sticky="ew", **pad)
        ttk.Button(frm_paths, text="Browse…", command=self._pick_input).grid(row=0, column=2, **pad)

        ttk.Label(frm_paths, text="Output folder:").grid(row=1, column=0, sticky="w", **pad)
        ttk.Entry(frm_paths, textvariable=self.var_output).grid(row=1, column=1, sticky="ew", **pad)
        ttk.Button(frm_paths, text="Browse…", command=self._pick_output).grid(row=1, column=2, **pad)

        # Settings
        frm_set = ttk.LabelFrame(self, text="Settings")
        frm_set.pack(fill="x", padx=10, pady=4)
        frm_set.columnconfigure(1, weight=1)

        self.var_model = tk.StringVar(value="medium")
        self.var_lang = tk.StringVar(value="Auto-detect")
        self.var_task = tk.StringVar(value=list(TASKS)[0])
        self.var_device = tk.StringVar(value="Auto")

        rows = [
            ("Model:", self.var_model, MODELS),
            ("Audio language:", self.var_lang, list(LANGUAGES)),
            ("Task:", self.var_task, list(TASKS)),
            ("Device:", self.var_device, list(DEVICES)),
        ]
        for r, (label, var, values) in enumerate(rows):
            ttk.Label(frm_set, text=label).grid(row=r, column=0, sticky="w", **pad)
            ttk.Combobox(frm_set, textvariable=var, values=values, state="readonly").grid(
                row=r, column=1, sticky="ew", **pad
            )

        # Formats
        frm_fmt = ttk.LabelFrame(self, text="Output formats")
        frm_fmt.pack(fill="x", padx=10, pady=4)
        self.var_txt = tk.BooleanVar(value=True)
        self.var_srt = tk.BooleanVar(value=False)
        self.var_vtt = tk.BooleanVar(value=False)
        ttk.Checkbutton(frm_fmt, text="TXT (text)", variable=self.var_txt).pack(side="left", **pad)
        ttk.Checkbutton(frm_fmt, text="SRT (subtitles)", variable=self.var_srt).pack(side="left", **pad)
        ttk.Checkbutton(frm_fmt, text="VTT (subtitles)", variable=self.var_vtt).pack(side="left", **pad)

        # Buttons
        frm_btn = ttk.Frame(self)
        frm_btn.pack(fill="x", padx=10, pady=6)
        self.btn_start = ttk.Button(frm_btn, text="▶ Start", command=self._start)
        self.btn_start.pack(side="left", padx=(0, 6))
        self.btn_stop = ttk.Button(frm_btn, text="■ Stop", command=self._stop, state="disabled")
        self.btn_stop.pack(side="left")

        # Progress
        self.progress = ttk.Progressbar(self, mode="determinate")
        self.progress.pack(fill="x", padx=10, pady=(0, 4))
        self.var_status = tk.StringVar(value="Ready")
        ttk.Label(self, textvariable=self.var_status).pack(anchor="w", padx=10)

        # Log
        self.log = scrolledtext.ScrolledText(self, height=12, state="disabled", wrap="word")
        self.log.pack(fill="both", expand=True, padx=10, pady=(4, 10))

    # ---------- Helpers ----------
    def _pick_input(self):
        d = filedialog.askdirectory(initialdir=self.var_input.get())
        if d:
            self.var_input.set(d)

    def _pick_output(self):
        d = filedialog.askdirectory(initialdir=self.var_output.get())
        if d:
            self.var_output.set(d)

    def _log(self, text):
        self.log_queue.put(("log", text))

    def _poll_queue(self):
        try:
            while True:
                kind, value = self.log_queue.get_nowait()
                if kind == "log":
                    self.log.configure(state="normal")
                    self.log.insert("end", value + "\n")
                    self.log.see("end")
                    self.log.configure(state="disabled")
                elif kind == "progress":
                    self.progress["value"] = value
                elif kind == "status":
                    self.var_status.set(value)
                elif kind == "done":
                    self.btn_start.configure(state="normal")
                    self.btn_stop.configure(state="disabled")
        except queue.Empty:
            pass
        self.after(100, self._poll_queue)

    # ---------- Start ----------
    def _start(self):
        in_dir = self.var_input.get().strip()
        out_dir = self.var_output.get().strip()
        if not os.path.isdir(in_dir):
            messagebox.showerror("Error", "Input folder does not exist.")
            return

        formats = []
        if self.var_txt.get():
            formats.append("txt")
        if self.var_srt.get():
            formats.append("srt")
        if self.var_vtt.get():
            formats.append("vtt")
        if not formats:
            messagebox.showerror("Error", "Select at least one output format.")
            return

        files = sorted(f for f in os.listdir(in_dir) if f.lower().endswith(EXTENSIONS))
        if not files:
            messagebox.showinfo("No files", "No supported audio/video files found in the input folder.")
            return

        cfg = {
            "in_dir": in_dir,
            "out_dir": out_dir,
            "files": files,
            "model": self.var_model.get(),
            "lang": LANGUAGES[self.var_lang.get()],
            "task": TASKS[self.var_task.get()],
            "device": DEVICES[self.var_device.get()],
            "formats": formats,
        }

        self.stop_flag.clear()
        self.btn_start.configure(state="disabled")
        self.btn_stop.configure(state="normal")
        self.progress["value"] = 0
        self.progress["maximum"] = len(files)

        self.worker = threading.Thread(target=self._run, args=(cfg,), daemon=True)
        self.worker.start()

    def _stop(self):
        self.stop_flag.set()
        self._log("Stopping after current file finishes…")
        self.log_queue.put(("status", "Stopping…"))

    # ---------- Worker thread ----------
    def _run(self, cfg):
        try:
            self.log_queue.put(("status", "Loading libraries…"))
            import torch
            import whisper
            from whisper.utils import get_writer

            device = cfg["device"]
            if device == "auto":
                device = "cuda" if torch.cuda.is_available() else "cpu"
            if device == "cuda" and not torch.cuda.is_available():
                self._log("CUDA not available, using CPU.")
                device = "cpu"

            key = (cfg["model"], device)
            if self.model is None or self.model_key != key:
                self._log(f"Loading model '{cfg['model']}' on {device}…")
                self.log_queue.put(("status", "Loading model…"))
                self.model = whisper.load_model(cfg["model"], device=device)
                self.model_key = key
            else:
                self._log(f"Model '{cfg['model']}' is already loaded.")

            os.makedirs(cfg["out_dir"], exist_ok=True)
            total = len(cfg["files"])
            self._log(f"Found files: {total}. Starting…")

            writer_opts = {"max_line_width": None, "max_line_count": None, "highlight_words": False}

            for i, filename in enumerate(cfg["files"]):
                if self.stop_flag.is_set():
                    self._log("Stopped by user.")
                    break

                path = os.path.join(cfg["in_dir"], filename)
                self._log(f"[{i + 1}/{total}] {filename}")
                self.log_queue.put(("status", f"Processing {i + 1}/{total}: {filename}"))

                try:
                    result = self.model.transcribe(
                        path,
                        language=cfg["lang"],
                        task=cfg["task"],
                        fp16=(device == "cuda"),
                    )

                    for fmt in cfg["formats"]:
                        if fmt == "txt":
                            txt_path = os.path.join(cfg["out_dir"], filename + ".txt")
                            with open(txt_path, "w", encoding="utf-8") as f:
                                f.write(result["text"].strip())
                        else:
                            writer = get_writer(fmt, cfg["out_dir"])
                            writer(result, path, writer_opts)
                    self._log("   ✔ done")
                except Exception as e:
                    self._log(f"   ✖ Error in {filename}: {e}")

                self.log_queue.put(("progress", i + 1))

            self._log("------------------------------------------")
            self._log(f"Done! Results in: {cfg['out_dir']}")
            self.log_queue.put(("status", "Finished"))
        except Exception as e:
            self._log(f"Critical error: {e}")
            self.log_queue.put(("status", "Error"))
        finally:
            self.log_queue.put(("done", None))

if __name__ == "__main__":
    App().mainloop()
