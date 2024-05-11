import os
import torch
from concurrent.futures import ThreadPoolExecutor
from src.nlp.tts.models.fastpitch import FastPitch2Wave
from src.utils.utils import preprocess_arabic_text
from pydub import AudioSegment
import soundfile as sf
from pydub import AudioSegment


def split_text(text):
    num_of_words = 30
    text = preprocess_arabic_text(text)
    words = text.split()
    chunks = []

    current_chunk = []
    for word in words:
        if len(current_chunk) >= num_of_words:  # Check if the current chunk already has 15 words
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]  # Start a new chunk with the current word
        else:
            current_chunk.append(word)  # Add the word to the current chunk

    # Add the last chunk if it contains any words
    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks
        
def text_to_speech(text_chunk, book_name, index):
    use_cpu = False
    device = torch.device('cuda' if torch.cuda.is_available() and not use_cpu else 'cpu')
    cwd = os.getcwd()
    
    model_path = os.path.join(cwd, 'src', 'nlp', 'tts', 'fastpitch_ar_adv.pth')
    vocoder_path = os.path.join(cwd, 'src', 'nlp', 'tts', 'pretrained', 'hifigan-asc-v1', 'hifigan-asc.pth')
    vocoder_config_path = os.path.join(cwd, 'src', 'nlp', 'tts', 'pretrained', 'hifigan-asc-v1', 'config.json')
    
    model = FastPitch2Wave(model_sd_path=model_path, vocoder_sd=vocoder_path, vocoder_config=vocoder_config_path)
    model = model.to(device)
    model.eval()

    
    wave = model.tts(text_chunk)
    wave = wave.cpu().numpy()
    
    
    if os.path.exists(os.path.join(cwd, 'src', 'nlp', 'tts', 'output', book_name)) is False:
        os.makedirs(os.path.join(cwd, 'src', 'nlp', 'tts', 'output', book_name))
        
    filename = os.path.join(cwd, 'src', 'nlp', 'tts', 'output', book_name, f"chunk_{index}.wav")
    
    sf.write(filename, wave, 22050)
    return filename

def concatenate_audios(audio_files):
    """
    Concatenates a list of audio files into a single audio file.

    Args:
        audio_files (list): A list of file paths to the audio files.

    Returns:
        AudioSegment: The combined audio segment.

    Raises:
        FileNotFoundError: If any of the audio files are not found.
    """
    combined = AudioSegment.empty()
    
    if len(audio_files) > 1:
        audio_files = sorted(audio_files, key=lambda x: int(x.split('_')[-1].split('.')[0]))
        
    for file in audio_files:
        audio = AudioSegment.from_file(file)
        combined += audio
    
    return combined
    
    
def generate_audio_book(book_content, book_name):
    """
    Generate an audio book from the given book content.

    Args:
        book_content (str): The content of the book.
        book_name (str): The name of the book.

    Returns:
        bytes: The audio data of the generated audio book.
    """
    # Assume chunks are split and text_to_speech is defined somewhere to handle text to speech conversion.
    # Assuming split_text function splits text into manageable chunks.
    chunks = split_text(book_content)

    args = [(chunk, book_name, i) for i, chunk in enumerate(chunks)]

    audio_files = []
    with ThreadPoolExecutor() as executor:
        # Assuming text_to_speech returns file paths.
        results = executor.map(text_to_speech, *zip(*args))
        audio_files = list(results)

    # Get the concatenated audio data
    combined_audio = concatenate_audios(audio_files)

    # Cleanup: remove temporary audio files
    for file in audio_files:
        os.remove(file)

    # Instead of returning a path, return the audio data directly
    return combined_audio