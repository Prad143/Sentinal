import re
import requests
from urllib.parse import urljoin
from utils.file_operations import read_urls_from_file, write_to_file

def extract_js_urls(html_content, base_url):
    js_urls = []
    script_tags = re.findall(r'<script.*?src=["\'](.+?)["\']', html_content, re.IGNORECASE)
    for src in script_tags:
        full_url = urljoin(base_url, src)
        js_urls.append(full_url)
    return js_urls

def extract_inline_js(html_content):
    inline_js = re.findall(r'<script>(.*?)</script>', html_content, re.DOTALL)
    return inline_js

def fetch_js_content(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        pass
    return None

def scan_javascript(input_file, output_file):
    urls = read_urls_from_file(input_file)
    all_js_content = set()
    js_url_mapping = {}

    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                # Extract and process external JavaScript
                js_urls = extract_js_urls(response.text, url)
                for js_url in js_urls:
                    js_content = fetch_js_content(js_url)
                    if js_content:
                        all_js_content.add(js_content)
                        if js_content not in js_url_mapping:
                            js_url_mapping[js_content] = []
                        js_url_mapping[js_content].append(js_url)
                
                # Extract and process inline JavaScript
                inline_js = extract_inline_js(response.text)
                for js in inline_js:
                    all_js_content.add(js)
                    if js not in js_url_mapping:
                        js_url_mapping[js] = []
                    js_url_mapping[js].append(f"{url} (inline)")
        except requests.RequestException:
            continue

    # Write unique JavaScript content to file
    write_to_file(output_file, "\n".join(all_js_content))

    # Write JavaScript URL mapping to file
    url_mapping_file = output_file.replace('.txt', '_url_mapping.txt')
    with open(url_mapping_file, 'w') as f:
        for content, urls in js_url_mapping.items():
            f.write(f"Content Hash: {hash(content)}\n")
            f.write("URLs:\n")
            for url in urls:
                f.write(f"- {url}\n")
            f.write("\n")

    print(f"JavaScript scanning complete. Results written to {output_file} and {url_mapping_file}")

if __name__ == "__main__":
    # This allows the script to be run standalone for testing
    from config import FILE_NAME, JS_SCANNER_FILE_NAME
    scan_javascript(FILE_NAME, JS_SCANNER_FILE_NAME)