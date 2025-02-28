import os
import json
from PIL import Image
import google.generativeai as genai

# load api key
with open('GEMINI_API_KEY.txt', 'r') as key_file:
    os.environ['GEMINI_API_KEY'] = key_file.read().strip()

genai.configure(api_key=os.environ['GEMINI_API_KEY'])

MODEL_NAME = "gemini-1.5-flash"
model = genai.GenerativeModel(model_name=MODEL_NAME)

class BackIDExtractor:
    def extract_text_from_image(self, image_path: str) -> str:
        image = Image.open(image_path)

        # prompt to extract the details
        prompt = (
            "Extract all text from the Egyptian national ID image, ensuring no essential information is omitted. "
            "The valid ID number is always a 14-digit numeric code near the bottom right. Ignore any code that "
            "contains letters or fewer digits on the bottom-left corner (that is NOT the ID number). "
            "Return ONLY valid JSON with the following keys: id_number, marital_status, gender, religion, occupation."
            "For marital_status, religion, and occupation, transform them from Arabic to English."
            "For id_number, transform it from Arabic to English digits (e.g., 1234567890)."
            "For gender,  transform it from Arabic to English to be  male or female. "
            "Do NOT add any extra words or explanations outside the JSON. "
            "Remove any '\n' that appears."
            "Example:\n"
            "{\n"
            "  \"id_number\": \"...\",\n"
            "  \"marital_status\": \"...\",\n"
            "  \"gender\": \"...\",\n"
            "  \"religion\": \"...\",\n"
            "  \"occupation\": \"...\"\n"
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

    def run(self):
        folder_path = "./dataset1"
        results = []
        for filename in os.listdir(folder_path):
            if filename.lower().endswith((".jpg", ".jpeg", ".png")):
                image_path = os.path.join(folder_path, filename)
                print(f"Processing {filename}...")  # Progress update
                raw_output = self.extract_text_from_image(image_path)
                parsed_data = self.parse_json_response(raw_output)
                results.append({
                    "image": filename,
                    "extracted_info": parsed_data
                })
        with open("extracted_back_text.json", "w", encoding="utf-8") as json_file:
            json.dump(results, json_file, indent=4, ensure_ascii=False)
        print("All images processed successfully!")

def main():
    extractor = BackIDExtractor()
    extractor.run()

if __name__ == "__main__":
    main()