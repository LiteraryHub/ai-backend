import re
import cv2 as cv
import numpy as np
import requests
import nltk
import os
import yaml
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

def count_tokens(english_text):
    """
    Count the number of tokens (words) in the given English text.

    Parameters:
    - english_text (str): The input English text.

    Returns:
    - int: The number of tokens (words) in the text.

    Example:
    english_text = "This is an example sentence."
    num_tokens = count_tokens(english_text)
    print(f"Number of tokens: {num_tokens}")
    """
    tokens = nltk.word_tokenize(english_text)
    return len(tokens)


def replace_arabic_with_english_letters(text):
    """
    Replace Arabic letters with their English equivalents in a given text.

    Parameters:
    - text (str): The input text containing Arabic characters.

    Returns:
    - str: The input text with Arabic characters replaced by their English equivalents.

    Example:
    arabic_text = "مرحبا بك في عالم البرمجة"
    english_equivalent = replace_arabic_with_english_letters(arabic_text)
    print(f"English Equivalent: {english_equivalent}")
    """
    # Dictionary mapping Arabic letters to their English equivalents.
    ARABIC_TO_ENGLISH = {
        'ا': 'a',
        'أ': 'a',
        'إ': 'a',
        'آ': 'a',
        'ب': 'b',
        'ت': 't',
        'ث': 'th',
        'ج': 'j',
        'ح': 'h',
        'خ': 'kh',
        'د': 'd',
        'ذ': 'th',
        'ر': 'r',
        'ز': 'z',
        'س': 's',
        'ش': 'sh',
        'ص': 's',
        'ض': 'd',
        'ط': 't',
        'ظ': 'z',
        'ع': 'aa',
        'غ': 'gh',
        'ف': 'f',
        'ق': 'q',
        'ك': 'k',
        'ل': 'l',
        'م': 'm',
        'ن': 'n',
        'ه': 'h',
        'ة': 'h',
        'و': 'w',
        'ي': 'y'
    }

    # Replace each Arabic letter with its English equivalent in the text.
    for arabic, english in ARABIC_TO_ENGLISH.items():
        text = text.replace(arabic, english)

    # Return the text with Arabic characters replaced by their English equivalents.
    return text


def save_image(img, folder, title):
    cv.imwrite(f'./{folder}/{title}.png', img)


def projection(gray_img, axis: str = 'horizontal'):
    """ Compute the horizontal or the vertical projection of a gray image """

    if axis == 'horizontal':
        projection_bins = np.sum(gray_img, 1).astype('int32')
    elif axis == 'vertical':
        projection_bins = np.sum(gray_img, 0).astype('int32')

    return projection_bins


def split_text_into_chunks(text, chunk_size=512):
    """
    Split the input text into chunks of a specified size number of tokens.
    
    Args:
        text (str): The input text to be split into chunks.
        chunk_size (int): The desired number of tokens in each chunk.

    Returns:
        list: A list of text chunks, each containing the specified number of tokens.
    """
    words = text.split()  # Split text into words based on whitespace
    chunks = []
    current_chunk = []

    for word in words:
        current_chunk.append(word)
        if len(current_chunk) == chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = []

    if current_chunk:  # Add any remaining words as a final chunk
        chunks.append(" ".join(current_chunk))

    return chunks


def split_text(text, max_length=512):
    """
    Splits the text into manageable chunks, attempting to avoid cutting words.
    """
    words = text.split()
    chunks = []
    current_chunk = []
    for word in words:
        if len(' '.join(current_chunk + [word])) > max_length:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]
        else:
            current_chunk.append(word)
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    return chunks


def preprocess_arabic_text(text):
    """ 
    Preprocess Arabic text by removing diacritics and punctuation.
    
    Args:
        text (str): The input Arabic text.
    
    Returns:
        str: The preprocessed Arabic text.
    """
    text = text.replace("\n", " ").replace("  ", " ")

    # Remove punctuation
    punctuations = '''`÷×؛<>_()*&^%][ـ،/:"؟.,'{}~¦+|!”…“–ـ»«'''
    translator = str.maketrans('', '', punctuations)
    text = text.translate(translator)
    
    # I want to remove english characters or numbers or words
    text = re.sub(r'[a-zA-Z0-9]', '', text)
    
    return text


class DictConfig(object):
    """Creates a Config object from a dict 
       such that object attributes correspond to dict keys.    
    """

    def __init__(self, config_dict):
        self.__dict__.update(config_dict)

    def __str__(self):
        return '\n'.join(f"{key}: {val}" for key, val in self.__dict__.items())

    def __repr__(self):
        return self.__str__()


def get_custom_config(fname):
    with open(fname, 'r') as stream:
        config_dict = yaml.load(stream, Loader)
    config = DictConfig(config_dict)
    return config


def get_basic_config():
    cwd = os.getcwd()
    config_path = os.path.join(cwd, 'src', 'nlp', 'tts', 'configs', 'basic.yaml')
    return get_custom_config(config_path)
