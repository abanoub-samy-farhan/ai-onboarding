import os
import json
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()



genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))

MODEL_NAME = "gemini-1.5-flash"
model = genai.GenerativeModel(model_name=MODEL_NAME)

class FrontIDExtractor:
    def extract_text_from_image(self, image_path: str) -> str:
        image = Image.open(image_path)
        prompt = (
            "Extract all text from the Egyptian national ID image, ensuring the first name is not omitted, "
            "and convert all Arabic text and digits to English. "
            "The valid ID number is always a 14-digit numeric code near the bottom right. Ignore any code that "
            "contains letters or fewer digits on the bottom-left corner (that is NOT the ID number). "
            "Return ONLY valid JSON in English with the following keys: fullname, address, id_number, birthdate, is_valid. "
            "For id_number and birthdate, convert any Arabic digits to English digits (e.g., 1234567890). "
            "For the birthdate, use the format year/month/day (e.g., 1990/07/29). "
            "For fullname and address, convert the text from Arabic to English. "
            "For is_valid, return true if the ID appears to be valid, otherwise return false. "
            "Do NOT add any extra words or explanations outside the JSON. "
            "Remove any '\\n' that appears. "
            "Example:\n"
            "{\n"
            "  \"fullname\": \"...\",\n"
            "  \"address\": \"...\",\n"
            "  \"id_number\": \"...\",\n"
            "  \"birthdate\": \"...\",\n"
            "  \"is_valid\": true\n"
            "}"
        )
        response = model.generate_content([prompt, image])
        return response.text

    def parse_json_response(self, raw_text: str) -> dict:
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

    def run(self, image_path: str):
        results = []
        print(f"Processing {os.path.basename(image_path)}...")
        raw_output = self.extract_text_from_image(image_path)
        parsed_data = self.parse_json_response(raw_output)
        results.append({
            "image": os.path.basename(image_path),
            "extracted_info": parsed_data
        })
        with open("extracted_front_text.json", "w", encoding="utf-8") as json_file:
            json.dump(results, json_file, indent=4, ensure_ascii=False)
        print("Image processed successfully!")
        return results

def main():
    image_path = "./dataset2/2.jpg"
    extractor = FrontIDExtractor()
    extractor.run(image_path)

if __name__ == "__main__":
    main()
