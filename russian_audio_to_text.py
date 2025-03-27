import speech_recognition as sr
import os

def list_audio_files():
    audio_dir = "audio_files"
    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir)
    
    files = [f for f in os.listdir(audio_dir) if f.lower().endswith(('.wav', '.aiff', '.aiff-c', '.flac'))]
    if not files:
        print(f"No audio files found in {audio_dir} directory.")
        return None
    
    print("\nAvailable audio files:")
    for i, file in enumerate(files, 1):
        print(f"{i}. {file}")
    
    while True:
        try:
            choice = int(input("\nSelect a file number (or 0 to enter custom path): "))
            if choice == 0:
                return input("Enter the path to your audio file: ")
            if 1 <= choice <= len(files):
                return os.path.join(audio_dir, files[choice - 1])
            print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

def convert_audio_to_text(audio_file_path=None):
    # Initialize recognizer
    recognizer = sr.Recognizer()
    
    try:
        if audio_file_path:
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
        
        # Recognize speech using Google Speech Recognition
        print("Processing...")
        text = recognizer.recognize_google(audio, language='ru-RU')
        print("\nTranscription:")
        print(text)
        
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

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