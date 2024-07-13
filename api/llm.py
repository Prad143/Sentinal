import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL

class GeminiLLM:
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(GEMINI_MODEL)

    def analyze_javascript(self, js_content):
        prompt = """
        You are a cybersecurity expert with 20 years of experience in searching for vulnerabilities in source code.
        Analyze the following JavaScript code for potential security vulnerabilities:

        {js_content}

        Please provide a detailed report on any vulnerabilities found, including:
        1. The type of vulnerability
        2. The location in the code
        3. The potential impact
        4. Recommendations for mitigation
        """

        response = self.model.generate_content(prompt.format(js_content=js_content))
        return response.text

def analyze_javascript(js_file_path):
    llm = GeminiLLM()
    
    with open(js_file_path, 'r') as file:
        js_content = file.read()
    
    analysis = llm.analyze_javascript(js_content)
    
    output_file_path = js_file_path.replace('.txt', '_analysis.txt')
    with open(output_file_path, 'w') as file:
        file.write(analysis)
    
    print(f"Analysis complete. Results written to {output_file_path}")