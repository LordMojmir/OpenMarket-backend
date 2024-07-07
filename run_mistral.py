import os
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import dotenv

dotenv.load_dotenv()

def get_response(prompt):
    model = "mistral-large-latest"
    api_key = os.getenv("MISTRAL_API_KEY")

    if not api_key:
        raise ValueError("API key not found in environment variables")

    custom_prompt = f'{prompt} create all the details of a character.'

    client = MistralClient(api_key=api_key)
    chat_response = client.chat(
        model=model,
        messages=[
            ChatMessage(role="system", content="You are a creative character creator. You are tasked with creating a character. The output should be an image generation prompt to create it. You are also in charge of creating key features of the character and a backstory. Make it concise and understandable for an LLM. Create real people and not mystical beings. Make the image a description of their LinkedIn profile picture. Describe only attractive people."),
            ChatMessage(role="user", content=custom_prompt)
        ],
    )

    return chat_response.choices[0].message.content

def extract_data(text, name):
    character_name = name
    key_features = {}
    backstory = ""
    image_prompt = ""

    # Split the text into lines
    lines = text.strip().split("\n")

    # Iterate through each line to extract data
    i = 0
    while i < len(lines):
        line = lines[i].strip()

        if line.startswith("Key Features:"):
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("Backstory:"):
                feature_line = lines[i].strip()
                if feature_line:
                    parts = feature_line.split(":")
                    if len(parts) == 2:
                        key = parts[0].strip()
                        value = parts[1].strip()
                        key_features[key] = value
                i += 1

        elif line.startswith("Backstory:"):
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("Image Generation Prompt:"):
                backstory += lines[i].strip() + " "
                i += 1
            backstory = backstory.strip()

        elif line.startswith("Image Generation Prompt:"):
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("store"):
                image_prompt += lines[i].strip() + " "
                i += 1
            image_prompt = image_prompt.strip()

        i += 1

    # Construct the extracted data into a dictionary
    data = {
        "Character Name": character_name,
        "Key Features": key_features,
        "Backstory": backstory,
        "Image Generation Prompt": image_prompt,
        "imgURL": "not yet implemented.com"
    }

    return data

if __name__ == "__main__":
    character_names = [
        "Scarlett", "Olivia", "Ethan", "Sophia", "Xavier",
        "Isabella", "Luca", "Ava", "Gabriel", "Amelia",
        "Mateo", "Mia", "Santiago", "Harper", "Elena",
        "Leonardo", "Stella", "Nico", "Grace", "Alessandro"
    ]

    for name in character_names:
        response = get_response(name)
        print(response)
        data = extract_data(response, name)
        print(data)

