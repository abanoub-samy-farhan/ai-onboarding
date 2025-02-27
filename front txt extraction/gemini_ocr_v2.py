import os
import json
from PIL import Image
import google.generativeai as genai

# api key
with open('GEMINI_API_KEY.txt', 'r') as key_file:
    os.environ['GEMINI_API_KEY'] = key_file.read().strip()

genai.configure(api_key=os.environ['GEMINI_API_KEY'])

# gemini model
MODEL_NAME = "gemini-1.5-flash"
model = genai.GenerativeModel(model_name=MODEL_NAME)

# image + prompt -> gemini -> extracted text 
def extract_text_from_image(image_path: str) -> str:
    image = Image.open(image_path)

    # prompt (for gemini) to extract ID info as json
    prompt = (
        "Extract all text from the Egyptian national ID image, ensuring the first name is not omitted. "
        "The valid ID number is always a 14-digit numeric code near the bottom right. Ignore any code that "
        "contains letters or fewer digits on the bottom-left corner (that is NOT the ID number). "
        "Return ONLY valid JSON with the following keys: fullname, address, id_number, birthdate. "
        "For id_number and birthdate, use Arabic digits (e.g., ١٢٣٤٥٦٧٨٩٠). "
        "Do NOT add any extra words or explanations outside the JSON. "
        "Remove any '\n' that appears."
        "Example:\n"
        "{\n"
        "  \"fullname\": \"...\",\n"
        "  \"address\": \"...\",\n"
        "  \"id_number\": \"...\",\n"
        "  \"birthdate\": \"...\"\n"
        "}"
    )

    response = model.generate_content([prompt, image])
    return response.text

# parsing + cleaning
def parse_json_response(raw_text: str) -> dict:
    cleaned_text = raw_text.replace("\n", " ")
    start = cleaned_text.find('{')
    end = cleaned_text.rfind('}')
    if start == -1 or end == -1 or start > end:
        return {"raw_extraction": cleaned_text}

    json_part = cleaned_text[start:end+1].strip()

    try:
        data = json.loads(json_part)
    except json.JSONDecodeError:
        data = {"raw_extraction": cleaned_text}

    return data

def main():
    folder_path = "./dataset2"
    results = []

    for filename in os.listdir(folder_path):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            image_path = os.path.join(folder_path, filename)
            # visuals for fun
            print(f"Processing {filename}...")

            # extract + parse
            raw_output = extract_text_from_image(image_path)
            parsed_data = parse_json_response(raw_output)

            results.append({
                "image": filename,
                "extracted_info": parsed_data
            })

    # yay writing the json data to the file
    with open("extracted_text.json", "w", encoding="utf-8") as json_file:
        json.dump(results, json_file, indent=4, ensure_ascii=False)
    
    print("All images processed.")

if __name__ == "__main__":
    main()