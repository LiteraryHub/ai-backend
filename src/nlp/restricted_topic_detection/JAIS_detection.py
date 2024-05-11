import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from collections import Counter
import os
import json
import time
from tqdm import tqdm

device = "cuda" if torch.cuda.is_available() else "cpu"

model_path = "inception-mbzuai/jais-13b-chat"

tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path, device_map="auto", trust_remote_code=True, low_cpu_mem_usage=True)


def get_response(text, tokenizer=tokenizer, model=model):
    """
    Generates a response given an input text using the specified tokenizer and model.

    Args:
        text (str): The input text for which a response is generated.
        tokenizer: The tokenizer used to tokenize the input text.
        model: The model used to generate the response.

    Returns:
        str: The generated response.

    """
    input_ids = tokenizer(text, return_tensors="pt").input_ids
    inputs = input_ids.to(device)
    input_len = inputs.shape[-1]
    generate_ids = model.generate(
        inputs,
        top_p=0.9,
        temperature=1,
        max_length=2048,
        min_length=input_len + 4,
        repetition_penalty=1.2,
        do_sample=True,
    )
    response = tokenizer.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=True)[0]
    response = response.split("### Response: [|AI|]")
    return response


def parse_model_response(model_response):
    """
    Parses the model response and returns a label.

    Args:
        model_response (str): The response from the model.

    Returns:
        int: The label extracted from the model response. Returns 0 if "0" is found in the response,
        returns 1 if "1" is found in the response, otherwise returns 1.
    """
    cleaned_response = model_response.strip().replace("\n", " ")
    
    cleaned_response = ''.join(filter(str.isdigit, cleaned_response))
    print("cleaned_response: ", cleaned_response)
    if "0" in cleaned_response:
        return 0
    elif "1" in cleaned_response:
        return 1
    else:
        return 1


def check_restricted_content(text):
    """
    Check if the given text contains any restricted topics.

    Args:
        text (str): The text to be analyzed.

    Returns:
        int: A binary value indicating whether the text contains any restricted topics.
            - If the text does not contain any restricted topics, return 0.
            - If the text contains any restricted topics, return 1.
    """
    prompt = """
    ### Instruction:
    Carefully analyze the provided Arabic text to identify the presence of any prohibited themes listed below. You must consider both the explicit and implicit content, evaluating the context, nuances, and implications of each mentioned aspect. This analysis is critical in determining compliance with the outlined prohibitions. Your response should be a single digit, "0" or "1", based solely on the criteria given below:

    #### Prohibited Themes:
    1. **Sensitive Religious Content**: This includes any form of disrespect or derogatory remarks towards any religion, mockery of religious scriptures, symbols, rituals, or revered figures, and the promotion of religious or sectarian hatred or violence.
    2. **Profanity and Obscene Language**: Encompasses the use of any foul, vulgar, or obscene language, insults, slurs, or any form of speech that is overtly offensive or abusive towards any individual or group.
    3. **Sexual Content**: Detailed descriptions or depictions of sexual acts, explicit or implicit promotion of pornography, or any content that could be seen as promoting or glorifying sexual exploitation or harassment.
    4. **Political Sensitivity**: Content that could potentially incite political unrest, contains controversial or provocative criticism of governments or political figures, or could be interpreted as political propaganda.
    5. **Violence and Hate Speech**: Advocacy of violence or terrorism, content promoting or inciting hatred against individuals or groups based on race, religion, gender, sexual identity, or other distinguishing characteristics.
    6. **Illegal Activities**: Promotion or encouragement of illegal acts such as drug use, theft, fraud, hacking, or piracy.
    7. **Racist or Sexist Content**: Any content that promotes racial or sexual discrimination, reinforces harmful stereotypes, or includes racial or sexual insults.
    8. **Harmful or Dangerous Content**: Promotions of self-harm, participation in dangerous challenges, instructions for creating weapons, or engaging in unsafe practices.

    ### Evaluation Criteria:
    - Respond with "0" if none of the prohibited themes are present within the text.
    - Respond with "1" if any of the prohibited themes are identified in the text.

    ### Note:
    In cases of uncertainty, prioritize a comprehensive re-evaluation of the text, examining each element in question more closely. If doubt persists after a detailed analysis, respond with "1" to err on the side of caution.

    ### Input Format: 
    [|Human|] {text}
    
    ### Output Format: Must be a single digit, "0" or "1".

    ### Response: [|AI|]
    """.format(text=text)

    model_response = get_response(prompt)
    return parse_model_response(model_response[1])


def get_restricted_content_prediction(text, iterations=3):
    """
    Repeats the restricted content check multiple times to determine the most common label and its confidence level.
    
    Args:
        text (str): The text to be analyzed for restricted content.
        iterations (int, optional): The number of times to repeat the content analysis. Defaults to 5.

    Returns:
        tuple: A tuple containing the most common label (0 or 1) and its confidence level.

    """
    predictions = []
    for _ in tqdm(range(iterations), desc="Predicting"):
        predictions.append(check_restricted_content(text))
    prediction_count = Counter(predictions)

    most_common_label, most_common_count = prediction_count.most_common(1)[0]
    confidence = most_common_count / iterations
    return most_common_label, confidence