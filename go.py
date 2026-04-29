import whisper
import os
import sys

# WhisperBatcher by Vitaliy Levkovych & Gemini AI
def main():
    print("------------------------------------------")
    print("Welcome to WhisperBatcher Portable")
    print("------------------------------------------")
    
    # Using 'tiny' model for maximum speed on CPU
    print("Loading AI model (tiny)... Please wait.")
    try:
        model = whisper.load_model("tiny")
    except Exception as e:
        print(f"Error loading model: {e}")
        return

    # Setup output directory
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Scan for audio files
    files = [f for f in os.listdir(".") if f.endswith(".wav")]
    
    if not files:
        print("No .wav files found in the current folder!")
        return

    print(f"Found {len(files)} files. Starting transcription...")
    print("------------------------------------------")

    for i, filename in enumerate(files):
        try:
            print(f"[{i+1}/{len(files)}] Processing: {filename}")
            
            # Transcribe English audio
            # You can change language="en" to language=None for auto-detection
            result = model.transcribe(filename, language="en")
            
            # Save the result to a text file
            txt_filename = os.path.join(output_dir, filename + ".txt")
            with open(txt_filename, "w", encoding="utf-8") as f:
                f.write(result["text"].strip())
                
        except Exception as e:
            print(f"Failed to process {filename}: {e}")

    print("------------------------------------------")
    print(f"Done! All transcriptions are saved in the '{output_dir}' folder.")
    print("Thank you for using WhisperBatcher.")

if __name__ == "__main__":
    main()