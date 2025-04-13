import speech_recognition as sr
import os
import wave
import contextlib
import time
from pydub import AudioSegment

def get_audio_duration(file_path):
    """Get the duration of an audio file in seconds."""
    try:
        if file_path.lower().endswith('.wav'):
            with contextlib.closing(wave.open(file_path, 'r')) as f:
                frames = f.getnframes()
                rate = f.getframerate()
                duration = frames / float(rate)
                return duration
        else:
            # For non-WAV files, use pydub
            audio = AudioSegment.from_file(file_path)
            return len(audio) / 1000.0  # Convert milliseconds to seconds
    except Exception as e:
        print(f"Warning: Could not determine audio duration: {e}")
        return None

def list_audio_files():
    audio_dir = "audio_files"
    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir)
        print(f"Created directory: {audio_dir}")
        return None
    
    # Support more audio formats
    supported_formats = ('.wav', '.aiff', '.aiff-c', '.flac', '.mp3', '.m4a', '.ogg')
    files = [f for f in os.listdir(audio_dir) if f.lower().endswith(supported_formats)]
    
    if not files:
        print(f"No audio files found in {audio_dir} directory.")
        print(f"Supported formats: {', '.join(supported_formats)}")
        return None
    
    print("\nAvailable audio files:")
    for i, file in enumerate(files, 1):
        file_path = os.path.join(audio_dir, file)
        duration = get_audio_duration(file_path)
        size_mb = os.path.getsize(file_path) / (1024 * 1024)
        duration_str = f" ({duration:.1f}s)" if duration else ""
        print(f"{i}. {file}{duration_str} ({size_mb:.1f} MB)")
    
    while True:
        try:
            choice = int(input("\nSelect a file number (or 0 to enter custom path): "))
            if choice == 0:
                custom_path = input("Enter the path to your audio file: ")
                if not os.path.exists(custom_path):
                    print("File not found!")
                    continue
                return custom_path
            if 1 <= choice <= len(files):
                return os.path.join(audio_dir, files[choice - 1])
            print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

def convert_audio_to_text(audio_file_path=None, max_retries=3):
    # Initialize recognizer
    recognizer = sr.Recognizer()
    
    try:
        if audio_file_path:
            # Check file size
            file_size_mb = os.path.getsize(audio_file_path) / (1024 * 1024)
            if file_size_mb > 10:  # Google's limit is around 10MB
                print(f"Warning: File size ({file_size_mb:.1f} MB) is large. Consider using a shorter audio clip.")
            
            # Check duration
            duration = get_audio_duration(audio_file_path)
            if duration and duration > 60:  # Google's limit is around 1 minute
                print(f"Warning: Audio duration ({duration:.1f} seconds) is long. Consider using a shorter clip.")
            
            # If audio file is provided, read from file
            with sr.AudioFile(audio_file_path) as source:
                print("Reading audio file...")
                audio = recognizer.record(source)
        else:
            # Use microphone input
            with sr.Microphone() as source:
                print("Listening... Speak in Russian")
                # Adjust for ambient noise
                recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = recognizer.listen(source)
        
        # Try recognition with retries
        for attempt in range(max_retries):
            try:
                print(f"Processing (attempt {attempt + 1}/{max_retries})...")
                text = recognizer.recognize_google(audio, language='ru-RU')
                print("\nTranscription:")
                print(text)
                return text
            except sr.UnknownValueError:
                print("Could not understand audio. Please try again.")
                if attempt < max_retries - 1:
                    time.sleep(1)  # Wait before retrying
                else:
                    print("Maximum retries reached. Please check your audio quality.")
            except sr.RequestError as e:
                print(f"Error with the speech recognition service: {e}")
                if attempt < max_retries - 1:
                    print("Retrying...")
                    time.sleep(2)  # Wait longer before retrying
                else:
                    print("Maximum retries reached. Please check your internet connection.")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                if attempt < max_retries - 1:
                    print("Retrying...")
                    time.sleep(1)
                else:
                    print("Maximum retries reached. Please try again later.")
        
    except Exception as e:
        print(f"An error occurred while processing the audio: {e}")

if __name__ == "__main__":
    print("Russian Audio to Text Converter")
    print("1. Use microphone input")
    print("2. Convert from audio file")
    
    choice = input("\nEnter your choice (1 or 2): ")
    
    if choice == "1":
        convert_audio_to_text()
    elif choice == "2":
        file_path = list_audio_files()
        if file_path and os.path.exists(file_path):
            convert_audio_to_text(file_path)
        else:
            print("File not found!")
    else:
        print("Invalid choice!") 