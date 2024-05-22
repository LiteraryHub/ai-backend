from diffusers import AutoPipelineForText2Image
import torch
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from fastapi import APIRouter
from fastapi.responses import FileResponse, StreamingResponse
import cv2
import arabic_reshaper
from bidi.algorithm import get_display
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import nltk
from src.nlp.translation.arabic_to_english import translate_arabic_to_english
from src.nlp.summarization.english_text_summarization import generate_summary
from src.utils.utils import *
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

nltk.download('punkt')
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

router = APIRouter()


def count_tokens(english_text):
    tokens = nltk.word_tokenize(english_text)
    return len(tokens)


def text_summarizer(text):
    summarizer = pipeline("summarization", model="Falconsai/text_summarization")
    return summarizer(text, max_length=77, min_length=30, do_sample=False)[0]["summary_text"]


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


def replace_arabic_with_english_letters(text):
    for arabic, english in ARABIC_TO_ENGLISH.items():
        text = text.replace(arabic, english)
    return text





def arabic2english(text):
    tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-ar-en")
    model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-ar-en")
    input_ids = tokenizer(text, return_tensors="pt").input_ids
    outputs = model.generate(input_ids=input_ids, num_beams=5, num_return_sequences=3)
    return tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]

def gen_img(prompt, num_inference_steps=10, guidance_scale=3.0):
    """
    Generates an image from a text prompt using a pretrained model.

    Args:
    prompt (str): The text prompt to generate the image.
    num_inference_steps (int): The number of steps for the generation process.
    guidance_scale (float): The scale of guidance for the generation.

    Returns:
    PIL.Image: The generated image.
    """

    pipeline = AutoPipelineForText2Image.from_pretrained("stabilityai/sdxl-turbo", torch_dtype=torch.float32, variant="fp16")
    pipeline.to(device)

    return pipeline(prompt=prompt, num_inference_steps=num_inference_steps, guidance_scale=guidance_scale).images[0]


def resize_gen_img(img):
    """
    Resizes a PIL image to a specific dimension suitable for book covers.

    Args:
    img (PIL.Image): The image to resize.

    Returns:
    PIL.Image: The resized image.
    """
    # Convert PIL image to NumPy array
    numpy_image = np.array(img)

    # Convert RGB to BGR (OpenCV uses BGR color format)
    img = cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)

    # Resize the image to the desired dimensions
    resized_img = cv2.resize(img, (6*96, 9*96))

    # Convert OpenCV image (BGR format) to RGB
    resized_img_rgb = cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB)

    # Convert numpy array to PIL Image
    pil_image = Image.fromarray(resized_img_rgb)

    return pil_image


def blur_rectangle(image, x_percentage, y_percentage, width_percentage, height_percentage):
    """
    Applies a blur effect to a specified rectangle area in an image.

    Args:
    image (PIL.Image): The original image.
    x_percentage (float): The x-coordinate as a percentage of the image width.
    y_percentage (float): The y-coordinate as a percentage of the image height.
    width_percentage (float): The width of the rectangle as a percentage of the image width.
    height_percentage (float): The height of the rectangle as a percentage of the image height.

    Returns:
    PIL.Image: The image with a blurred rectangle area.
    """
    numpy_image = np.array(image)

    # Convert RGB to BGR (OpenCV uses BGR color format)
    image = cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)

    # Get image dimensions
    height, width, _ = image.shape

    # Calculate rectangle dimensions based on percentages
    x = int(width * x_percentage)
    y = int(height * y_percentage)
    w = int(width * width_percentage)
    h = int(height * height_percentage)

    # Calculate rectangle coordinates
    x1 = x - w // 2
    y1 = y - h // 2
    x2 = x + w // 2
    y2 = y + h // 2

    # Create a copy of the image
    blurred_image = image.copy()

    # Blur the specified rectangle
    blurred_image[y1:y2, x1:x2] = cv2.GaussianBlur(
        blurred_image[y1:y2, x1:x2], (25, 25), 0)

    # Convert OpenCV image (BGR format) to RGB
    blurred_img_rgb = cv2.cvtColor(blurred_image, cv2.COLOR_BGR2RGB)

    # Convert numpy array to PIL Image
    pil_image = Image.fromarray(blurred_img_rgb)
    return pil_image


def add_en_text(english_title, arabic_title, arabic_authors, english_authors, image, x_percentage, y_percentage, width_percentage, height_percentage):
    image_temp = image
    # Convert PIL image to NumPy array
    numpy_image = np.array(image_temp)

    # Convert RGB to BGR (OpenCV uses BGR color format)
    image_temp = cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)

    # Get image dimensions
    height, width, _ = image_temp.shape

    # Calculate rectangle dimensions based on percentages
    x = int(width * x_percentage)
    y = int(height * y_percentage)
    w = int(width * width_percentage)
    h = int(height * height_percentage)

    title_font_resize = cv2.FONT_HERSHEY_SIMPLEX
    arabic_title_font = ImageFont.truetype(
        './font.ttf', size=55)
    arabic_title = arabic_reshaper.reshape(arabic_title)

    # Add text to the center of the blurred rectangle
    title_text_size = cv2.getTextSize(
        english_title, title_font_resize, 1, 2)[0]
    title_text_x = x - title_text_size[0] // 2
    title_text_y = (y + title_text_size[1] // 2) - 150

    image = ImageDraw.Draw(image)
    image.text((title_text_x, title_text_y), get_display(
        arabic_title), font=arabic_title_font, fill='black')

    authors_font = cv2.FONT_ITALIC

    counter = 50
    authors_arabic_title_font = ImageFont.truetype(
        './font.ttf', size=30)
    for i in range(len(english_authors)):
        authors_text_size = cv2.getTextSize(
            english_authors[i], authors_font, 1, 2)[0]
        authors_text_x = x - authors_text_size[0] // 2 + 30
        authors_text_y = (y + authors_text_size[1] // 2) - counter
        image.text((authors_text_x, authors_text_y), get_display(arabic_reshaper.reshape(
            arabic_authors[i])), font=authors_arabic_title_font, fill='black')
        counter = counter - 30

    # result_img = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)

    # # # Convert numpy array to PIL Image
    # # pil_image = Image.fromarray(result_img)
    # # return pil_image
    return image


def generate_book_cover(arabic_title, arabic_authors, book_summary, num_inference_steps, guidance_scale):
    english_book_summary = arabic2english(book_summary)

    if count_tokens(english_book_summary) > 77:
        english_book_summary = text_summarizer(english_book_summary)

    english_title = arabic2english(arabic_title)
    gen_image = gen_img(prompt=english_book_summary, num_inference_steps=num_inference_steps, guidance_scale=guidance_scale)
    resized_img = resize_gen_img(gen_image)
    base_cover = blur_rectangle(image=resized_img, x_percentage=0.5, y_percentage=0.8, width_percentage=0.9, height_percentage=0.3)

    english_authors = []
    for i in range(len(arabic_authors)):
        english_authors.append(replace_arabic_with_english_letters(arabic_authors[i]))

    result_cover = add_en_text(english_title, arabic_title, arabic_authors, english_authors,
                               base_cover, x_percentage=0.5, y_percentage=0.8, width_percentage=0.9, height_percentage=0.3)

    return result_cover


@router.post('/generate')
async def get_book_cover(payload: dict):
    # Get data from the request body
    data = payload

    # Extract parameters from the JSON data
    book_title = data.get('book_title')
    book_summary = data.get('book_summary')
    arabic_authors = data.get('arabic_authors', [])
    num_inference_steps = data.get('num_inference_steps', 10)
    guidance_scale = data.get('guidance_scale', 3)

    # Generate the book cover
    book_cover = generate_book_cover(
        arabic_title=book_title, arabic_authors=arabic_authors,
        book_summary=book_summary, num_inference_steps=num_inference_steps,
        guidance_scale=guidance_scale
    )

    # Convert the PIL Image to bytes
    img_bytesio = BytesIO()
    book_cover.save(img_bytesio, format='PNG')
    img_bytesio.seek(0)

    return StreamingResponse(img_bytesio, media_type='image/png', headers={'Content-Disposition': 'attachment; filename=book_cover.png'})
