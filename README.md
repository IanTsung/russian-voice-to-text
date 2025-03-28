# Russian Audio to Text Converter

This tool converts Russian speech to text using Google's Speech Recognition API. It can work with both microphone input and audio files.

## Features

- Convert Russian speech from microphone to text
- Convert Russian audio files to text
- Convert OGG files to WAV format
- Simple command-line interface
- Uses Google's Speech Recognition API for accurate results
- Organized audio file management with dedicated directory

## Requirements

- Python 3.6 or higher
- PyAudio
- SpeechRecognition
- ffmpeg-python (for OGG to WAV conversion)

## Installation

1. Clone this repository or download the files
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Converting Russian Speech to Text

1. Place your audio files in the `audio_files` directory (supported formats: WAV, AIFF, AIFF-C, FLAC)
2. Run the script:
   ```
   python russian_audio_to_text.py
   ```

You'll be presented with two options:
1. Use microphone input - Speak in Russian when prompted
2. Convert from audio file - Select from available files in the `audio_files` directory or enter a custom path

### Converting OGG to WAV

If you have OGG files that need to be converted to WAV format:

1. Run the converter:
   ```
   python ogg_to_wav.py
   ```
2. Select your OGG file from the list or enter a custom path
3. The converted WAV file will be saved in the `audio_files` directory

## Supported Audio Formats

The tool supports the following audio formats:
- WAV
- AIFF
- AIFF-C
- FLAC
- OGG (can be converted to WAV)

## Notes

- For microphone input, make sure your system's microphone is properly configured
- For audio files, place them in the `audio_files` directory or provide the full path to the file
- An internet connection is required as the tool uses Google's Speech Recognition API
- OGG files need to be converted to WAV format before they can be processed by the speech recognition tool 