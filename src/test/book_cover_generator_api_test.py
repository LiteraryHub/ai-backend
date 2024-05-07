import requests
# from utils.Utils import *
import cv2
import arabic_reshaper
from bidi.algorithm import get_display
from PIL import Image, ImageDraw, ImageFont
import numpy as np 
from io import BytesIO

# Replace this URL with the actual URL where your Flask application is running
API_URL = 'http://127.0.0.1:5002'
 

def test_get_book_cover():
    # Sample data for the book cover request
    data = {
        'book_title': 'الطريق',
        'book_summary': 'تدور أحداث هذه الرواية التي قدمها الأديب المصري نجيب محفوظ في عام 1964 في كل من العاصمة المصرية القاهرة ومدينة الإسكندرية، حيث تتحدث عن أحد الأشخاص الذين قد جبلت حياتهم بالمشاكل والآلام والذي يدعى “صابر” حيث أنّه يكون قد ولد لأم تعمل في مجال الأعمال الغير أخلاقية، وعندما يكبر يستفسر من والدته عن والده “سيد رحيمي” ومن هو، فتخبره بأن والده قد توفي وهو ما زال طفلا صغيرا، وهنا يقتنع بكلامها ويعيش معها مدة طويلة من الزمن معتقداً بان والده قد مات، هذه المدة التي لم يكن قد تعلم بها أي شيء ولم يتقن أي مهنة كانت، وفي احدى المرات يتم القبض على والدته بتهمة العمل الغير أخلاقي الذي تمتهنه، ويتم مصادرة كل أموالها لدرجة أنه لم يبقى منه شيئاً يستطيع أن يصرف على نفسه منه، وبعدها يتم إدخال والدته إلى السجن.',
        'arabic_authors': ['المؤلف', 'نجيب محفوظ'],
        'num_inference_steps': 6,
        'guidance_scale': 0.4
    }

    # Make a POST request to the API to generate the book cover
    response = requests.post(f'{API_URL}/get_book_cover', json=data)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        print("works!")
        # Save the received image as 'test_book_cover.png'
        with open('test_book_cover.png', 'wb') as file:
            file.write(response.content)
            
    else:
        print("error!")


if __name__ == '__main__':
    test_get_book_cover()


