import whisper
import os

def main():
    print("------------------------------------------")
    print("WhisperBatcher Multi-Format Edition")
    print("------------------------------------------")
    
    print("Loading AI model (tiny)...")
    model = whisper.load_model("tiny")

    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Додали підтримку різних розширень
    extensions = ('.wav', '.mp3', '.m4a', '.flac', '.ogg', '.mp4')
    files = [f for f in os.listdir(".") if f.lower().endswith(extensions)]
    
    if not files:
        print("No supported audio files found!")
        return

    print(f"Found {len(files)} files. Starting...")

    for i, filename in enumerate(files):
        try:
            print(f"[{i+1}/{len(files)}] Processing: {filename}")
            result = model.transcribe(filename, language="en")
            
            # Зберігаємо результат поруч із назвою (наприклад, track.mp3.txt)
            txt_filename = os.path.join(output_dir, filename + ".txt")
            with open(txt_filename, "w", encoding="utf-8") as f:
                f.write(result["text"].strip())
                
        except Exception as e:
            print(f"Error in {filename}: {e}")

    print("------------------------------------------")
    print("Done! Check the 'output' folder.")

if __name__ == "__main__":
    main()