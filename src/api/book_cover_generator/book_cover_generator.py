from diffusers import AutoPipelineForText2Image
import torch
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from fastapi import APIRouter
from fastapi.responses import FileResponse
import cv2
import arabic_reshaper
from bidi.algorithm import get_display
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import nltk
from src.nlp.translation.arabic_to_english import translate_arabic_to_english
from src.nlp.summarization.english_text_summarization import generate_summary
from src.utils.utils import *

nltk.download('punkt')
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

router = APIRouter()

def gen_img(prompt, num_inference_steps=5, guidance_scale=1.0):
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
    # Convert PIL image to NumPy array
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


def add_arabic_text(arabic_title, arabic_authors, image, x_percentage, y_percentage, width_percentage, height_percentage):
    """
    Adds Arabic text for the title and authors on a provided image.
    
    Args:
    arabic_title (str): The book title in Arabic.
    arabic_authors (list of str): The authors of the book in Arabic.
    image (PIL.Image): The image on which to overlay the text.
    x_percentage, y_percentage, width_percentage, height_percentage (float): The percentages defining the area to overlay text.

    Returns:
    PIL.Image: The image with added text.
    """
    cwd = os.getcwd()
    font_path = os.path.join(cwd, 'src', 'font.ttf')

    # Adjust the rectangle height based on title length
    words_in_title = arabic_title.split()
    if len(words_in_title) > 3:
        # Increase height by 5% for each word above 3
        height_percentage += 0.05 * (len(words_in_title) - 3)

    # Convert PIL image to NumPy array for manipulation
    numpy_image = np.array(image)
    image_temp = cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)
    height, width, _ = image_temp.shape

    # Recalculate rectangle dimensions with potential new height
    x = int(width * x_percentage)
    y = int(height * y_percentage)
    w = int(width * width_percentage)
    h = int(height * height_percentage)

    arabic_title_font = ImageFont.truetype(font_path, size=55)
    arabic_title = arabic_reshaper.reshape(arabic_title)  # Reshape for correct RTL rendering

    # Place title in the upper middle of the rectangle
    title_text_size = cv2.getTextSize(arabic_title, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
    title_text_x = x - title_text_size[0] // 2
    title_text_y = y - h // 4  # Adjust for title to be in upper middle

    image = Image.fromarray(cv2.cvtColor(image_temp, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(image)
    draw.text((title_text_x, title_text_y), get_display(arabic_title), font=arabic_title_font, fill='black')

    # Draw authors under the title
    authors_arabic_title_font = ImageFont.truetype(font_path, size=30)
    authors_text_y = title_text_y + 70  # Start authors 70 pixels below the title
    for author in arabic_authors:
        reshaped_author = arabic_reshaper.reshape(author)
        author_text_size = cv2.getTextSize(reshaped_author, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
        author_text_x = x - author_text_size[0] // 2 + 30
        draw.text((author_text_x, authors_text_y), get_display(reshaped_author), font=authors_arabic_title_font, fill='black')
        authors_text_y += 40  # Space subsequent authors 40 pixels apart

    return image


def generate_book_cover(arabic_title, arabic_authors, book_summary, num_inference_steps, guidance_scale):
    # Translate book summary to English to use in image generation
    english_book_summary = translate_arabic_to_english(book_summary)

    # Optionally, summarize the book summary if it is too long
    if count_tokens(english_book_summary) > 77:
        english_book_summary = generate_summary(english_book_summary)

    # Generate an image based on the English book summary
    gen_image = gen_img(prompt=english_book_summary, num_inference_steps=num_inference_steps, guidance_scale=guidance_scale)
    resized_img = resize_gen_img(gen_image)

    # Apply a blur effect to a portion of the image to overlay text
    base_cover = blur_rectangle(image=resized_img, x_percentage=0.5, y_percentage=0.8, width_percentage=0.9, height_percentage=0.3)

    # Add Arabic text to the image
    result_cover = add_arabic_text(arabic_title, arabic_authors, base_cover, x_percentage=0.5, y_percentage=0.8, width_percentage=0.9, height_percentage=0.3)

    return result_cover


@router.post('/generate')
async def get_book_cover(payload: dict):
    # Get data from the request body
    data = payload

    # Extract parameters from the JSON data
    book_title = data.get('book_title')
    book_summary = data.get('book_summary')
    arabic_authors = data.get('arabic_authors', [])
    num_inference_steps = data.get('num_inference_steps', 5)
    guidance_scale = data.get('guidance_scale', 0.6)

    # Generate the book cover
    book_cover = generate_book_cover(
        arabic_title=book_title, arabic_authors=arabic_authors,
        book_summary=book_summary, num_inference_steps=num_inference_steps,
        guidance_scale=guidance_scale
    )

    # Get the image from the book cover
    image = book_cover._image

    img_bytesio = BytesIO()
    image.save(img_bytesio, format='PNG')
    img_bytesio.seek(0)
    return FileResponse(img_bytesio, media_type='image/png', filename='book_cover.png')
