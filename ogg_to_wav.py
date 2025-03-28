import os
import ffmpeg
import shutil

def check_ffmpeg():
    """Check if FFmpeg is installed and accessible."""
    if shutil.which('ffmpeg') is None:
        print("\nError: FFmpeg is not installed or not found in system PATH!")
        print("\nTo install FFmpeg on Windows:")
        print("1. Download FFmpeg from: https://ffmpeg.org/download.html")
        print("   - Go to the Windows section")
        print("   - Download the 'Windows builds from gyan.dev' or 'Windows builds by BtbN'")
        print("2. Extract the downloaded zip file")
        print("3. Add FFmpeg to your system PATH:")
        print("   - Open System Properties (Win + Pause/Break)")
        print("   - Click on 'Advanced system settings'")
        print("   - Click on 'Environment Variables'")
        print("   - Under 'System variables', find and select 'Path'")
        print("   - Click 'Edit'")
        print("   - Click 'New'")
        print("   - Add the path to the FFmpeg bin folder (e.g., 'C:\\ffmpeg\\bin')")
        print("   - Click 'OK' on all windows")
        print("4. Restart your terminal/command prompt")
        return False
    return True

def convert_ogg_to_wav(input_file, output_dir="audio_files"):
    """
    Convert an OGG file to WAV format and save it in the specified output directory.
    
    Args:
        input_file (str): Path to the input OGG file
        output_dir (str): Directory to save the converted WAV file
    """
    try:
        # Check if FFmpeg is installed
        if not check_ffmpeg():
            return
        
        # Debug prints for input parameters
        print("\nDebug Information:")
        print(f"Original input_file: {input_file}")
        print(f"Original output_dir: {output_dir}")
        
        # Convert paths to absolute paths
        input_file = os.path.abspath(input_file)
        output_dir = os.path.abspath(output_dir)
        
        print(f"Absolute input_file: {input_file}")
        print(f"Absolute output_dir: {output_dir}")
        
        # Check if input file exists
        print(f"Input file exists: {os.path.exists(input_file)}")
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            print(f"Creating output directory: {output_dir}")
            os.makedirs(output_dir)
        
        # Get the filename without extension
        filename = os.path.splitext(os.path.basename(input_file))[0]
        output_file = os.path.join(output_dir, f"{filename}.wav")
        print(f"Output file path: {output_file}")
        
        # Convert OGG to WAV using ffmpeg
        print(f"\nStarting FFmpeg conversion...")
        print(f"Input file: {input_file}")
        print(f"Output file: {output_file}")
        
        stream = ffmpeg.input(input_file)
        stream = ffmpeg.output(stream, output_file, acodec='pcm_s16le', ac=2, ar='44100')
        
        # Debug print the FFmpeg command
        print("\nFFmpeg command:")
        print(ffmpeg.compile(stream))
        
        ffmpeg.run(stream, capture_stdout=True, capture_stderr=True)
        
        print(f"\nConversion successful!")
        print(f"WAV file saved as: {output_file}")
        
    except ffmpeg.Error as e:
        print(f"\nFFmpeg Error:")
        print(f"stdout: {e.stdout.decode() if e.stdout else 'None'}")
        print(f"stderr: {e.stderr.decode() if e.stderr else 'None'}")
    except Exception as e:
        print(f"\nGeneral Error:")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        import traceback
        print("\nFull traceback:")
        traceback.print_exc()

def list_ogg_files():
    """List all OGG files in the current directory and subdirectories."""
    print("\nDebug: Starting file search...")
    ogg_files = []
    for root, dirs, files in os.walk("."):
        print(f"Searching in directory: {root}")
        for file in files:
            if file.lower().endswith('.ogg'):
                # Convert to absolute path
                full_path = os.path.abspath(os.path.join(root, file))
                print(f"Found OGG file: {full_path}")
                ogg_files.append(full_path)
    
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
                custom_path = input("Enter the path to your OGG file: ")
                abs_path = os.path.abspath(custom_path)
                print(f"Custom path resolved to: {abs_path}")
                return abs_path
            if 1 <= choice <= len(ogg_files):
                selected_file = ogg_files[choice - 1]
                print(f"Selected file: {selected_file}")
                return selected_file
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