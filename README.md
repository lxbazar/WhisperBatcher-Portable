# 🚀 WhisperBatcher Portable

A lightweight, portable tool for bulk transcribing thousands of short audio files using OpenAI's Whisper. Optimized for multi-core CPUs (even older 4-core systems) and designed for game modders, localizers, and developers.

## 🌟 Why this tool?
* **One-Click Setup:** No need to install FFmpeg system-wide — it's already in the folder.
* **Massive Processing:** Handled 3,000+ files in one go without crashing.
* **Portable:** Just copy the folder and run.
* **Optimized for CPU:** Uses `tiny` or `base` models to ensure speed on standard PCs without high-end GPUs.

---

## 🛠️ Prerequisites

1.  **Python 3.x:** Download from [python.org](https://www.python.org/downloads/).
    * **IMPORTANT:** Check the box **"Add Python to PATH"** during installation.
2.  **Whisper Library:** Open CMD and run:
    ```bash
    pip install openai-whisper
    ```

---

## 🚀 How to Use

1.  **Prepare:** Place your `.wav` files into the main folder (next to `go.py`).
2.  **Open Console:** Click on the folder address bar, type `cmd`, and press `Enter`.
3.  **Run:** Type the following command:
    ```bash
    python go.py
    ```
4.  **Result:** All transcribed text will appear in the `output` folder as individual `.txt` files.

---

## 📦 Project Structure
* `go.py` — The core Python logic (loads model once, processes everything).
* `ffmpeg.exe` — Portable audio processing engine (included).
* `output/` — Your results will be saved here.
* `README.md` — This guide.

---

## 🤝 Credits
* **Developer:** Vitaliy Levkovych
* **AI Assistant:** Gemini (Google AI) — Script optimization & troubleshooting.

---

## ⚠️ Troubleshooting
* **"FFmpeg not found":** Ensure `ffmpeg.exe` is in the same folder as `go.py`.
* **"Python not recognized":** Reinstall Python and make sure to check "Add to PATH".
* **Slow Speed:** Transcription is CPU-intensive. Close background apps (like Chrome or games) for better performance.