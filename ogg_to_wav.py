import os
from pydub import AudioSegment

def convert_ogg_to_wav(input_file, output_dir="audio_files"):
    """
    Convert an OGG file to WAV format and save it in the specified output directory.
    
    Args:
        input_file (str): Path to the input OGG file
        output_dir (str): Directory to save the converted WAV file
    """
    try:
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Get the filename without extension
        filename = os.path.splitext(os.path.basename(input_file))[0]
        output_file = os.path.join(output_dir, f"{filename}.wav")
        
        # Load the OGG file
        print(f"Loading {input_file}...")
        audio = AudioSegment.from_ogg(input_file)
        
        # Export as WAV
        print(f"Converting to WAV...")
        audio.export(output_file, format="wav")
        
        print(f"\nConversion successful!")
        print(f"WAV file saved as: {output_file}")
        
    except Exception as e:
        print(f"Error during conversion: {e}")

def list_ogg_files():
    """List all OGG files in the current directory and subdirectories."""
    ogg_files = []
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.lower().endswith('.ogg'):
                ogg_files.append(os.path.join(root, file))
    
    if not ogg_files:
        print("No OGG files found in the current directory or subdirectories.")
        return None
    
    print("\nAvailable OGG files:")
    for i, file in enumerate(ogg_files, 1):
        print(f"{i}. {file}")
    
    while True:
        try:
            choice = int(input("\nSelect a file number (or 0 to enter custom path): "))
            if choice == 0:
                return input("Enter the path to your OGG file: ")
            if 1 <= choice <= len(ogg_files):
                return ogg_files[choice - 1]
            print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

if __name__ == "__main__":
    print("OGG to WAV Converter")
    print("This tool converts OGG audio files to WAV format.")
    print("Converted files will be saved in the 'audio_files' directory.")
    
    input_file = list_ogg_files()
    if input_file and os.path.exists(input_file):
        convert_ogg_to_wav(input_file)
    else:
        print("File not found!") 