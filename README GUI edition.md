# 🚀 WhisperBatcher Portable (GUI Edition)

A lightweight, portable tool with a graphical interface for bulk transcribing thousands of short audio/video files using OpenAI's Whisper. Optimized for both multi-core CPUs and CUDA GPUs. Designed for game modders, localizers, and developers.

## 🌟 What's New in the GUI Update?
* **User-Friendly Interface:** No more command line! Select folders, models, and settings directly in a clean visual interface.
* **Multiple Output Formats:** Export transcripts as raw text (`.txt`) or subtitles (`.srt`, `.vtt`).
* **Model & Device Selection:** Easily switch between Whisper models (tiny, base, small, medium, large, turbo) and processing units (Auto, CPU, GPU/CUDA).
* **Language & Task Control:** Auto-detect language or force a specific one. Choose between original language transcription or translation to English.
* **Portable FFmpeg:** No need to install FFmpeg system-wide — it's already in the folder.

---

## 🛠️ Prerequisites

1.  **Python 3.x:** Download from [python.org](https://www.python.org/downloads/).
    * **IMPORTANT:** Check the box **"Add Python to PATH"** during installation.
2.  **Whisper Library:** Open CMD and run:
    ```bash
    pip install openai-whisper
    ```
    *(If you want to use your GPU for faster transcription, make sure to install PyTorch with CUDA support).*

---

## 🚀 How to Use

1.  **Launch:** Double-click the `run.bat` (or `start.bat`) file to open the program.
2.  **Select Folders:** Choose your input folder (where your audio/video files are) and your output folder.
3.  **Configure:** Choose your preferred Whisper model, audio language, and output formats.
4.  **Run:** Click "**▶ Start**" and watch the progress bar and log. Results will be saved automatically.

---

## 📦 Project Structure
* `gui.py` — The core Python application with the graphical interface.
* `start.bat` / `run.bat` — Quick launch scripts.
* `ffmpeg.exe` — Portable audio processing engine (included).
* `output/` — Default folder for results.
* `README.md` — This guide.

---

## 🤝 Credits
* **Developer:** Vitaliy Levkovych
* **AI Assistant:** Gemini (Google AI) — UI development, script optimization & troubleshooting.

---

## ⚠️ Troubleshooting
* **The `.bat` file opens and immediately closes:** Ensure your `start.bat` is saved in standard **UTF-8** encoding (without BOM) and try changing `python gui.py` to `py gui.py` inside the script.
* **"FFmpeg not found":** Ensure `ffmpeg.exe` is in the same folder as `gui.py`.
* **"Python not recognized":** Reinstall Python and make sure to check "Add to PATH".
* **Slow Speed:** If you don't have a powerful graphics card and are relying on your CPU, choose `tiny` or `base` models.
