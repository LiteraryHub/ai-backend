from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

def translate_arabic_to_english(text):
   """
   Translates Arabic text to English using a pre-trained model.

   Parameters:
   - text (str): The Arabic text to be translated.

   Returns:
   - str: The translated English text.

   Example:
   arabic_text = "تدور أحداث هذه الرواية..."
   english_translation = translate_arabic_to_english(arabic_text)

   The function takes an Arabic text as input and returns the translated English text.
   It uses a pre-trained model to perform the translation.

   The translation process involves the following steps:
   1. Tokenize the input text and convert it to PyTorch tensors.
   2. Generate translations using the pre-trained model.
      - Beam search with 5 beams is used to generate multiple sequences for diversity.
   3. Decode the generated sequences, skipping special tokens.
   4. Return the first decoded sequence (highest probability) as the translation.
   """

   # Load pre-trained tokenizer and model for Arabic-to-English translation
   tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-ar-en")
   model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-ar-en")
   # Tokenize the input text and convert it to PyTorch tensors.
   input_ids = tokenizer(text, return_tensors="pt").input_ids

   # Generate translations using the pre-trained model.
   # Use beam search with 5 beams and return 3 sequences for diversity.
   outputs = model.generate(input_ids=input_ids, num_beams=5, num_return_sequences=3)

   # Decode the generated sequences, skipping special tokens.
   decoded_outputs = tokenizer.batch_decode(outputs, skip_special_tokens=True)

   # Return the first decoded sequence (highest probability) as the translation.
   return decoded_outputs[0]