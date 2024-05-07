# from diffusers import AutoPipelineForText2Image
# import torch
# from PIL import Image, ImageDraw, ImageFont
# import numpy as np
# from flask import Flask, request, send_file
# from utils.Utils import *
# import cv2
# import arabic_reshaper
# from bidi.algorithm import get_display
# from PIL import Image, ImageDraw, ImageFont
# from io import BytesIO

# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# app = Flask(__name__)
# ##nltk.download('punkt')

# pipe = AutoPipelineForText2Image.from_pretrained(
#     "C:\\Users\\Youssef Tarek\\LiteraryHub\\src\\books-cover-generator\\Sdxlturbo", torch_dtype=torch.float32, variant="fp16")
# pipe.to(device)


# def gen_img(prompt, num_inference_steps=5, guidance_scale=1.0):
#     return pipe(prompt=prompt, num_inference_steps=num_inference_steps, guidance_scale=guidance_scale).images[0]


# def resize_gen_img(img):
#     # Convert PIL image to NumPy array
#     numpy_image = np.array(img)

#     # Convert RGB to BGR (OpenCV uses BGR color format)
#     img = cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)

#     # Resize the image to the desired dimensions
#     resized_img = cv2.resize(img, (6*96, 9*96))

#     # Convert OpenCV image (BGR format) to RGB
#     resized_img_rgb = cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB)

#     # Convert numpy array to PIL Image
#     pil_image = Image.fromarray(resized_img_rgb)

#     return pil_image


# def blur_rectangle(image, x_percentage, y_percentage, width_percentage, height_percentage):
#     # Convert PIL image to NumPy array
#     numpy_image = np.array(image)

#     # Convert RGB to BGR (OpenCV uses BGR color format)
#     image = cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)

#     # Get image dimensions
#     height, width, _ = image.shape

#     # Calculate rectangle dimensions based on percentages
#     x = int(width * x_percentage)
#     y = int(height * y_percentage)
#     w = int(width * width_percentage)
#     h = int(height * height_percentage)

#     # Calculate rectangle coordinates
#     x1 = x - w // 2
#     y1 = y - h // 2
#     x2 = x + w // 2
#     y2 = y + h // 2

#     # Create a copy of the image
#     blurred_image = image.copy()

#     # Blur the specified rectangle
#     blurred_image[y1:y2, x1:x2] = cv2.GaussianBlur(
#         blurred_image[y1:y2, x1:x2], (25, 25), 0)

#     # Convert OpenCV image (BGR format) to RGB
#     blurred_img_rgb = cv2.cvtColor(blurred_image, cv2.COLOR_BGR2RGB)

#     # Convert numpy array to PIL Image
#     pil_image = Image.fromarray(blurred_img_rgb)
#     return pil_image

# def add_en_text(english_title, arabic_title, arabic_authors, english_authors, image, x_percentage, y_percentage, width_percentage, height_percentage):
    
#     image_temp = image
#     # Convert PIL image to NumPy array
#     numpy_image = np.array(image_temp)

#     # Convert RGB to BGR (OpenCV uses BGR color format)
#     image_temp = cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)

#     # Get image dimensions
#     height, width, _ = image_temp.shape

#     # Calculate rectangle dimensions based on percentages
#     x = int(width * x_percentage)
#     y = int(height * y_percentage)
#     w = int(width * width_percentage)
#     h = int(height * height_percentage)

#     title_font_resize = cv2.FONT_HERSHEY_SIMPLEX
#     arabic_title_font = ImageFont.truetype(
#         'C:\\Users\\Youssef Tarek\\LiteraryHub\\src\\books-cover-generator\\font.ttf', size=55)
#     arabic_title = arabic_reshaper.reshape(arabic_title)

#     # Add text to the center of the blurred rectangle
#     title_text_size = cv2.getTextSize(
#         english_title, title_font_resize, 1, 2)[0]
#     title_text_x = x - title_text_size[0] // 2
#     title_text_y = (y + title_text_size[1] // 2) - 150

#     image = ImageDraw.Draw(image)
#     image.text((title_text_x, title_text_y), get_display(
#         arabic_title), font=arabic_title_font, fill='black')

#     authors_font = cv2.FONT_ITALIC

#     counter = 50
#     authors_arabic_title_font = ImageFont.truetype('C:\\Users\\Youssef Tarek\\LiteraryHub\\src\\books-cover-generator\\font.ttf', size=30)
#     for i in range(len(english_authors)):
#         authors_text_size = cv2.getTextSize(
#             english_authors[i], authors_font, 1, 2)[0]
#         authors_text_x = x - authors_text_size[0] // 2 + 30
#         authors_text_y = (y + authors_text_size[1] // 2) - counter
#         image.text((authors_text_x, authors_text_y), get_display(arabic_reshaper.reshape(
#             arabic_authors[i])), font=authors_arabic_title_font, fill='black')
#         counter = counter - 30

#     return image


# def generate_book_cover(arabic_title, arabic_authors, book_summary, num_inference_steps, guidance_scale):
#     english_book_summary = arabic2english(book_summary)

#     if count_tokens(english_book_summary) > 77:
#         english_book_summary = english_text_summarizer(english_book_summary)

#     # english_title = arabic2english(arabic_title)
#     gen_image = gen_img(prompt=english_book_summary,
#                         num_inference_steps=num_inference_steps, guidance_scale=guidance_scale)
#     resized_img = resize_gen_img(gen_image)
#     base_cover = blur_rectangle(image=resized_img, x_percentage=0.5,
#                                 y_percentage=0.8, width_percentage=0.9, height_percentage=0.3)

#     english_authors = []
#     for i in range(len(arabic_authors)):
#         english_authors.append(
#             replace_arabic_with_english_letters(arabic_authors[i]))
        
    
        
#     english_title = arabic2english(arabic_title)

#     result_cover = add_en_text(english_title, arabic_title, arabic_authors, english_authors,
#                                 base_cover, x_percentage=0.5, y_percentage=0.8, width_percentage=0.9, height_percentage=0.3)

#     return result_cover


# @app.route('/get_book_cover', methods=['POST'])
# def get_book_cover():
#     # Get data from the request body
#     data = request.get_json()

#     # Extract parameters from the JSON data
#     book_title = data.get('book_title')
#     book_summary = data.get('book_summary')
#     arabic_authors = data.get('arabic_authors', [])
#     num_inference_steps = data.get('num_inference_steps', 5)
#     guidance_scale = data.get('guidance_scale', 0.6)

#     # Generate the book cover
#     book_cover = generate_book_cover(
#         arabic_title=book_title, arabic_authors=arabic_authors,
#         book_summary=book_summary, num_inference_steps=num_inference_steps,
#         guidance_scale=guidance_scale
#     )

#     # Get the image from the book cover
#     image = book_cover._image

#     # Save the image to a BytesIO object
#     img_bytesio = BytesIO()
#     image.save(img_bytesio, format='PNG')
#     img_bytes = img_bytesio.getvalue()

#     # Return the image as a response
#     return send_file(BytesIO(img_bytes), mimetype='image/png', as_attachment=True, download_name='book_cover.png')


# if __name__ == '__main__':
#     app.run(debug=True, port=5002)
