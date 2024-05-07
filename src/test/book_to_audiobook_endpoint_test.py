import requests
import time

def test_text_to_speech_endpoint_v2():
    """
    Test the text-to-speech endpoint by sending an Arabic text and saving the response as an audio file.

    This function sends a POST request to the text-to-speech endpoint with an Arabic text. If the request is successful,
    the response content is saved as an audio file. The audio file is then loaded using pydub library.

    Returns:
        None
    """

    url = 'http://127.0.0.1:8001/audiobook/v2/text-to-speech/'
    
    with open("./src/test/Untitled.txt", 'r', encoding='utf-8') as file:
        text = file.read()

    print("reading completed")
    
    text = """فتوحات المكية من أعظم كتب ابن عربي في علم التصوف التي تحتوي أكثر من4000صفحة قال فيها الشيخ كنت نويت الحج والعمرة
فلما وصلت أم القرى أقام هللافي خاطرى أن أعرف الولي يفنون من المعارف حصلتها في غيبتى، وكان االغلب هذهمنها ما فتح هللا
على ثم طوافى بيته المكر، وقال في الباب الثامنواألربعين واعلم ان ترتيب أبواب الفتوحات لم يكن عن اختيار وال عن نظرالمذوق
وإنما الحق. هللا يملى لنا على لسان ملك اإللهام جميع ما نسطره وقدنذكر كالما بين كالمين ال تعلق له بما قبله والبما بعده، وذلك شبيه
بقولهللا: "حافظوا على الصلوات والصالة الوسطى" . بين آيات طالق ونكاح وعدةووفاة وقال واعلم ان جميع مااتكلم فيه في مجالسى
وتصانيفى انما هو من حضرةالقرآن وخزائنه فانى أعطيتمفاتيح الفهم فيه واالمداد منه. وفي أوله مقدمةفي فهرسة ذكر فيه خمسمائة
وستين بابًا والباب التاسع والخمسون وخمسمائة منهباب عظيم جمع فيه أسرار الفتوحات كلها وجد بخطه في آخر الفتوحات من هذا
الباب في شهر بنو سنة تسع وعشرين وستمائة"""
    text = text.encode('utf-8')
    print(text)
    data = {'text': text, 'book_name': 'test_book_2'}

    response = requests.post(url, json=data)

    # Assuming the request was successful, save the response to a file
    if response.status_code == 200:
        print("Audio v2 file saved.")
    else:
        print(f"Failed to fetch audio v2. Status code: {response.status_code}")

if __name__ == '__main__':
    start_time = time.time()
    test_text_to_speech_endpoint_v2()
    end_time = time.time()
    
    print(end_time - start_time)
