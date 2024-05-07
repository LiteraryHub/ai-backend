from pathlib import Path
from openai import OpenAI
client = OpenAI(api_key="sk-proj-rnJGXpB3BcJkgk84f7EfT3BlbkFJ5FQXHAVOnQcRDxel7fuP")

text = """فتوحات المكية من أعظم كتب ابن عربي في علم التصوف التي تحتوي أكثر من 4000صفحة قال فيها الشيخ كنت نويت الحج والعمرة
فلما وصلت أم القرى أقام هللافي خاطرى أن أعرف الولي يفنون من المعارف حصلتها في غيبتى، وكان االغلب هذهمنها ما فتح هللا
على ثم طوافى بيته المكر، وقال في الباب الثامنواألربعين واعلم ان ترتيب أبواب الفتوحات لم يكن عن اختيار وال عن نظرالمذوق
وإنما الحق. هللا يملى لنا على لسان ملك اإللهام جميع ما نسطره وقدنذكر كالما بين كالمين ال تعلق له بما قبله والبما بعده، وذلك شبيه
بقولهللا: "حافظوا على الصلوات والصالة الوسطى" . بين آيات طالق ونكاح وعدةووفاة وقال واعلم ان جميع مااتكلم فيه في مجالسى
وتصانيفى انما هو من حضرةالقرآن وخزائنه فانى أعطيتمفاتيح الفهم فيه واالمداد منه. وفي أوله مقدمةفي فهرسة ذكر فيه خمسمائة
وستين بابًا والباب التاسع والخمسون وخمسمائة منهباب عظيم جمع فيه أسرار الفتوحات كلها وجد بخطه في آخر الفتوحات من هذا
الباب في شهر بنو سنة تسع وعشرين وستمائة"""

speech_file_path = Path(__file__).parent / "speech.mp3"
response = client.audio.speech.create(
    model="tts-1-hd",
    voice="alloy",
    input=text,
)

# content, `.with_streaming_response.method()` should be used instead
# response.stream_to_file(speech_file_path)

response.write_to_file(speech_file_path)
# response.stream_to_file(speech_file_path)
