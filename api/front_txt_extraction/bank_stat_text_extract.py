import os
import json
from PIL import Image
import google.generativeai as genai
from pdf2image import convert_from_path

# api key
with open('GEMINI_API_KEY.txt', 'r') as key_file:
    os.environ['GEMINI_API_KEY'] = key_file.read().strip()

genai.configure(api_key=os.environ['GEMINI_API_KEY'])

# gemini model
MODEL_NAME = "gemini-1.5-flash"
model = genai.GenerativeModel(model_name=MODEL_NAME)

class BankStatementExtractor:
    def extract_text_from_file(self, file_path: str) -> str:
        if file_path.lower().endswith(".pdf"):
            pages = convert_from_path(file_path, first_page=1, last_page=1)
            image = pages[0]
        else:
            image = Image.open(file_path)
        prompt = (
            "Extract all text from the bank statement image, ensuring to capture the following information: branch, account_number, currency, date_from, date_to, previous_balance, current_balance, available_balance, transactions. "
            "For transactions, return an array of objects with keys: date, ref_number, description, debit, credit, balance. "
            "Return ONLY valid JSON with the specified keys. Do NOT add any extra words or explanations outside the JSON. "
            "Remove any '\\n' that appears. "
            "Example:\n"
            "{\n"
            "  \"branch\": \"BADR CITY BRANCH\",\n"
            "  \"account_number\": \"1133010376000301012\",\n"
            "  \"currency\": \"Egyptian Pound\",\n"
            "  \"date_from\": \"01/05/2020\",\n"
            "  \"date_to\": \"09/11/2020\",\n"
            "  \"previous_balance\": \"912.15\",\n"
            "  \"current_balance\": \"742.15\",\n"
            "  \"available_balance\": \"742.15\",\n"
            "  \"transactions\": [\n"
            "      { \"date\": \"30/06/2020\", \"ref_number\": \"113CB21EGP\", \"description\": \"Admin Fees\", \"debit\": \"30.00\", \"credit\": \"\", \"balance\": \"882.15\" }\n"
            "  ]\n"
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
        folder_path = "./bank_states"
        results = []
        for filename in os.listdir(folder_path):
            if filename.lower().endswith((".jpg", ".jpeg", ".png", ".pdf")):
                file_path = os.path.join(folder_path, filename)
                print(f"Processing {filename}...")
                raw_output = self.extract_text_from_file(file_path)
                parsed_data = self.parse_json_response(raw_output)
                results.append({
                    "file": filename,
                    "extracted_info": parsed_data
                })
        with open("extracted_bank_text.json", "w", encoding="utf-8") as json_file:
            json.dump(results, json_file, indent=4, ensure_ascii=False)
        print("All files processed successfully!")

def main():
    extractor = BankStatementExtractor()
    extractor.run()

if __name__ == "__main__":
    main()