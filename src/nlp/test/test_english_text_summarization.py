import unittest
from ..summarization.english_text_summarization import generate_summary

class TestGenerateSummary(unittest.TestCase):
    def test_generate_summary(self):
        # provide a long piece of text more than 100 words
        text = """
        Artificial intelligence (AI) is the intelligence of machines or software, as opposed to the intelligence of living beings, primarily of humans. It is a field of study in computer science that develops and studies intelligent machines. Such machines may be called AIs.
        AI technology is widely used throughout industry, government, and science. Some high-profile applications are: advanced web search engines (e.g., Google Search), recommendation systems (used by YouTube, Amazon, and Netflix), interacting via human speech (e.g., Google Assistant, Siri, and Alexa), self-driving cars (e.g., Waymo), generative and creative tools (e.g., ChatGPT and AI art), and superhuman play and analysis in strategy games (e.g., chess and Go).[1] However, many AI applications are not perceived as AI: "A lot of cutting edge AI has filtered into general applications, often without being called AI because once something becomes useful enough and common enough it's not labeled AI anymore."[2][3]
        Alan Turing was the first person to conduct substantial research in the field that he called machine intelligence.[4] Artificial intelligence was founded as an academic discipline in 1956.[5] The field went through multiple cycles of optimism,[6][7] followed by periods of disappointment and loss of funding, known as AI winter.[8][9] Funding and interest vastly increased after 2012 when deep learning surpassed all previous AI techniques,[10] and after 2017 with the transformer architecture.[11] This led to the AI boom of the early 2020s, with companies, universities, and laboratories overwhelmingly based in the United States pioneering significant advances in artificial intelligence.[12]
        The growing use of artificial intelligence in the 21st century is influencing a societal and economic shift towards increased automation, data-driven decision-making, and the integration of AI systems into various economic sectors and areas of life, impacting job markets, healthcare, government, industry, and education. This raises questions about the ethical implications and risks of AI, prompting discussions about regulatory policies to ensure the safety and benefits of the technology.
        """
        summary = generate_summary(text)
        print(f"Summary: {summary}")
        self.assertIsInstance(summary, str)
        self.assertGreater(len(text), len(summary))


if __name__ == '__main__':
    unittest.main()