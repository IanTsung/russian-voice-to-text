import speech_recognition as sr
import os
import wave
import contextlib
import time
import shutil
from pydub import AudioSegment
from pydub.silence import split_on_silence
from googletrans import Translator

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

def translate_text(text, target_lang='en'):
    """Translate text to the target language using Google Translate."""
    try:
        translator = Translator()
        translation = translator.translate(text, src='ru', dest=target_lang)
        return translation.text
    except Exception as e:
        print(f"Translation error: {e}")
        return None

def split_audio_file(file_path, chunk_length_ms=120000, silence_thresh=-40):
    """Split audio file into chunks based on silence."""
    try:
        print("Splitting audio file into chunks...")
        audio = AudioSegment.from_file(file_path)
        
        # Create temp directory in current working directory
        temp_dir = os.path.join(os.getcwd(), "temp_chunks")
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)  # Clean up any existing temp directory
        os.makedirs(temp_dir)
        print(f"Created temporary directory: {temp_dir}")
        
        # Split on silence with longer minimum silence length
        chunks = split_on_silence(
            audio,
            min_silence_len=1000,  # Increased from 500 to 1000ms
            silence_thresh=silence_thresh,
            keep_silence=200  # Increased from 100 to 200ms
        )
        
        # If no silence found or too many chunks, split into fixed length chunks
        if not chunks or len(chunks) > 10:  # Limit to 10 chunks max
            print("Using fixed-length chunks for better quality...")
            chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]
        
        # Save chunks
        chunk_files = []
        for i, chunk in enumerate(chunks):
            chunk_file = os.path.join(temp_dir, f"chunk_{i}.wav")
            chunk.export(chunk_file, format="wav")
            chunk_files.append(chunk_file)
            print(f"Created chunk {i+1}/{len(chunks)} ({len(chunk)/1000:.1f}s)")
        
        return chunk_files, temp_dir
    except Exception as e:
        print(f"Error splitting audio file: {e}")
        return None, None

def process_audio_chunk(chunk_file, recognizer, max_retries=3):
    """Process a single audio chunk."""
    try:
        with sr.AudioFile(chunk_file) as source:
            audio = recognizer.record(source)
        
        for attempt in range(max_retries):
            try:
                print(f"Processing chunk (attempt {attempt + 1}/{max_retries})...")
                text = recognizer.recognize_google(audio, language='ru-RU')
                return text
            except sr.UnknownValueError:
                print("Could not understand audio in this chunk.")
                return None
            except sr.RequestError as e:
                print(f"Error with the speech recognition service: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2)
                else:
                    return None
    except Exception as e:
        print(f"Error processing chunk: {e}")
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

def convert_audio_to_text(audio_file_path=None, translate=False):
    # Initialize recognizer
    recognizer = sr.Recognizer()
    temp_dir = None
    
    try:
        if audio_file_path:
            # Check file size
            file_size_mb = os.path.getsize(audio_file_path) / (1024 * 1024)
            if file_size_mb > 10:  # Google's limit is around 10MB
                print(f"File size ({file_size_mb:.1f} MB) is large. Splitting into chunks...")
                chunk_files, temp_dir = split_audio_file(audio_file_path)
                if not chunk_files:
                    print("Failed to split audio file.")
                    return
                
                print(f"\nProcessing {len(chunk_files)} chunks...")
                full_text = []
                for i, chunk_file in enumerate(chunk_files, 1):
                    print(f"\nProcessing chunk {i}/{len(chunk_files)}")
                    text = process_audio_chunk(chunk_file, recognizer)
                    if text:
                        full_text.append(text)
                        print(f"Successfully transcribed chunk {i}")
                    else:
                        print(f"Failed to transcribe chunk {i}")
                
                if full_text:
                    print("\nFull Transcription:")
                    final_text = "\n".join(full_text)
                    print(final_text)
                    
                    if translate:
                        print("\nTranslating to English...")
                        translation = translate_text(final_text)
                        if translation:
                            print("\nEnglish Translation:")
                            print(translation)
                else:
                    print("No text could be transcribed from any chunks.")
                return
            
            # For smaller files, process directly
            with sr.AudioFile(audio_file_path) as source:
                print("Reading audio file...")
                audio = recognizer.record(source)
            
            print("Processing...")
            text = recognizer.recognize_google(audio, language='ru-RU')
            print("\nTranscription:")
            print(text)
            
            if translate:
                print("\nTranslating to English...")
                translation = translate_text(text)
                if translation:
                    print("\nEnglish Translation:")
                    print(translation)
            
        else:
            # Use microphone input
            with sr.Microphone() as source:
                print("Listening... Speak in Russian")
                recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = recognizer.listen(source)
            
            print("Processing...")
            text = recognizer.recognize_google(audio, language='ru-RU')
            print("\nTranscription:")
            print(text)
            
            if translate:
                print("\nTranslating to English...")
                translation = translate_text(text)
                if translation:
                    print("\nEnglish Translation:")
                    print(translation)
            
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print(f"Error with the speech recognition service: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Clean up temp directory
        if temp_dir and os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir)
                print(f"\nCleaned up temporary directory: {temp_dir}")
            except Exception as e:
                print(f"Warning: Could not clean up temporary directory: {e}")

if __name__ == "__main__":
    print("Russian Audio to Text Converter")
    print("1. Use microphone input")
    print("2. Convert from audio file")
    
    choice = input("\nEnter your choice (1 or 2): ")
    
    if choice in ["1", "2"]:
        translate = input("Do you want to translate the text to English? (y/n): ").lower() == 'y'
        if choice == "1":
            convert_audio_to_text(translate=translate)
        else:
            file_path = list_audio_files()
            if file_path and os.path.exists(file_path):
                convert_audio_to_text(file_path, translate=translate)
            else:
                print("File not found!")
    else:
        print("Invalid choice!") 