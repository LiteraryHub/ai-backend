import os
import torch
from concurrent.futures import ThreadPoolExecutor
from src.nlp.tts.models.fastpitch import FastPitch2Wave
from src.utils.utils import preprocess_arabic_text
from pydub import AudioSegment
import soundfile as sf


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


def concatenate_audios(audio_files, output_path):
    combined = AudioSegment.empty()
    
    if len(audio_files) > 1:
        audio_files = sorted(audio_files, key=lambda x: int(x.split('_')[-1].split('.')[0]))
        
    for file in audio_files:
        audio = AudioSegment.from_file(file)
        combined += audio
    combined.export(output_path, format="wav")
    
    
def generate_audio_book(book_content, book_name):
    output_path = os.path.join(os.getcwd(), 'src', 'nlp', 'tts', 'output', book_name)
    
    # Process text to speech
    chunks = split_text(book_content)
    
    args = [(chunk, book_name, i) for i, chunk in enumerate(chunks)]

    audio_files = []
    with ThreadPoolExecutor() as executor:
        results = executor.map(text_to_speech, *zip(*args))
        audio_files = list(results)

    # Concatenate audio files and cleanup
    output_path = os.path.join(output_path, f"{book_name}.wav")
    concatenate_audios(audio_files, output_path)
    for file in audio_files:
        os.remove(file)

    return output_path





if __name__ == '__main__':
    # Example call to generate an audiobook
    content = "أَلسَّلامُ عَلَيكُم يا صَديقي, هذا مثال لنص عربي يتم تحويله إلى كتاب صوتي"
    book_name = "MyAudiobook"
    audio_book_path = generate_audio_book(content, book_name)
    print("Audio book created at:", audio_book_path)