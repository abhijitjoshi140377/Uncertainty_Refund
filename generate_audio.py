"""
Generate audio file from hackathon transcript using text-to-speech
"""
import os

def create_audio():
    # Read the transcript
    with open('HACKATHON_AUDIO_TRANSCRIPT.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract only the spoken text (remove markdown headers and timestamps)
    lines = content.split('\n')
    spoken_text = []
    
    for line in lines:
        line = line.strip()
        # Skip empty lines, markdown headers, and timestamp lines
        if not line or line.startswith('#') or line.startswith('**') or line.startswith('['):
            continue
        # Skip separator lines
        if line == '---':
            continue
        spoken_text.append(line)
    
    # Join all text
    full_text = ' '.join(spoken_text)
    
    # Try using pyttsx3 (offline TTS)
    try:
        import pyttsx3
        
        print('[INFO] Using pyttsx3 for text-to-speech...')
        engine = pyttsx3.init()
        
        # Set properties
        engine.setProperty('rate', 130)  # Speed (words per minute)
        engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
        
        # Get available voices
        voices = engine.getProperty('voices')
        # Try to use a better voice if available
        for voice in voices:
            if 'david' in voice.name.lower() or 'zira' in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
        
        # Save to file
        output_file = 'HACKATHON_PRESENTATION_AUDIO.mp3'
        engine.save_to_file(full_text, output_file)
        engine.runAndWait()
        
        print(f'[SUCCESS] Audio file created: {output_file}')
        print(f'[INFO] Duration: Approximately 5 minutes')
        print(f'[INFO] Location: c:/Users/AbhijitJoshi/Uncertainty_Refund/{output_file}')
        return True
        
    except ImportError:
        print('[ERROR] pyttsx3 not installed. Installing...')
        os.system('pip install pyttsx3')
        print('[INFO] Please run the script again after installation.')
        return False
    except Exception as e:
        print(f'[ERROR] Failed to generate audio: {str(e)}')
        print('[INFO] Alternative: Use online TTS services like:')
        print('  - Google Text-to-Speech')
        print('  - Amazon Polly')
        print('  - Microsoft Azure Speech')
        print('[INFO] Or use the transcript file for manual recording')
        return False

if __name__ == '__main__':
    create_audio()

# Made with Bob
